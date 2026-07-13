# Implementation Plan: migrate-polars

**Branch**: `refactor/migrate-polars` | **Date**: 2026-07-13 | **Spec**: [spec.md](spec.md)

## Summary

Migración de la lógica analítica y visualizaciones desde Pandas a Polars, y actualización de todas las dependencias del proyecto a sus últimas versiones estables compatibles. Esto implica modificar las consultas y agrupaciones en `dash/graficos.py` para consumir APIs de Polars, actualizar `pyproject.toml` y regenerar el archivo `uv.lock`.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**:
- `django` (última versión estable)
- `python-decouple` (última versión estable)
- `psycopg2-binary` (última versión estable)
- `pillow` (última versión estable)
- `django-bootstrap5` (última versión estable)
- `django-quill-editor` (última versión estable)
- `polars` (última versión estable)
- `plotly` (última versión estable)

**Storage**: SQLite (`db.sqlite3` en dev) y PostgreSQL en producción.

**Testing**: Django TestCase ejecutado mediante `uv run python manage.py test`.

**Target Platform**: Linux / macOS / Windows.

**Project Type**: Django Web Application.

**Performance Goals**: Tiempos de renderizado y procesamiento de datos inferiores a 1 segundo para el dashboard analítico.

**Constraints**: Ninguna dependencia de Pandas permitida en el entorno.

**Scale/Scope**: Refactorización del módulo `dash` y actualización de dependencias de todo el proyecto.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principio I: Gestión con uv**: ✅ PASSED. La actualización y exclusión de Pandas se orquesta mediante `pyproject.toml` y `uv sync`.
- **Principio II: Desacoplamiento (core/dash)**: ✅ PASSED. Los cambios en los DataFrames se limitan al módulo `dash/graficos.py`, respetando la separación.
- **Principio III: python-decouple**: ✅ PASSED. Se mantiene la lectura de configuraciones de entorno.
- **Principio IV: Base de datos según entorno**: ✅ PASSED. Polars consumirá los conjuntos de datos recuperados por el ORM de Django de forma transparente para SQLite y PostgreSQL.
- **Principio V: Spec-Driven Development**: ✅ PASSED. Cumplido mediante el diseño estructurado en este directorio de especificaciones.

## Project Structure

### Documentation (this feature)

```text
specs/002-migrate-polars/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (sin cambios en base de datos)
└── quickstart.md        # Phase 1 output
```

### Source Code (repository root)

```text
.
├── dash/
│   └── graficos.py      # Refactorizado de Pandas a Polars
├── pyproject.toml       # Dependencias actualizadas y Polars añadido (Pandas removido)
├── uv.lock              # Bloqueo de dependencias de uv actualizado
└── requirements.txt     # Regenerado para retrocompatibilidad
```

**Structure Decision**: El proyecto sigue la misma estructura Django. Se modifica únicamente la sección de dependencias en la raíz y la lógica del script de gráficos en `dash/`.

## Complexity Tracking

*(No hay violaciones a la Constitución que requieran justificación)*
