"""
Este archivo concentra TODA la lógica que sabe leer y escribir ese JSON,
para que views.py se dedique únicamente a recibir la petición del
navegador y decidir qué template mostrar. A esta separación se le llama
"capa de servicios": views.py pregunta cosas como "dame todos los
compromisos" o "crea uno nuevo", y este archivo se encarga de hacerlo.
Los cuatro estados posibles de un compromiso son siempre estos, en este
orden:
    "Ingresado" -> "Pendiente" -> "En proceso" -> "Realizado"
"""
import json
from datetime import date, datetime
from django.conf import settings

# Lista de estados válidos, en el orden en que se muestran las columnas
# del tablero tipo kanban. Se define una sola vez aquí para no repetir
# el mismo texto en varios archivos (views.py y los templates la usan).
ESTADOS = ["Ingresado", "Pendiente", "En proceso", "Realizado"]
# Ruta absoluta al archivo JSON donde viven los compromisos.
# settings.BASE_DIR ya apunta a la carpeta raíz del proyecto Django,
# así que el archivo real queda en: <raíz_del_proyecto>/data/compromisos.json
DATA_FILE = settings.BASE_DIR / "data" / "compromisos.json"

def cargar_compromisos():
    """
    Si el archivo todavía no existe (por ejemplo, la primera vez que se
    ejecuta el proyecto en un computador nuevo) o si el contenido está
    dañado/corrupto, se devuelve una lista vacía en vez de hacer que la
    página falle con un error 500.
    """
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []


def guardar_compromisos(compromisos):
    """
    Recibe la lista completa de compromisos (ya modificada en memoria) y
    la vuelve a escribir en el archivo JSON, reemplazando todo su
    contenido anterior.
    Se crea la carpeta "data/" automáticamente si no existiera, para que
    el proyecto funcione aunque alguien clone el repositorio sin esa
    carpeta creada.
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as archivo:
        # ensure_ascii=False permite guardar tildes y ñ de forma legible.
        # indent=2 deja el archivo bien ordenado para poder revisarlo a mano.
        json.dump(compromisos, archivo, ensure_ascii=False, indent=2)


def obtener_compromisos(filtro_territorio=None, filtro_responsable=None, filtro_estado=None):
    """
    Devuelve la lista de compromisos aplicando filtros opcionales.
    Cualquier filtro que llegue en None o vacío simplemente se ignora.
    - filtro_territorio: deja solo los compromisos de una delegación exacta.
    - filtro_responsable: búsqueda parcial (no distingue mayúsculas) por
      el nombre del funcionario responsable.
    - filtro_estado: deja solo los compromisos que están en ese estado.
    """
    compromisos = cargar_compromisos()
    if filtro_territorio:
        compromisos = [c for c in compromisos if c.get("territorio") == filtro_territorio]
    if filtro_responsable:
        texto_buscado = filtro_responsable.lower()
        compromisos = [
            c for c in compromisos
            if texto_buscado in c.get("responsable", "").lower()]

    if filtro_estado:
        compromisos = [c for c in compromisos if c.get("estado") == filtro_estado]
    return compromisos


def obtener_compromiso_por_id(compromiso_id):
    """Busca un compromiso por su id numérico. Devuelve None si no existe."""
    for compromiso in cargar_compromisos():
        if compromiso.get("id") == compromiso_id:
            return compromiso
    return None


def agrupar_por_estado(compromisos):
    """
    Recibe una lista de compromisos y la organiza en un diccionario con
    una lista por cada estado. Esto es lo que necesita el template del
    tablero para dibujar las 4 columnas del kanban:
        {
            "Ingresado": [ ... ],
            "Pendiente": [ ... ],
            "En proceso": [ ... ],
            "Realizado": [ ... ],
        }
    """
    columnas = {estado: [] for estado in ESTADOS}
    for compromiso in compromisos:
        estado = compromiso.get("estado")
        if estado in columnas:
            columnas[estado].append(compromiso)
    return columnas

def esta_vencido(compromiso):
    """
    Regla de negocio simple: un
    compromiso está "vencido" cuando su fecha_compromiso ya pasó y
    todavía no está marcado como "Realizado".

    Se usa en el template para destacar en rojo los compromisos
    incumplidos, sin necesidad de guardar ese cálculo en el JSON.
    """
    if compromiso.get("estado") == "Realizado":
        return False
    try:
        fecha_limite = datetime.strptime(compromiso["fecha_compromiso"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return False
    return fecha_limite < date.today()


def crear_compromiso(origen, solicitante, territorio, responsable, area_apoyo,
                      descripcion, fecha_compromiso, autor):
    """
    Crea un compromiso nuevo, siempre en estado "Ingresado", y lo agrega al archivo JSON.
    El id del compromiso nuevo se calcula tomando el id más alto que ya
    existe y sumándole 1, para que nunca se repita un mismo id aunque se
    hayan eliminado compromisos anteriores.
    """
    compromisos = cargar_compromisos()
    nuevo_id = max([c.get("id", 0) for c in compromisos], default=0) + 1
    nuevo_compromiso = {
        "id": nuevo_id,
        "origen": origen,
        "solicitante": solicitante,
        "territorio": territorio,
        "responsable": responsable,
        "area_apoyo": area_apoyo,
        "descripcion": descripcion,
        "fecha_registro": str(date.today()),
        "fecha_compromiso": fecha_compromiso,
        "estado": "Ingresado",
        "observacion": "",
        # El historial guarda cada cambio de estado con su autor y fecha,
        "historial": [
            {
                "estado_anterior": None,
                "estado_nuevo": "Ingresado",
                "autor": autor,
                "fecha": str(date.today()),
                "observacion": "Compromiso registrado en la agenda colectiva.",
            }
        ],
    }

    compromisos.append(nuevo_compromiso)
    guardar_compromisos(compromisos)
    return nuevo_compromiso

def cambiar_estado_compromiso(compromiso_id, nuevo_estado, autor, observacion=""):
    """
    Cambia el estado de un compromiso existente y deja registro del
    cambio en su historial (estado anterior, estado nuevo, quién lo hizo,
    cuándo y con qué observación).
    Devuelve True si el compromiso existía y se pudo actualizar, o False
    si no se encontró ningún compromiso con ese id.
    """
    if nuevo_estado not in ESTADOS:
        return False
    compromisos = cargar_compromisos()
    encontrado = False
    for compromiso in compromisos:
        if compromiso.get("id") == compromiso_id:
            estado_anterior = compromiso.get("estado")
            compromiso["estado"] = nuevo_estado
            compromiso["observacion"] = observacion
            compromiso.setdefault("historial", []).append({
                "estado_anterior": estado_anterior,
                "estado_nuevo": nuevo_estado,
                "autor": autor,
                "fecha": str(date.today()),
                "observacion": observacion,})
            encontrado = True
            break
    if encontrado:
        guardar_compromisos(compromisos)
    return encontrado
