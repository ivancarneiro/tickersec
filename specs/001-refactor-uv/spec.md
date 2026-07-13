# Feature Specification: refactor-uv

**Feature Branch**: `001-refactor-uv`

**Created**: 2026-07-13

**Status**: Draft

**Input**: User description: "Refactorizar el proyecto bajo la librería uv para centralizar paquetes, entornos virtuales, etc. Manejo de github (ivancarneiro) mediante gh CLI."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Inicialización y Sincronización de Entorno Limpio con uv (Priority: P1)

Como desarrollador del proyecto TickerSec, quiero clonar el repositorio e inicializar un entorno de desarrollo completamente aislado y reproducible en un solo paso mediante `uv`, de forma que pueda comenzar a programar de inmediato sin configurar entornos virtuales manualmente.

**Why this priority**: Es la base de la tarea de centralización. Permite establecer las bases del entorno para que cualquier otra persona o herramienta pueda trabajar con las dependencias correctas sin fricciones.

**Independent Test**: Eliminar cualquier carpeta `.venv` o entorno virtual previo, y correr `uv sync` en la raíz del proyecto. El comando debe completar con éxito, crear el directorio `.venv` local e instalar todas las dependencias necesarias.

**Acceptance Scenarios**:

1. **Given** que el proyecto está en un directorio limpio y no tiene entorno virtual (`.venv`), **When** ejecuto `uv sync`, **Then** se debe crear la carpeta `.venv` y se deben instalar exactamente las versiones de paquetes declaradas.
2. **Given** un entorno recién sincronizado con `uv`, **When** ejecuto `uv run python manage.py check`, **Then** Django debe inicializarse correctamente, realizar los chequeos del sistema y retornar éxito sin que falte ningún paquete importado.

---

### User Story 2 - Centralización de Dependencias en pyproject.toml (Priority: P2)

Como desarrollador del proyecto TickerSec, quiero que todas las dependencias del proyecto y la configuración del entorno estén declaradas formalmente en un archivo `pyproject.toml` estándar de Python, dejando atrás el archivo plano `requirements.txt` como la única fuente de verdad desestructurada.

**Why this priority**: Proporciona estructura al proyecto acorde con las mejores prácticas modernas de Python, permitiendo a `uv` gestionar y bloquear las dependencias de manera determinista.

**Independent Test**: Validar que la edición de dependencias se realice a través de comandos como `uv add` o modificando el archivo `pyproject.toml`, y verificar que el archivo `uv.lock` registre la estructura exacta del árbol de dependencias.

**Acceptance Scenarios**:

1. **Given** el archivo `pyproject.toml` configurado, **When** ejecuto `uv sync`, **Then** las dependencias directas (`django`, `plotly`, `pandas`, etc.) y sus dependencias transitivas deben resolverse y bloquearse de forma consistente en un archivo `uv.lock`.
2. **Given** la necesidad de dar soporte a pipelines de despliegue legados, **When** ejecuto un comando de exportación de `uv` (como `uv pip compile`), **Then** se debe poder generar un `requirements.txt` compatible de forma automática a partir del `pyproject.toml`.

---

### User Story 3 - Integración del Flujo de Trabajo en GitHub con la cuenta ivancarneiro (Priority: P2)

Como mantenedor del proyecto TickerSec, quiero utilizar la herramienta `gh` CLI configurada localmente para crear la rama del feature `001-refactor-uv`, hacer commits y subir cambios como pull request a GitHub bajo la identidad de `ivancarneiro`.

**Why this priority**: Asegura que el flujo de trabajo de Spec-kit mantenga la trazabilidad y se integre de forma nativa con GitHub desde la línea de comandos, respetando los permisos de usuario establecidos.

**Independent Test**: Ejecutar comandos de Git y `gh pr create` usando la identidad configurada y validar que el repositorio remoto reciba las actualizaciones en la rama correspondiente.

**Acceptance Scenarios**:

1. **Given** que las modificaciones locales están listas y validadas, **When** ejecuto el flujo de Git para la rama `001-refactor-uv`, **Then** la rama remota debe crearse en GitHub bajo el usuario `ivancarneiro`.
2. **Given** la rama publicada, **When** ejecuto `gh pr create` (o similar), **Then** se debe abrir un pull request en el repositorio correspondiente sin errores de permisos.

## Edge Cases

- **Incompatibilidad de dependencias**: Qué pasa cuando versiones específicas de Pandas o Plotly colisionan con Django 5.0.11 al resolver dependencias bajo el modo estricto de `uv`. El resolutor de `uv` debe encontrar un árbol compatible o reportar claramente el conflicto.
- **Entorno virtual preexistente**: Cómo maneja `uv sync` si ya existe un entorno virtual creado por otra herramienta. `uv` debe limpiar y sobreescribir el `.venv` para asegurar que las dependencias estén sincronizadas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El proyecto MUST utilizar un archivo `pyproject.toml` para definir la configuración y dependencias en la raíz del proyecto.
- **FR-002**: Las dependencias de producción declaradas MUST incluir de forma exacta:
  - `django==5.0.11`
  - `python-decouple==3.8`
  - `psycopg2-binary==2.9.9`
  - `pillow==10.4.0`
  - `django-bootstrap5==24.2`
  - `django-quill-editor==0.1.40`
  - `pandas` (versión compatible con python 3.10+)
  - `plotly==5.24.1`
- **FR-003**: El entorno virtual de Python MUST estar alojado localmente en la carpeta `.venv` en la raíz del proyecto.
- **FR-004**: Todas las llamadas a scripts del proyecto, incluyendo `manage.py` y `populatedb.py`, MUST ejecutarse a través de `uv run` para garantizar el aislamiento (ej. `uv run python manage.py runserver`).
- **FR-005**: El archivo `requirements.txt` actual MUST sincronizarse inicialmente con el `pyproject.toml` y luego mantenerse sincronizado o eliminarse de acuerdo al plan de despliegue.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La inicialización del entorno (desde un directorio limpio hasta la creación del `.venv` e instalación de dependencias) mediante `uv sync` debe completarse en menos de 20 segundos en la máquina local.
- **SC-002**: Ninguna dependencia requerida para ejecutar Django o los gráficos de Plotly debe quedar instalada en el entorno global del sistema de Python.
- **SC-003**: El comando `uv run python manage.py migrate` se ejecuta y conecta correctamente a la base de datos (SQLite en dev) aplicando las migraciones del core en menos de 5 segundos.
