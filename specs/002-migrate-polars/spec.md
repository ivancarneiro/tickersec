# Feature Specification: migrate-polars

**Feature Branch**: `refactor/migrate-polars`

**Created**: 2026-07-13

**Status**: Draft

**Input**: User description: "Recuerda que debemos utilizar Github Flows para desarrollar la nueva etapa de refact. Crea una rama staging para test y una rama por cada feature como bien dice el estándar conventional commits. Debemos actualizar las librerías a sus últimas versiones estables. Reemplazaremos pandas por polars."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reemplazo de Pandas por Polars en Visualización (Priority: P1)

Como desarrollador del panel analítico de TickerSec, quiero que el procesamiento de datos y la agregación de métricas de tickets para los gráficos de Plotly se realice exclusivamente mediante la librería `polars` en lugar de `pandas`, para mejorar el rendimiento del procesamiento y eliminar la dependencia de Pandas.

**Why this priority**: Es el requerimiento central de refactorización analítica. Aísla y elimina Pandas del código fuente, reemplazándolo por un motor de DataFrames de alto rendimiento.

**Independent Test**: Modificar `dash/graficos.py` para remover `pandas` y usar `polars`, y verificar que el dashboard funcione cargando correctamente los datos y renderizando los gráficos sin errores de tipos o valores en las páginas web.

**Acceptance Scenarios**:

1. **Given** que el código de `dash/graficos.py` ha sido refactorizado, **When** se llama a `barTicketSeveritiesXmonth`, `pieTicketSeverities`, y `pieTicketCategories`, **Then** la consulta de tickets se convierte a un DataFrame de Polars (`pl.DataFrame`) y realiza las agregaciones por severidad, mes y categorías exitosamente.
2. **Given** la necesidad de limitar la distribución de categorías en el gráfico, **When** se procesan los datos, **Then** se obtienen correctamente las 10 categorías principales usando la función de Polars `top_k()` o `head(10)` y se envían a Plotly Express para el renderizado.

---

### User Story 2 - Actualización de Librerías a sus Últimas Versiones Estables (Priority: P2)

Como administrador del sistema TickerSec, quiero actualizar las librerías registradas en `pyproject.toml` a sus últimas versiones estables liberadas, de modo que el proyecto incorpore las últimas optimizaciones y parches de seguridad.

**Why this priority**: Mantiene la salud del proyecto a largo plazo y evita la acumulación de vulnerabilidades de seguridad en el entorno de producción.

**Independent Test**: Modificar los rangos de versiones en `pyproject.toml` (o remover restricciones estrictas obsoletas), correr `uv lock --upgrade` y comprobar que no se produzcan fallos al levantar Django.

**Acceptance Scenarios**:

1. **Given** que el archivo `pyproject.toml` define las dependencias del proyecto, **When** ejecuto `uv sync --upgrade`, **Then** se descargan las últimas versiones estables compatibles de Django, Plotly, Polars y otros paquetes y se bloquean en `uv.lock`.
2. **Given** la actualización completada, **When** corro `uv run python manage.py check`, **Then** Django no arroja advertencias de compatibilidad de APIs deprecadas.

---

### User Story 3 - Flujo de Trabajo en Staging bajo GitHub Flow (Priority: P2)

Como desarrollador, quiero implementar los cambios en la rama `refactor/migrate-polars` y abrir el Pull Request dirigido a la rama de integración `staging` para realizar las pruebas correspondientes antes de llevarlo a `main`.

**Why this priority**: Sigue el flujo estándar de integración continua y control de calidad antes de liberar cambios en producción.

**Independent Test**: Verificar que el PR abierto con `gh pr create` esté apuntando como base a la rama `staging` y que todos los tests pasen en esa rama de staging.

**Acceptance Scenarios**:

1. **Given** que estamos en la rama `refactor/migrate-polars`, **When** abrimos un PR, **Then** el PR se establece con la rama base `staging`.
2. **Given** que los cambios son validados en `staging`, **When** se comprueba la estabilidad, **Then** se puede proceder a fusionar `staging` a la rama `main`.

## Edge Cases

- **Compatibilidad de tipos de Polars con Plotly Express**: Plotly Express requiere en ocasiones estructuras específicas para leer los datos (como DataFrames de pandas u objetos tipo diccionario). Debemos asegurar que los DataFrames de Polars se puedan pasar directamente a Plotly Express (las versiones modernas de Plotly lo soportan) o convertirlos a diccionarios compatibles (`df.to_dict(as_series=False)`) en caso de incompatibilidades en ciertos tipos de gráficos.
- **Tipos de datos de tiempo en Polars**: Cuando se extrae el mes de las fechas en Polars, hay que asegurar que la conversión de tipo de datos mantenga el tipo entero para mapear correctamente el mes con la función `obtener_nombre_mes_abreviado`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La librería `pandas` MUST ser completamente removida de `pyproject.toml` y de cualquier parte del código fuente.
- **FR-002**: La librería `polars` MUST ser agregada a las dependencias de `pyproject.toml`.
- **FR-003**: Todas las dependencias principales en `pyproject.toml` MUST ser actualizadas a su última versión estable (compatibles con Python >= 3.10).
- **FR-004**: El procesamiento y agregaciones de los DataFrames en `dash/graficos.py` MUST realizarse utilizando Polars (`pl.DataFrame`).
- **FR-005**: La rama base para la integración de features en GitHub MUST ser la rama `staging`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El dashboard de analíticas se renderiza por completo en el navegador en menos de 1 segundo tras la llamada HTTP en desarrollo local.
- **SC-002**: No existe ninguna referencia a `import pandas` en el código de la aplicación.
- **SC-003**: El comando `uv run python manage.py check` y el servidor inician sin errores con las versiones de paquetes más recientes bloqueadas en `uv.lock`.
