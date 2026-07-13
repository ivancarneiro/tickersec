# Tasks: refactor-uv

**Input**: Design documents from `/specs/001-refactor-uv/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Organization**: Las tareas están agrupadas por fases y por historias de usuario para permitir el desarrollo incremental y la verificación independiente de cada hito.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede correr en paralelo (archivos distintos, sin dependencias mutuas).
- **[Story]**: Identificador de la historia de usuario a la que pertenece (ej. US1, US2, US3).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicialización del archivo de configuración del proyecto con `uv`.

- [ ] T001 Crear el archivo de configuración `/home/ciex/PROYECTOS/tickersec/pyproject.toml` en la raíz.
- [ ] T002 Configurar los metadatos y las dependencias iniciales (`django==5.0.11`, `python-decouple==3.8`) en el archivo `/home/ciex/PROYECTOS/tickersec/pyproject.toml`.
- [ ] T003 [P] Configurar las exclusiones de Git en `/home/ciex/PROYECTOS/tickersec/.gitignore` para omitir el directorio `.venv/` de uv.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Completar la declaración e instalación de todos los paquetes de soporte del proyecto.

**⚠️ CRITICAL**: Ningún trabajo de las historias de usuario puede comenzar hasta que este paso se complete con éxito.

- [ ] T004 Agregar dependencias adicionales del sistema Django (`psycopg2-binary==2.9.9`, `pillow==10.4.0`, `django-bootstrap5==24.2`, `django-quill-editor==0.1.40`) en `/home/ciex/PROYECTOS/tickersec/pyproject.toml`.
- [ ] T005 [P] Agregar dependencias de analítica (`pandas`, `plotly==5.24.1`) en `/home/ciex/PROYECTOS/tickersec/pyproject.toml`.
- [ ] T006 Ejecutar el comando `uv sync` en la raíz del proyecto para generar la carpeta de entorno `.venv/` y el archivo de bloqueo `uv.lock`.

**Checkpoint**: La base del entorno virtual está lista para probar la ejecución aislada de las historias de usuario.

---

## Phase 3: User Story 1 - Sincronización e Inicialización del Entorno (Priority: P1) 🎯 MVP

**Goal**: Permitir a cualquier desarrollador sincronizar y probar la aplicación de forma aislada en un solo comando rápido.

**Independent Test**: Eliminar el `.venv` e instalar todo de nuevo con `uv sync`. Verificar el correcto chequeo de Django.

### Implementation for User Story 1

- [ ] T007 [US1] Validar la sincronización del entorno ejecutando el chequeo de Django vía `uv run python manage.py check`.
- [ ] T008 [US1] Aplicar las migraciones de la base de datos local SQLite mediante `uv run python manage.py migrate`.
- [ ] T009 [US1] Poblar la base de datos de desarrollo mediante `uv run python populatedb.py` y comprobar que no hay errores de inserción.

**Checkpoint**: A partir de este momento, la aplicación es completamente ejecutable y testeable de forma independiente bajo `uv`.

---

## Phase 4: User Story 2 - Centralización de Dependencias (Priority: P2)

**Goal**: Garantizar la consistencia de dependencias y la compatibilidad con entornos legados.

**Independent Test**: Verificar la exportación de dependencias de `pyproject.toml` a un `requirements.txt` alternativo.

### Implementation for User Story 2

- [ ] T010 [US2] Probar la generación del archivo de dependencias compiladas usando `uv pip compile pyproject.toml -o requirements.txt` para asegurar la retrocompatibilidad.
- [ ] T011 [US2] Sobreescribir el archivo de requerimientos original `/home/ciex/PROYECTOS/tickersec/requirements.txt` con la versión exportada por `uv`.

---

## Phase 5: User Story 3 - Integración del Flujo de Trabajo en GitHub (Priority: P2)

**Goal**: Utilizar `gh` CLI y Git bajo la identidad de `ivancarneiro` para realizar pull requests y commits del feature.

**Independent Test**: Ejecutar comandos de Git y `gh` para proponer y registrar los cambios en la rama.

### Implementation for User Story 3

- [ ] T012 [US3] Crear e inicializar la rama local del feature ejecutando `git checkout -b 001-refactor-uv`.
- [ ] T013 [US3] Realizar el seguimiento de cambios mediante commits de Git y abrir el Pull Request a GitHub usando `gh pr create` (vinculado a `ivancarneiro`).

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Mejoras finales en documentación y validación de ejecución.

- [ ] T014 Actualizar la documentación de inicio y despliegue en `/home/ciex/PROYECTOS/tickersec/README.md` detallando el uso de `uv sync` y `uv run`.
- [ ] T015 Eliminar carpetas temporales de compilación o rastros de entornos virtuales anteriores obsoletos.
- [ ] T016 Levantar y validar localmente el servidor de desarrollo ejecutando `uv run python manage.py runserver` y conectando el navegador.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias. Comienza de inmediato.
- **Foundational (Phase 2)**: Depende de Setup (Phase 1). Bloquea la implementación de las historias de usuario.
- **User Stories (Phases 3+)**: Dependen de la finalización de Foundational (Phase 2). Se ejecutan secuencialmente según la prioridad (P1 -> P2).
- **Polish (Final Phase)**: Se ejecuta una vez que todas las historias de usuario han sido completadas e integradas.
