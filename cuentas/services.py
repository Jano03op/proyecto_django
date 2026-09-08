import json
from django.conf import settings

DATA_FILE = settings.BASE_DIR / "data" / "usuarios.json"

def cargar_usuarios():
    """Carga la lista completa de usuarios desde el archivo JSON."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []

def guardar_usuarios(usuarios):
    """Guarda la lista de usuarios en el archivo JSON."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, ensure_ascii=False, indent=2)

def autenticar_usuario(username, password):
    username_limpio = username.strip().lower()
    password_limpio = password.strip()
    
    for u in cargar_usuarios():
        if u.get("username", "").lower() == username_limpio and str(u.get("password")) == password_limpio:
            return {
                "id": u.get("id"),
                "username": u.get("username"),
                "nombre": u.get("nombre"),
                "cargo": u.get("cargo"),
                "rol": u.get("rol"),
                "delegacion": u.get("delegacion"),
                "email": u.get("email"),
            }
    return None

def obtener_usuario_por_id(usuario_id):
    """Retorna los datos públicos del usuario por su ID."""
    for u in cargar_usuarios():
        if u.get("id") == usuario_id:
            return {
                "id": u.get("id"),
                "username": u.get("username"),
                "nombre": u.get("nombre"),
                "cargo": u.get("cargo"),
                "rol": u.get("rol"),
                "delegacion": u.get("delegacion"),
                "email": u.get("email"),
            }
    return None

def registrar_usuario(username, password, nombre, cargo, rol, delegacion, email=""):
    """Registra un nuevo usuario en el sistema si el username no está repetido."""
    usuarios = cargar_usuarios()
    username_limpio = username.strip().lower()

    if any(u.get("username", "").lower() == username_limpio for u in usuarios):
        return None, "El nombre de usuario ya está registrado."

    nuevo_id = max([u.get("id", 0) for u in usuarios], default=0) + 1
    nuevo_usuario = {
        "id": nuevo_id,
        "username": username_limpio,
        "password": password.strip(),
        "nombre": nombre.strip(),
        "cargo": cargo.strip(),
        "rol": rol.strip(),
        "delegacion": delegacion.strip(),
        "email": email.strip(),
    }
    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    
    return {
        "id": nuevo_usuario["id"],
        "username": nuevo_usuario["username"],
        "nombre": nuevo_usuario["nombre"],
        "cargo": nuevo_usuario["cargo"],
        "rol": nuevo_usuario["rol"],
        "delegacion": nuevo_usuario["delegacion"],
        "email": nuevo_usuario["email"],
    }, None

