# agenda/services.py
"""
Capa de servicios para la aplicación 'agenda'.
Gestiona los compromisos ciudadanos futuros y el tablero Kanban,
consumiendo datos centralizados desde datosarray.
"""

from datetime import date
from datosarray import compromisos, personas


def obtener_compromisos(filtro_estado=None, filtro_delegacion=None, filtro_funcionario=None):
    """Retorna la lista de compromisos aplicando filtros opcionales."""
    resultado = list(compromisos)

    if filtro_estado:
        resultado = [c for c in resultado if c.get("estado") == filtro_estado]

    if filtro_delegacion:
        resultado = [c for c in resultado if c.get("delegacion") == filtro_delegacion]

    if filtro_funcionario:
        resultado = [
            c for c in resultado 
            if filtro_funcionario.lower() in c.get("funcionario", "").lower()
        ]

    return resultado


def obtener_compromiso_por_id(compromiso_id):
    """Busca y retorna un compromiso por su ID."""
    for c in compromisos:
        if c.get("id") == compromiso_id:
            return c
    return None


def obtener_tablero_kanban():
    """Agrupa los compromisos por estado para visualización en tablero Kanban."""
    estados = ["Por Iniciar", "En Proceso", "Finalizado"]
    tablero = {estado: [] for estado in estados}
    for c in compromisos:
        estado = c.get("estado", "Por Iniciar")
        if estado in tablero:
            tablero[estado].append(c)
        else:
            tablero.setdefault(estado, []).append(c)
    return tablero


def crear_compromiso(titulo, descripcion, funcionario, delegacion, fecha_limite, prioridad="Media", contacto=""):
    """Registra un nuevo compromiso ciudadano en datosarray."""
    nuevo_id = max([c.get("id", 0) for c in compromisos], default=0) + 1
    nuevo_compromiso = {
        "id": nuevo_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "funcionario": funcionario,
        "delegacion": delegacion,
        "fecha_registro": str(date.today()),
        "fecha_limite": str(fecha_limite),
        "estado": "Por Iniciar",
        "prioridad": prioridad,
        "contacto": contacto,
    }
    compromisos.append(nuevo_compromiso)
    return nuevo_compromiso


def actualizar_estado_compromiso(compromiso_id, nuevo_estado):
    """Actualiza el estado de un compromiso en el tablero Kanban."""
    for c in compromisos:
        if c.get("id") == compromiso_id:
            c["estado"] = nuevo_estado
            return True
    return False
