# Bitácora del proyecto

## Sesión 1 (2026-11-14): estructura del proyecto
**Hecho**
- Entorno conda `predict_future_sales` (Python 3.11) con pandas, statsmodels, seaborn, pyarrow y jupyter. Kernel registrado como "Python (predict_future_sales)".
- Estructura generada con cookiecutter-data-science v2.3 (`ccds`): conda, environment.yml, pytest, ruff, sin licencia y con el scaffold del paquete `predict_future_sales`.
- `.gitignore` ajustado: se ignoran los archivos dentro de `data/*/` pero se conservan los `.gitkeep`. También se ignoran `*.csv`, `*.zip`, `*.parquet` y `*.pkl`.
- Datos de Kaggle copiados en `data/raw/` (6 CSV, ~100 MB).
- Notebook esqueleto `notebooks/01_exploratory_data_analysis.ipynb` con las secciones 1–10 del enunciado.
- `git init` y primer commit.

- Repo de GitHub creado por Fabio: https://github.com/25001013-star/fs-pd-predict-future-sales (remoto `origin`).
- **EDA completo (secciones 1–10)** en el notebook, ejecutado sin errores. Las funciones están en `predict_future_sales/eda.py` (carga, limpieza, `monthly_series`, `plot_acf_pacf`, `save_fig`) y las figuras clave en `reports/figures/`.
- Limpieza → `data/interim/sales_clean.parquet`:
  - Se eliminaron 6 duplicados exactos, 1 precio ≤ 0 y 2 outliers (precio > 100k, cantidad > 1000).
  - Se unificaron tiendas: 0→57, 1→58, 11→10. La 40 no se unificó con la 39 porque vendieron en paralelo.
  - Se conservan las devoluciones.

**Hallazgos clave**
- Tendencia descendente en unidades (ADF p = 0.15, no estacionaria; con una diferencia sí lo es). Pico en diciembre; noviembre es mayor que octubre.
- Ciclo semanal (el sábado es el día más fuerte). ACF diaria con picos cada 7 días.
- PACF con rezago 1 en todos los niveles (AR(1)). Lag 12 significativo en la serie diferenciada (≈ 0.45).
- 18 % de los productos concentra el 80 % de las unidades. La bolsa de compra `20949` es un caso especial.
- Test = malla de 42 tiendas × 5,100 productos:
  - 52 % de los pares tiene historial.
  - 41 % son productos conocidos, nuevos en esa tienda.
  - 7 % son productos nuevos.
  - Solo 13 % de los pares vendió en oct-2015.
- La mediana de meses sin venta por par es 94 % (series intermitentes) → conviene un modelo global de ML con lags y variables de respaldo.

**Pendiente (lo hace Fabio)**
- `git push -u origin main` (requiere su login).
- Screenshot del `git pull` (1.f).
- Revisar y ejecutar el notebook en VS Code, ajustando las interpretaciones con su propio criterio.

**Siguiente paso**
- Fase 2: feature engineering (malla mensual, `item_cnt_month` recortado a [0, 20], lags) y pasar el flujo a scripts.
