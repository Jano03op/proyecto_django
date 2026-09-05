import json
from datetime import date
from pathlib import Path
from django.conf import settings

DATA_FILE = settings.BASE_DIR / "data" / "actividades.json"


def cargar_actividades():
    """Lee y retorna la lista de actividades desde el archivo JSON."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def guardar_actividades(actividades):
    """Guarda la lista completa de actividades en el archivo JSON."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(actividades, f, ensure_ascii=False, indent=2)


def obtener_actividades(filtro_delegacion=None, filtro_estado=None, filtro_funcionario=None):
    """Retorna actividades aplicando filtros opcionales."""
    actividades = cargar_actividades()

    if filtro_delegacion:
        actividades = [a for a in actividades if a.get("delegacion") == filtro_delegacion]

    if filtro_estado:
        actividades = [
            a for a in actividades 
            if a.get("evidencia", {}).get("estado") == filtro_estado
        ]

    if filtro_funcionario:
        actividades = [
            a for a in actividades 
            if filtro_funcionario.lower() in a.get("funcionario", "").lower()
        ]

    return actividades


def obtener_actividad_por_id(actividad_id):
    """Busca y retorna una actividad por su ID numérico."""
    actividades = cargar_actividades()
    for act in actividades:
        if act.get("id") == actividad_id:
            return act
    return None


def crear_actividad(fecha, funcionario, delegacion, item, descripcion, accion, contacto, telefono, archivo_evidencia=None):
    """Crea una nueva actividad, genera su código de evidencia y persiste en el JSON."""
    actividades = cargar_actividades()
    nuevo_id = max([a.get("id", 0) for a in actividades], default=0) + 1

    # Generar prefijo de evidencia según delegación (primeras 3 letras o GEN)
    prefijo = (delegacion[:3] if delegacion else "GEN").upper()
    codigo_evidencia = f"EVI-{prefijo}-{nuevo_id:03d}"

    nueva_actividad = {
        "id": nuevo_id,
        "fecha": str(fecha),
        "funcionario": funcionario,
        "delegacion": delegacion,
        "item": item,
        "descripcion": descripcion,
        "accion": accion,
        "contacto": contacto,
        "telefono": telefono,
        "evidencia": {
            "codigo": codigo_evidencia,
            "archivo": archivo_evidencia or "img/evidencias/evidencia_01.svg",
            "estado": "Pendiente",
            "observacion": "",
            "fecha_validacion": None,
            "verificador": None,
        },
    }

    actividades.append(nueva_actividad)
    guardar_actividades(actividades)
    return nueva_actividad


def actualizar_estado_evidencia(actividad_id, nuevo_estado, observacion="", verificador="Coordinación"):
    """Actualiza el estado y observaciones de la evidencia de una actividad."""
    actividades = cargar_actividades()
    encontrado = False

    for act in actividades:
        if act.get("id") == actividad_id:
            evidencia = act.get("evidencia", {})
            evidencia["estado"] = nuevo_estado
            evidencia["observacion"] = observacion
            evidencia["fecha_validacion"] = str(date.today())
            evidencia["verificador"] = verificador
            act["evidencia"] = evidencia
            encontrado = True
            break

    if encontrado:
        guardar_actividades(actividades)
        return True
    return False
