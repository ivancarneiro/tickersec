# Tasks: migrate-polars

**Input**: Design documents from `/specs/002-migrate-polars/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Organization**: Las tareas están agrupadas por fases y asociadas a las historias de usuario correspondientes para permitir un flujo de trabajo ordenado y modular.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo.
- **[Story]**: Identificador de la historia de usuario a la que pertenece la tarea (ej. US1, US2, US3).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configuración del archivo de dependencias del proyecto.

- [ ] T001 Actualizar el archivo `/home/ciex/PROYECTOS/tickersec/pyproject.toml` removiendo `pandas` y agregando la librería `polars`.
- [ ] T002 Actualizar las demás dependencias en `/home/ciex/PROYECTOS/tickersec/pyproject.toml` removiendo las restricciones de versión fijas estrictas obsoletas para permitir resolver las últimas versiones estables compatibles.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Asegurar la consistencia del nuevo árbol de dependencias e instalación del entorno.

**⚠️ CRITICAL**: El trabajo de las historias de usuario de refactorización no puede comenzar hasta que este paso sea completado con éxito.

- [ ] T003 Ejecutar `uv sync --upgrade` en la raíz del proyecto para descargar las últimas versiones de librerías y generar el nuevo archivo de bloqueo `uv.lock`.
- [ ] T004 Validar que Django arranque en el nuevo entorno ejecutando el chequeo de consistencia de Django `uv run python manage.py check`.

**Checkpoint**: El entorno virtual de Python está completamente actualizado y Polars está instalado y listo para ser utilizado en el código.

---

## Phase 3: User Story 1 - Reemplazo de Pandas por Polars en Visualización (Priority: P1) 🎯 MVP

**Goal**: Refactorizar la carga y agrupamiento de datos de tickets para Plotly en `dash/graficos.py` usando Polars de forma aislada.

**Independent Test**: Verificar que las funciones analíticas corran y devuelvan el marcado HTML correcto para Plotly sin lanzar excepciones.

### Implementation for User Story 1

- [ ] T005 [US1] Refactorizar la función `barTicketSeveritiesXmonth` en `/home/ciex/PROYECTOS/tickersec/dash/graficos.py` para reemplazar el DataFrame de Pandas por `pl.DataFrame(data)` y usar la agregación `.group_by(['month', 'severity']).len().rename({'len': 'count'})` de Polars.
- [ ] T006 [US1] Refactorizar la función `pieTicketSeverities` en `/home/ciex/PROYECTOS/tickersec/dash/graficos.py` para reemplazar la agrupación de Pandas por `pl.DataFrame(data)` y la agregación de Polars.
- [ ] T007 [US1] Refactorizar la función `pieTicketCategories` en `/home/ciex/PROYECTOS/tickersec/dash/graficos.py` reemplazando la lógica de Pandas por la agrupación de Polars y el límite de las 10 categorías principales usando `.top_k(10, by='count')`.
- [ ] T008 [US1] Validar la renderización interactiva de todos los gráficos del panel analítico levantando el servidor `uv run python manage.py runserver` y conectando el navegador.

**Checkpoint**: Todos los gráficos se renderizan y procesan los datos correctamente utilizando Polars de forma transparente.

---

## Phase 4: User Story 2 - Actualización de Librerías a Versiones Estables (Priority: P2)

**Goal**: Regenerar y verificar la lista compilada de requerimientos del proyecto.

**Independent Test**: Comprobar que se exporte de forma limpia el archivo de requerimientos tradicionales.

### Implementation for User Story 2

- [ ] T009 [US2] Compilar y exportar las dependencias resueltas a `/home/ciex/PROYECTOS/tickersec/requirements.txt` ejecutando `uv pip compile pyproject.toml -o requirements.txt` para mantener la consistencia externa.

---

## Phase 5: User Story 3 - Integración en Staging bajo GitHub Flow (Priority: P2)

**Goal**: Confirmar e integrar los cambios en la rama de staging remota para la realización de pruebas.

**Independent Test**: Comprobar que el PR esté abierto en GitHub con destino a la rama `staging`.

### Implementation for User Story 3

- [ ] T010 [US3] Agregar, confirmar y subir los cambios a la rama remota ejecutando `git add`, `git commit` y `git push origin refactor/migrate-polars`.
- [ ] T011 [US3] Crear el Pull Request en GitHub dirigido como base a la rama `staging` usando el comando de consola `gh pr create --base staging --fill`.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Mejoras finales y validación de calidad.

- [ ] T012 Actualizar la documentación técnica en `/home/ciex/PROYECTOS/tickersec/README.md` registrando la migración a Polars.
- [ ] T013 Validar que todas las pruebas unitarias pasen sin excepciones ejecutando `uv run python manage.py test`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias. Comienza de inmediato.
- **Foundational (Phase 2)**: Depende de Setup (Phase 1). Bloquea la implementación de las historias de usuario.
- **User Stories (Phases 3+)**: Dependen de la finalización de Foundational (Phase 2). Se ejecutan secuencialmente según la prioridad (P1 -> P2).
- **Polish (Final Phase)**: Se ejecuta una vez que todas las historias de usuario han sido completadas e integradas.
