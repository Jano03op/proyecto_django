# datosarray.py
"""
Fuente centralizada de datos para el Sistema de Gestión de Resultados (SGR).
Los datos de 'periodo' y 'personas' se leen dinámicamente desde datosarray.json
(requisito formal de persistencia en archivos JSON sin base de datos relacional).
"""

import json
from pathlib import Path

_DATA_PATH = Path(__file__).resolve().parent / "datosarray.json"

with open(_DATA_PATH, encoding="utf-8") as _archivo:
    _datos = json.load(_archivo)

periodo = _datos["periodo"]
personas = _datos["personas"]

# Colección base para la aplicación 'agenda' (Tablero Kanban)
compromisos = [
    {
        "id": 1,
        "titulo": "Instalación de luminarias Pasaje Las Rosas",
        "descripcion": "Coordinación con Alumbrado Público para recambio de luminarias LED.",
        "funcionario": "Pablo Cuadra Corrales",
        "delegacion": "Las Compañías",
        "fecha_registro": "2026-09-02",
        "fecha_limite": "2026-09-20",
        "estado": "En Proceso",
        "prioridad": "Alta",
        "contacto": "Patricia Collao",
    },
    {
        "id": 2,
        "titulo": "Operativo de batea y desmalezado",
        "descripcion": "Instalación de bateas comunitarias en Villa La Florida.",
        "funcionario": "Elizabeth Villanueva",
        "delegacion": "La Antena",
        "fecha_registro": "2026-09-02",
        "fecha_limite": "2026-09-15",
        "estado": "Por Iniciar",
        "prioridad": "Media",
        "contacto": "Carlos Araya",
    },
    {
        "id": 3,
        "titulo": "Taller postulación Subsidio DS49",
        "descripcion": "Segunda jornada informativa presencial para comité de allegados.",
        "funcionario": "María Soledad Rojas",
        "delegacion": "La Pampa",
        "fecha_registro": "2026-09-03",
        "fecha_limite": "2026-09-10",
        "estado": "Finalizado",
        "prioridad": "Media",
        "contacto": "Marta Gómez Castillo",
    },
    {
        "id": 4,
        "titulo": "Mantención camino vecinal quebrada El Romero",
        "descripcion": "Coordinación de maquinaria pesada para nivelación de camino rural.",
        "funcionario": "Manuel Barraza Delgado",
        "delegacion": "Rural",
        "fecha_registro": "2026-09-05",
        "fecha_limite": "2026-09-25",
        "estado": "En Proceso",
        "prioridad": "Alta",
        "contacto": "Juan Perez",
    },
]

# Colección base para la aplicación 'cuentas' (Usuarios del sistema)
usuarios = [
    {
        "id": 1,
        "username": "evillanueva",
        "nombre": "Elizabeth Villanueva",
        "email": "evillanueva@laserena.cl",
        "rol": "Delegada",
        "delegacion": "La Antena",
        "password": "password123",
        "activo": True,
    },
    {
        "id": 2,
        "username": "pcuadra",
        "nombre": "Pablo Cuadra Corrales",
        "email": "pcuadra@laserena.cl",
        "rol": "Encargado",
        "delegacion": "Las Compañías",
        "password": "password123",
        "activo": True,
    },
    {
        "id": 3,
        "username": "mrojas",
        "nombre": "María Soledad Rojas",
        "email": "mrojas@laserena.cl",
        "rol": "Encargada",
        "delegacion": "La Pampa",
        "password": "password123",
        "activo": True,
    },
    {
        "id": 4,
        "username": "rfuenzalida",
        "nombre": "Rodrigo Fuenzalida Vásquez",
        "email": "rfuenzalida@laserena.cl",
        "rol": "Encargado",
        "delegacion": "Avenida del Mar",
        "password": "password123",
        "activo": True,
    },
    {
        "id": 5,
        "username": "mbarraza",
        "nombre": "Manuel Barraza Delgado",
        "email": "mbarraza@laserena.cl",
        "rol": "Encargado",
        "delegacion": "Rural",
        "password": "password123",
        "activo": True,
    },
    {
        "id": 6,
        "username": "avonkretschmann",
        "nombre": "Alan Von Kretschmann",
        "email": "avonkretschmann@laserena.cl",
        "rol": "Coordinador",
        "delegacion": "Centro",
        "password": "password123",
        "activo": True,
    },
]
