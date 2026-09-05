# Sistema de Gestión de Resultados (SGR) — Delegaciones Municipales

Este proyecto corresponde a la **Evaluación Sumativa #1** de la asignatura **Programación Back End (TI3041)** en **INACAP La Serena**.

El sistema tiene como propósito centralizar el registro, verificación, seguimiento y medición de la gestión operativa de los funcionarios y las delegaciones de la Ilustre Municipalidad de La Serena.

---

## 1. Restricciones y Lineamientos Técnicos de la Evaluación

- **Persistencia sin base de datos**: Toda la información se almacena y consulta mediante archivos en formato **JSON**.
- **Framework Web**: **Django**.
- **Diseño y Estilos**: **Bootstrap 5 local** (ubicado en `static/css/` y `static/js/`), sin dependencias externas por CDN.
- **Herencia de plantillas**: Estructura centralizada en `templates/base.html` con bloques reutilizables (`{% block content %}`, etc.).
- **Archivos estáticos**: Imágenes y recursos multimedia servidos localmente mediante `{% load static %}`.
- **Enrutamiento modular**: Cada aplicación gestiona sus propias rutas en su respectivo `urls.py`, enlazadas desde `config/urls.py` mediante `include()`.

---

## 2. Arquitectura Modular del Proyecto (4 Aplicaciones)

El equipo de desarrollo dividió las responsabilidades en 4 aplicaciones Django:

| Aplicación | Responsabilidad Principal |
|---|---|
| **`cuentas`** | Gestión de acceso, login, registro y recuperación de contraseñas de usuarios. |
| **`organizacion`** | Núcleo operativo: registro diario de actividades por funcionario y validación de evidencias por parte de coordinación. |
| **`agenda`** | Registro y seguimiento de compromisos ciudadanos futuros agrupados por estados (tipo Kanban). |
| **`indicadores`** | Tableros de avance, cumplimiento porcentual ponderado y cálculo de semáforo de desempeño. |

---

## 3. Módulo `organizacion` (Especificación Detallada)

### 3.1 Responsabilidad
Permite al funcionario ingresar sus actividades diarias vinculadas a los ítems de su cargo con su respectivo respaldo de evidencia. Asimismo, permite a la coordinación revisar, aprobar o rechazar dichas evidencias con observaciones.

### 3.2 Rutas y Vistas Planificadas
Ruta base del módulo: `/organizacion/`

| Ruta | Vista (`views.py`) | Nombre de Ruta (`name`) | Template Asociado | Descripción |
|---|---|---|---|---|
| `panel/` | `panel_admin(request)` | `panel_admin` | `organizacion/panel_admin.html` | Consolidado general de todas las actividades con filtros por delegación y estado. |
| `mis-actividades/` | `panel_funcionario(request)` | `panel_funcionario` | `organizacion/panel_funcionario.html` | Vista personal que lista únicamente las actividades del funcionario actual. |
| `registrar/` | `registrar_actividad(request)` | `registrar_actividad` | `organizacion/registrar_actividad.html` | Formulario para ingresar nueva actividad y generar su código de evidencia. |
| `validar/<int:id>/` | `validar_evidencia(request, id)` | `validar_evidencia` | `organizacion/validar_evidencia.html` | Interfaz de coordinación para aprobar o rechazar la evidencia con comentarios. |

### 3.3 Estructura de Datos (`data/actividades.json`)
La información de actividades se almacena en el archivo `data/actividades.json` con el siguiente esquema:

```json
[
  {
    "id": 1,
    "fecha": "2026-09-01",
    "funcionario": "Elizabeth Villanueva",
    "delegacion": "La Antena",
    "item": "Atención de usuario",
    "descripcion": "Atención presencial a ciudadana por orientación en subsidio habitacional DS49.",
    "accion": "Orientación técnica y derivación interna a oficina de vivienda.",
    "contacto": "Marta Gómez Castillo",
    "telefono": "+56987654321",
    "evidencia": {
      "codigo": "EVI-ANT-001",
      "archivo": "img/evidencias/evidencia_01.svg",
      "estado": "Aprobado",
      "observacion": "Atención registrada correctamente con ficha y derivación.",
      "fecha_validacion": "2026-09-02",
      "verificador": "Alan Von Kretschmann"
    }
  }
]
```

---

## 4. Instalación y Ejecución Local

### 4.1 Requisitos Previos
- Python 3.10 o superior.

### 4.2 Pasos de Puesta en Marcha

1. **Activar el entorno virtual**:
   - En Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - O en Command Prompt (cmd):
     ```cmd
     .\venv\Scripts\activate.bat
     ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

4. **Acceder a la aplicación**:
   - Página de inicio (Landing): `http://127.0.0.1:8000/`
   - Módulo Organización: `http://127.0.0.1:8000/organizacion/panel/`
   - Módulo Indicadores: `http://127.0.0.1:8000/indicadores/progreso/`

---

## 5. Estructura de Directorios del Proyecto

```text
proyecto_django/
├── config/                  # Configuración principal del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── data/                    # Almacenamiento de datos en JSON (sin BD)
│   └── actividades.json
├── static/                  # Archivos estáticos locales
│   ├── css/                 # Bootstrap CSS local
│   ├── js/                  # Bootstrap JS local
│   └── img/                 # Imágenes y evidencias locales
│       └── evidencias/
├── templates/               # Plantillas HTML
│   ├── base.html            # Plantilla base compartida (Herencia)
│   ├── landing.html         # Página de presentación
│   ├── organizacion/        # Vistas de la app organización
│   └── indicadores/         # Vistas de la app indicadores
├── agenda/                  # App Django: Agenda colectiva
├── cuentas/                 # App Django: Autenticación y usuarios
├── indicadores/             # App Django: Métricas y semáforos
├── organizacion/            # App Django: Registro y validación de actividades
├── manage.py
├── requirements.txt
└── README.md
```
