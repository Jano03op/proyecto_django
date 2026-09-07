# Sistema de Gestión de Resultados (SGR) — Delegaciones Municipales

Este proyecto corresponde a la **Evaluación Sumativa #1** de la asignatura **Programación Back End (TI3041)** en **INACAP La Serena**.

El sistema tiene como propósito centralizar el registro, verificación, seguimiento y medición de la gestión operativa de los funcionarios y las delegaciones de la Ilustre Municipalidad de La Serena.

---

## 1. Restricciones y Lineamientos Técnicos de la Evaluación

- **Persistencia sin base de datos relacional**: Toda la información del dominio operativo se almacena y consulta de forma centralizada en colecciones en memoria mediante el archivo **`datosarray.py`**.
- **Framework Web**: **Django 6.1**.
- **Diseño y Estilos**: **Bootstrap 5 local** (ubicado en `static/css/` y `static/js/`), sin dependencias externas por CDN, con paleta institucional serenense (granate y azul costero).
- **Herencia de plantillas**: Estructura centralizada en `templates/base.html` con bloques reutilizables (`{% block content %}`, etc.).
- **Archivos estáticos**: Recursos multimedia servidos localmente mediante `{% load static %}`.
- **Enrutamiento modular**: Cada aplicación gestiona sus propias rutas en su respectivo `urls.py`, enlazadas desde `config/urls.py` mediante `include()`.
- **Internacionalización**: Configuración localizada para Chile (`LANGUAGE_CODE = 'es-cl'` y `TIME_ZONE = 'America/Santiago'`).

---

## 2. Arquitectura Modular del Proyecto (4 Aplicaciones)

El equipo de desarrollo dividió las responsabilidades en 4 aplicaciones Django desacopladas mediante capas de servicios:

| Aplicación | Capa de Servicio | Responsabilidad Principal |
|---|---|---|
| **`cuentas`** | `cuentas/services.py` | Gestión de acceso, autenticación de funcionarios, roles y perfiles desde `usuarios`. |
| **`organizacion`** | `organizacion/services.py` | Núcleo operativo: registro de actividades, validación de evidencias y filtros territoriales. |
| **`agenda`** | `agenda/services.py` | Registro y seguimiento de compromisos ciudadanos agrupados por estados (Tablero Kanban). |
| **`indicadores`** | `indicadores/views.py` | Tableros de avance, cumplimiento porcentual ponderado y cálculo de semáforo de desempeño. |

---

## 3. Módulo `organizacion` (Especificación Detallada)

### 3.1 Responsabilidad
Permite al funcionario ingresar sus actividades diarias vinculadas a los ítems de su cargo con su respectivo respaldo de evidencia (`EVI-XXX-00X`). Asimismo, permite a la coordinación revisar, aprobar o rechazar dichas evidencias con observaciones formales.

### 3.2 Rutas y Vistas Planificadas
Ruta base del módulo: `/organizacion/`

| Ruta | Vista (`views.py`) | Nombre de Ruta (`name`) | Template Asociado | Descripción |
|---|---|---|---|---|
| `panel/` | `panel_admin(request)` | `panel_admin` | `organizacion/panel_admin.html` | Consolidado general de todas las actividades con filtros por delegación y estado. |
| `mis-actividades/` | `panel_funcionario(request)` | `panel_funcionario` | `organizacion/panel_funcionario.html` | Vista personal que lista únicamente las actividades del funcionario actual. |
| `registrar/` | `registrar_actividad(request)` | `registrar_actividad` | `organizacion/registrar_actividad.html` | Formulario con selector de fecha `DD/MM/AAAA` y generación automática de código de evidencia. |
| `validar/<int:id>/` | `validar_evidencia(request, id)` | `validar_evidencia` | `organizacion/validar_evidencia.html` | Interfaz de coordinación para aprobar o rechazar la evidencia con comentarios. |

### 3.3 Estructura de Datos (`datosarray.py`)
Toda la información se centraliza en `datosarray.py` evitando conflictos entre aplicaciones:
- **`periodo`**: Rango de fechas del ciclo de evaluación municipal.
- **`personas`**: Lista de funcionarios, sus metas por ítem, avances y ponderadores.
- **`actividades`**: Registros operativos con códigos de evidencia, observaciones y estados (`Pendiente`, `Aprobado`, `Rechazado`).
- **`compromisos`**: Base para el tablero Kanban de la app `agenda`.
- **`usuarios`**: Base de credenciales y roles para la app `cuentas`.

```python
actividades = [
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

### 3.4 Identidad Visual y Colores de Delegaciones
Para facilitar la lectura rápida en el consolidado general, cada delegación cuenta con una identificación cromática accesible con punto indicador:

| Delegación | Tonalidad Representativa | Clase CSS (`slugify`) |
|---|---|---|
| **Avenida del Mar** | Azul Océano / Costero | `.badge-delegacion-avenida-del-mar` |
| **Centro** | Granate Colonial Serenense | `.badge-delegacion-centro` |
| **La Antena** | Terracota / Ámbar Cálido | `.badge-delegacion-la-antena` |
| **Las Compañías** | Índigo Profundo / Comunitario | `.badge-delegacion-las-companias` |
| **La Pampa** | Verde Valle / Social | `.badge-delegacion-la-pampa` |
| **Rural** | Dorado Tierra / Conectividad | `.badge-delegacion-rural` |

---

## 4. Instalación, Ejecución y Pruebas

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

3. **Ejecutar migraciones internas de Django (auth/sesiones)**:
   ```bash
   python manage.py migrate
   ```

4. **Ejecutar la suite de pruebas**:
   ```bash
   python manage.py test
   ```
   *(18 tests unitarios cubriendo `organizacion`, `agenda` y `cuentas`)*.

5. **Ejecutar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

6. **Acceder a la aplicación**:
   - Landing Page (con acceso directo): `http://127.0.0.1:8000/`
   - Módulo Organización (Consolidado): `http://127.0.0.1:8000/organizacion/panel/`
   - Mis Actividades (Funcionario): `http://127.0.0.1:8000/organizacion/mis-actividades/`
   - Formulario de Registro: `http://127.0.0.1:8000/organizacion/registrar/`
   - Módulo Indicadores: `http://127.0.0.1:8000/indicadores/progreso/`

---

## 5. Estructura de Directorios del Proyecto

```text
proyecto_django/
├── config/                  # Configuración principal del proyecto Django
│   ├── settings.py          # Settings, i18n (es-cl), apps y plantillas
│   ├── urls.py              # Router central con include() y landing
│   └── wsgi.py
├── datosarray.py            # Fuente centralizada de datos en memoria
├── static/                  # Recursos estáticos locales
│   ├── css/                 # Bootstrap CSS local
│   ├── js/                  # Bootstrap JS local
│   └── img/                 # Imágenes y evidencias locales
│       └── evidencias/
├── templates/               # Plantillas HTML con diseño municipal
│   ├── base.html            # Plantilla base compartida y diseño global
│   ├── landing.html         # Página de presentación con acceso al módulo
│   ├── organizacion/        # Vistas de la app organización
│   │   ├── panel_admin.html
│   │   ├── panel_funcionario.html
│   │   ├── registrar_actividad.html
│   │   └── validar_evidencia.html
│   └── indicadores/         # Vistas de la app indicadores
├── agenda/                  # App Django: Agenda y Tablero Kanban
│   ├── services.py          # Servicios para compromisos y estados
│   ├── tests.py
│   └── views.py
├── cuentas/                 # App Django: Autenticación y usuarios
│   ├── services.py          # Servicios de acceso y perfiles
│   ├── tests.py
│   └── views.py
├── indicadores/             # App Django: Métricas y semáforos
│   └── views.py
├── organizacion/            # App Django: Registro y validación operativa
│   ├── services.py          # Capa de lógica y persistencia en datosarray
│   ├── urls.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```
