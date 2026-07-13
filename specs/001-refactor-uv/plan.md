# Implementation Plan: refactor-uv

**Branch**: `001-refactor-uv` | **Date**: 2026-07-13 | **Spec**: [spec.md](spec.md)

## Summary

Refactorización y centralización de la gestión del entorno y dependencias del proyecto `tickersec` utilizando `uv`. Esto incluye declarar todas las dependencias requeridas por Django, Plotly y Pandas en un archivo `pyproject.toml` estándar y generar un archivo de bloqueo determinista `uv.lock`.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**: 
- `django==5.0.11`
- `python-decouple==3.8`
- `psycopg2-binary==2.9.9`
- `pillow==10.4.0`
- `django-bootstrap5==24.2`
- `django-quill-editor==0.1.40`
- `pandas`
- `plotly==5.24.1`

**Storage**: SQLite (`db.sqlite3` en local/dev) y PostgreSQL en producción.

**Testing**: Django TestCase ejecutado mediante `uv run python manage.py test`.

**Target Platform**: Linux / macOS / Windows (con soporte nativo para `uv`).

**Project Type**: Django Web Application.

**Performance Goals**: Inicialización rápida y sincronización de dependencias en menos de 20 segundos.

**Constraints**: Aislamiento estricto de dependencias en el directorio local `.venv/` en la raíz.

**Scale/Scope**: Ámbito global del proyecto TickerSec (entornos de desarrollo y dependencias locales).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principio I: Gestión con uv**: ✅ PASSED. La centralización de paquetes y del entorno virtual se realiza mediante `pyproject.toml` y `uv.lock`.
- **Principio II: Desacoplamiento (core/dash)**: ✅ PASSED. La refactorización del entorno no altera ni introduce acoplamientos entre `core` y `dash`.
- **Principio III: python-decouple**: ✅ PASSED. Las configuraciones sensibles y del entorno siguen leyéndose mediante `.env` y `python-decouple`.
- **Principio IV: Base de datos según entorno**: ✅ PASSED. El entorno de `uv` provee soporte para `psycopg2-binary` (PostgreSQL) y SQLite de forma compatible.
- **Principio V: Spec-Driven Development**: ✅ PASSED. Esta refactorización se está planificando y estructurando siguiendo el flujo de Spec-kit.

## Project Structure

### Documentation (this feature)

```text
specs/001-refactor-uv/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (empty/no db changes)
└── quickstart.md        # Phase 1 output
```

### Source Code (repository root)

```text
.
├── .venv/               # Entorno virtual de uv (creado localmente)
├── core/                # Django core app
├── dash/                # Django dashboard app
├── tickersec/           # Django configuration folder
├── pyproject.toml       # Especificación de dependencias uv
├── uv.lock              # Archivo de bloqueo determinista uv
├── manage.py            # Entrypoint Django
├── populatedb.py        # Script de prueba para base de datos
└── requirements.txt     # (Mantener sincronizado o depreciar)
```

**Structure Decision**: El proyecto mantiene su arquitectura monolítica de Django de dos aplicaciones (`core` y `dash`). `pyproject.toml` y `uv.lock` se ubicarán en la raíz para orquestar la ejecución.

## Complexity Tracking

*(No hay violaciones a la Constitución que requieran justificación)*
