# Mezcla Django (proyecto_django-main) + Diseño Figma (módulo Delegaciones)

## Qué se hizo

- **Se mantiene intacto** todo lo que ya tenías funcionando:
  - `config/` (settings, urls, wsgi/asgi) — sin cambios de fondo, solo se agregó una línea en `config/urls.py` para incluir las rutas de `organizacion`.
  - `cuentas/` y `agenda/` — intactas (seguían siendo apps vacías, no había nada que perder).
  - `indicadores/` — su vista, urls y `datosarray.py` **no se tocaron**. Solo se actualizó `templates/indicadores/dashboard.html` para que herede de la nueva base compartida (`organizacion/base_app.html`), tal como decía el comentario `TODO` que ya estaba en ese archivo. El contenido y la lógica del dashboard son exactamente los mismos.
  - `templates/landing.html` — intacta, solo se reemplazaron los dos botones "Ingresar" (que apuntaban a `#`) para que lleven al listado real de delegaciones.
  - `requirements.txt`, `datosarray.py`, `importante.txt`, `db.sqlite3` — sin cambios.

- **Se implementó de verdad** la app `organizacion` (antes estaba vacía):
  - `models.py`: `Delegacion`, `Cargo`, `Funcionario` (los campos que pedía el diseño de Figma: nombre, ámbito, estado, cargo, es_verificador, etc.).
  - `forms.py`: formulario de delegación con la misma validación que tenía el diseño (nombre obligatorio, mínimo 4 caracteres).
  - `views.py`: listado con búsqueda + filtro de estado + paginación, crear, editar, detalle (con funcionarios asociados) y activar/desactivar.
  - `urls.py`, `admin.py`: rutas y registro en el panel de administración.
  - Templates: `base_app.html` (navbar con los mismos menús Organización / Actividad / Medición del diseño de Figma), `delegacion_list.html`, `delegacion_form.html`, `delegacion_detail.html` — replican las 5 pantallas del diseño de Figma (listado, crear, editar, detalle, modal de desactivación) usando Bootstrap 5 (ya incluido en `static/`).

## Colores: se usó la paleta del proyecto Django, no la de Figma

El diseño de Figma usaba azul marino (`#14213D`). Como pediste, se reemplazó por la paleta institucional que ya definía `landing.html`:

| Uso | Color Figma (original) | Color usado aquí (de tu proyecto) |
|---|---|---|
| Color primario / navbar | `#14213D` (navy) | `#7A1B1E` (granate) |
| Hover primario | `#1a2d54` | `#591314` (granate oscuro) |
| Fondo de página | `#f9fafb` (gray50) | `#F6F2EA` (crema) |
| Texto principal | `#111827` | `#1F2A33` (tinta) |
| Texto secundario | `#6b7280` | `#4A5560` (tinta suave) |
| Bordes | `#e5e7eb` | `#E2DACB` (línea) |
| Acento secundario (verificador) | azul claro | `#0E5C68` (azul costero) |

También se reutilizó la tipografía de `landing.html` (Fraunces para títulos, Inter para el resto) para mantener una sola identidad visual entre la página pública y el sistema interno.

## Lo que falta para que "Funcionarios", "Actividades", "Agenda colectiva" y "Períodos" funcionen

Esos ítems del menú están **deshabilitados intencionalmente** (marcados "(próximamente)") porque `agenda` y `cuentas` siguen siendo apps vacías — no se inventó lógica ni datos falsos ahí. Cuando quieras, seguimos con esos módulos usando el mismo patrón que ya se usó para `organizacion`.

## Cómo correrlo

```bash
cd proyecto_django-main
python -m venv venv
source venv/bin/activate      # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations organizacion
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Rutas para probar:
- `http://127.0.0.1:8000/` → landing pública (sin cambios de contenido, solo el botón "Ingresar" ahora funciona)
- `http://127.0.0.1:8000/organizacion/delegaciones/` → listado de delegaciones (diseño de Figma)
- `http://127.0.0.1:8000/indicadores/progreso/` → dashboard que ya tenías, ahora con el navbar compartido
- `http://127.0.0.1:8000/admin/` → panel admin, para cargar Cargos, Delegaciones y Funcionarios de prueba

Nota: crea primero uno o más `Cargo` desde el admin antes de crear `Funcionario`, ya que `Funcionario.cargo` es obligatorio.
