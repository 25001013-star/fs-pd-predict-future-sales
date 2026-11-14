# Bitácora del proyecto

## Sesión 1 (2026-11-14): estructura del proyecto
**Hecho**
- Entorno conda `predict_future_sales` (Python 3.11) con pandas, statsmodels, seaborn, pyarrow y jupyter. Kernel registrado como "Python (predict_future_sales)".
- Estructura generada con cookiecutter-data-science v2.3 (`ccds`): conda, environment.yml, pytest, ruff, sin licencia y con el scaffold del paquete `predict_future_sales`.
- `.gitignore` ajustado: se ignoran los archivos dentro de `data/*/` pero se conservan los `.gitkeep`. También se ignoran `*.csv`, `*.zip`, `*.parquet` y `*.pkl`.
- Datos de Kaggle copiados en `data/raw/` (6 CSV, ~100 MB).
- Notebook esqueleto `notebooks/01_exploratory_data_analysis.ipynb` con las secciones 1–10 del enunciado.
- `git init` y primer commit.

**Pendiente (lo hace Fabio)**
- Crear el repo vacío `predict-future-sales` en GitHub y pasar la URL para conectarlo y hacer push.
- Tomar el screenshot del `git pull` (punto 1.f).

**Siguiente paso**
- Llenar las secciones 2 (comprensión inicial) y 3 (validación de estructura) del notebook.
