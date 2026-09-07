from datetime import date
from datosarray import periodo, personas, actividades

PREFIJOS_DELEGACION = {
    "La Antena": "ANT",
    "Las Compañías": "COM",
    "La Pampa": "PAM",
    "Avenida del Mar": "MAR",
    "Centro": "CEN",
    "Rural": "RUR",
}


def obtener_personas():
    """Retorna la lista de funcionarios y su configuración desde datosarray."""
    return personas


def obtener_delegaciones():
    """Retorna la lista ordenada de nombres de delegaciones únicas."""
    return sorted({p["delegacion"] for p in personas if "delegacion" in p})


def obtener_persona_por_nombre(nombre):
    """Busca y retorna los datos de una persona según su nombre."""
    for p in personas:
        if p.get("nombre") == nombre:
            return p
    return None


def obtener_items_funcionario(nombre):
    """Retorna la lista de ítems medibles asignados a un funcionario."""
    persona = obtener_persona_por_nombre(nombre)
    if persona:
        return persona.get("items", [])
    return []


def obtener_coordinador():
    """Retorna el funcionario con cargo de Coordinador, o el primero disponible."""
    for p in personas:
        if p.get("cargo") == "Coordinador":
            return p
    return personas[0] if personas else None


def cargar_actividades():
    """Retorna la lista de actividades desde datosarray."""
    return actividades


def guardar_actividades(nuevas_actividades):
    """Sincroniza la lista de actividades en memoria."""
    actividades.clear()
    actividades.extend(nuevas_actividades)


def obtener_actividades(filtro_delegacion=None, filtro_estado=None, filtro_funcionario=None):
    """Retorna actividades aplicando filtros opcionales."""
    resultado = list(actividades)

    if filtro_delegacion:
        resultado = [a for a in resultado if a.get("delegacion") == filtro_delegacion]

    if filtro_estado:
        resultado = [
            a for a in resultado 
            if a.get("evidencia", {}).get("estado") == filtro_estado
        ]

    if filtro_funcionario:
        resultado = [
            a for a in resultado 
            if filtro_funcionario.lower() in a.get("funcionario", "").lower()
        ]

    return resultado


def obtener_actividad_por_id(actividad_id):
    """Busca y retorna una actividad por su ID numérico."""
    for act in actividades:
        if act.get("id") == actividad_id:
            return act
    return None


def crear_actividad(fecha, funcionario, delegacion, item, descripcion, accion, contacto, telefono, archivo_evidencia=None):
    """Crea una nueva actividad, genera su código de evidencia y la agrega a datosarray."""
    nuevo_id = max([a.get("id", 0) for a in actividades], default=0) + 1

    # Normalizar fecha a formato ISO (YYYY-MM-DD) si viene como DD/MM/AAAA
    fecha_str = str(fecha).strip()
    if "/" in fecha_str:
        partes = fecha_str.split("/")
        if len(partes) == 3:
            fecha_str = f"{partes[2]}-{partes[1].zfill(2)}-{partes[0].zfill(2)}"

    # Generar prefijo de evidencia según delegación
    prefijo = PREFIJOS_DELEGACION.get(delegacion)
    if not prefijo:
        prefijo = (delegacion.replace(" ", "")[:3] if delegacion else "GEN").upper()
    codigo_evidencia = f"EVI-{prefijo}-{nuevo_id:03d}"

    nueva_actividad = {
        "id": nuevo_id,
        "fecha": fecha_str,
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
    return nueva_actividad


def actualizar_estado_evidencia(actividad_id, nuevo_estado, observacion="", verificador="Coordinación"):
    """Actualiza el estado y observaciones de la evidencia de una actividad."""
    for act in actividades:
        if act.get("id") == actividad_id:
            evidencia = act.get("evidencia", {})
            evidencia["estado"] = nuevo_estado
            evidencia["observacion"] = observacion
            evidencia["fecha_validacion"] = str(date.today())
            evidencia["verificador"] = verificador
            act["evidencia"] = evidencia
            return True
    return False
