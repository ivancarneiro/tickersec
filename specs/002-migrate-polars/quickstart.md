# Quickstart: migrate-polars

Esta guía detalla cómo probar la migración a Polars y validar el dashboard analítico de TickerSec.

## 1. Actualización y Sincronización

Una vez modificadas las dependencias en `pyproject.toml`, sincroniza el entorno virtual con:

```bash
uv sync --upgrade
```

Esto:
1. Eliminará `pandas` y sus dependencias asociadas del entorno virtual.
2. Descargará las últimas versiones estables de `polars`, `django`, `plotly` y demás paquetes.
3. Actualizará el archivo `uv.lock`.

## 2. Ejecutar y Validar el Dashboard

Para comprobar que la migración a Polars de los gráficos en `dash/graficos.py` es correcta:

1. Levanta el servidor de desarrollo:
   ```bash
   uv run python manage.py runserver
   ```
2. Abre tu navegador y navega al dashboard analítico.
3. Comprueba que los tres gráficos principales (Tickets por Severidad en los 12 meses, Distribución por Severidad y Top 10 Categorías) se rendericen de forma interactiva y muestren los datos correctamente.
4. Opcionalmente, corre el conjunto de pruebas para verificar la consistencia del sistema:
   ```bash
   uv run python manage.py test
   ```
