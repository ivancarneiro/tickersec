<!--
Sync Impact Report:
Version change: 1.0.0 -> 1.1.0
List of modified principles: None -> Updated Technical Constraints
Added sections: None
Templates updated: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
-->
# TickerSec Constitution

## Core Principles

### I. Gestión Centralizada de Entorno y Paquetes con uv
Todas las dependencias de Python y la gestión del entorno virtual del proyecto DEBEN ser administradas de forma centralizada con la herramienta `uv`. No se deben utilizar entornos virtuales estándar creados con `venv` de manera aislada ni archivos `requirements.txt` desactualizados como origen de verdad. El archivo `pyproject.toml` (o el esquema de bloqueo de dependencias de `uv`) actuará como la fuente única de verdad para las dependencias del proyecto.
*Rationale*: Centralizar con `uv` garantiza instalaciones ultrarrápidas, repetibles, consistencia entre entornos locales y de producción, y elimina los conflictos típicos de dependencias en Django.

### II. Arquitectura Limpia y Desacoplada (core y dash)
El proyecto debe mantener una estricta separación de responsabilidades entre sus dos aplicaciones Django: `core` (responsable de la lógica de negocio, modelos de base de datos de tickets, auditorías y CRUD) y `dash` (responsable de la autenticación, vistas del panel y visualizaciones analíticas basadas en Plotly y Polars). Ninguna lógica de renderizado gráfico de `dash` debe inyectarse en los modelos o vistas del `core`.
*Rationale*: Mantener este desacoplamiento previene la acumulación de deuda técnica y permite evolucionar el motor de visualización (gráficos) de forma independiente del núcleo transaccional.

### III. Configuración basada en el Entorno con python-decouple
Toda la configuración del sistema que sea sensible (como llaves secretas, contraseñas, URLs de base de datos) o que dependa del entorno (como el modo `DEBUG` o el tipo de base de datos activa) DEBE ser gestionada mediante variables de entorno en un archivo `.env` local, consumidas a través de `python-decouple`. Ninguna credencial o configuración de entorno debe ser estática en `settings.py`.
*Rationale*: Garantiza la seguridad y facilita la portabilidad de la aplicación entre desarrollo (con SQLite) y producción (con PostgreSQL).

### IV. Base de Datos según el Entorno de Ejecución
El proyecto utilizará SQLite (`db.sqlite3`) como base de datos por defecto para el desarrollo local ágil y pruebas, y PostgreSQL (a través del adaptador `psycopg2-binary`) para el entorno de producción. Ambas configuraciones deben estar listas y ser conmutables a través del archivo `.env`.
*Rationale*: Permite un inicio de desarrollo rápido sin dependencias pesadas locales, mientras mantiene la compatibilidad con un entorno de producción robusto.

### V. Flujo de Trabajo Basado en Especificaciones (Spec-Driven Development)
Ninguna refactorización crítica o desarrollo de nuevas funcionalidades puede implementarse sin antes seguir el flujo de Spec-kit:
1. Definir los requerimientos funcionales y escenarios de usuario en una especificación clara (`spec.md`).
2. Diseñar la implementación técnica detallada en un plan de implementación (`plan.md`).
3. Estructurar las tareas secuenciales en una lista ordenada (`tasks.md`).
*Rationale*: Evita la codificación por intuición ("vibe coding"), asegurando que el diseño de software sea predecible, testeable y alineado a los requerimientos.

## Technical Constraints

- **Python**: Versión >= 3.10.
- **Django**: Versión 5.0.11 o posterior (última versión estable).
- **Visualización**: Plotly 5.24.1 + Polars (última versión estable).
- **Editor**: django-quill-editor 0.1.40 o posterior.
- **Gestión de Git**: Las ramas deben crearse siguiendo la convención de Spec-kit y conventional commits. Se utilizará la herramienta CLI `gh` de GitHub configurada con la cuenta `ivancarneiro` para gestionar pull requests y sincronización del repositorio.

## Development Workflow

1. **Especificar**: Se crea o actualiza el archivo `spec.md` para la funcionalidad.
2. **Planificar**: Se redacta `plan.md` resolviendo dudas de arquitectura e impacto en base de datos.
3. **Validar**: Se evalúa que el plan respeete los principios de esta Constitución.
4. **Implementar**: Se ejecutan las tareas paso a paso, asegurando que el entorno y dependencias sigan bajo el control estricto de `uv`.

## Governance

Toda modificación a esta Constitución o adición de principios debe ser documentada como un incremento de versión semántica de la gobernanza del proyecto. Los cambios mayores (como la remoción de un principio principal) requieren justificación explícita y una actualización de las plantillas dependientes bajo la carpeta `.specify/templates/`.

**Version**: 1.1.0 | **Ratified**: 2026-07-13 | **Last Amended**: 2026-07-13
