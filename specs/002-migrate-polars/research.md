# Research: migrate-polars

Este documento detalla la investigación técnica sobre el reemplazo de Pandas por Polars y la actualización general de las dependencias.

## 1. Migración de Sintaxis: Pandas a Polars

Polars tiene una sintaxis diferente para la manipulación de DataFrames. A continuación, se detalla el mapeo de las funciones utilizadas en `dash/graficos.py`:

### Caso 1: Agrupación Simple de Severidad por Mes
*   **Pandas**:
    ```python
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['month', 'severity']).size().reset_index(name='count')
    ```
*   **Polars**:
    ```python
    df = pl.DataFrame(data)
    df_grouped = df.group_by(['month', 'severity']).len().rename({'len': 'count'})
    ```
    *Nota*: Polars usa `group_by` en lugar de `groupby`, y la función `.len()` genera la columna con el recuento total de filas agrupadas. Renombramos `len` a `count` para mantener compatibilidad con las variables que lee Plotly Express.

### Caso 2: Top 10 Categorías
*   **Pandas**:
    ```python
    df_grouped = df.groupby(['category']).size().reset_index(name='count').nlargest(10, 'count')
    ```
*   **Polars**:
    ```python
    df_grouped = df.group_by(['category']).len().rename({'len': 'count'}).top_k(10, by='count')
    ```
    *Nota*: Polars utiliza `top_k(k, by='col')` para obtener los k elementos más grandes de forma muy eficiente, reemplazando a `nlargest(k, 'col')` de Pandas.

---

## 2. Actualización de Dependencias a sus Últimas Versiones Estables

Para permitir que `uv` instale las últimas versiones estables de las librerías en lugar de versiones congeladas antiguas, cambiaremos la declaración de dependencias en `pyproject.toml`:

*   **Django**: Quitar el anclaje estricto a `5.0.11` y permitir actualizaciones compatibles `django>=5.0`.
*   **Plotly**: Quitar el anclaje a `5.24.1` y declarar `plotly`.
*   **Decouple y adaptadores**: Declarar `python-decouple`, `psycopg2-binary`, `pillow`, `django-bootstrap5`, `django-quill-editor` sin versiones fijas para que `uv` busque las últimas versiones estables.
*   **Pandas**: Eliminar por completo de las dependencias.
*   **Polars**: Añadir `polars` como dependencia directa.
