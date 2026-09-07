# cuentas/services.py
"""
Capa de servicios para la aplicación 'cuentas'.
Gestiona autenticación, perfiles y usuarios del sistema,
consumiendo datos centralizados desde datosarray.
"""

from datosarray import usuarios, personas


def obtener_usuarios(filtro_delegacion=None, filtro_rol=None):
    """Retorna la lista de usuarios con filtros opcionales."""
    resultado = list(usuarios)

    if filtro_delegacion:
        resultado = [u for u in resultado if u.get("delegacion") == filtro_delegacion]

    if filtro_rol:
        resultado = [u for u in resultado if u.get("rol") == filtro_rol]

    return resultado


def obtener_usuario_por_username(username):
    """Busca un usuario por su nombre de usuario (case-insensitive)."""
    if not username:
        return None
    username_lower = username.strip().lower()
    for u in usuarios:
        if u.get("username", "").lower() == username_lower:
            return u
    return None


def obtener_usuario_por_id(usuario_id):
    """Busca un usuario por su identificador numérico."""
    for u in usuarios:
        if u.get("id") == usuario_id:
            return u
    return None


def autenticar_usuario(username, password):
    """Verifica credenciales del usuario contra la colección en memoria."""
    usuario = obtener_usuario_por_username(username)
    if usuario and usuario.get("password") == password and usuario.get("activo", True):
        return usuario
    return None


def registrar_usuario(username, nombre, email, rol, delegacion, password):
    """Registra un nuevo usuario en la colección centralizada."""
    if obtener_usuario_por_username(username):
        return None  # Usuario ya existe

    nuevo_id = max([u.get("id", 0) for u in usuarios], default=0) + 1
    nuevo_usuario = {
        "id": nuevo_id,
        "username": username.strip().lower(),
        "nombre": nombre.strip(),
        "email": email.strip().lower(),
        "rol": rol.strip(),
        "delegacion": delegacion.strip(),
        "password": password,
        "activo": True,
    }
    usuarios.append(nuevo_usuario)
    return nuevo_usuario


def cambiar_password(username, nuevo_password):
    """Actualiza la contraseña de un usuario."""
    usuario = obtener_usuario_por_username(username)
    if usuario:
        usuario["password"] = nuevo_password
        return True
    return False
