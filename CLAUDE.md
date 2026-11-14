# CLAUDE.md: predict-future-sales

Proyecto acumulativo del curso **Product Development** (maestría). Autor: Fabio Suruy (trabaja solo).
Dataset: Kaggle *Predict Future Sales* (1C Company). Objetivo final: predecir las ventas mensuales por par tienda-producto de nov-2015.

## Al iniciar una sesión
1. Lee `docs/BITACORA.md` para saber el estado, las decisiones y el siguiente paso.
2. Al terminar, agrega una entrada fechada a `docs/BITACORA.md` con lo hecho, las decisiones, los hallazgos y los pendientes.

## Fases del curso
1. **EDA**, estructura cookiecutter y GitHub ← Proyecto 1
2. Notebooks a scripts (PEP8, logging, pytest)
3. DVC, Docker y MLflow
4. API con FastAPI
5. Front-end con Streamlit o un agente

## Entorno
- conda: `conda activate predict_future_sales` (Python 3.11). Dependencias en `environment.yml`; el paquete está instalado en modo editable (`pip install -e .`).
- Kernel de Jupyter: **Python (predict_future_sales)**.
- Si se agrega una dependencia, añadirla también a `environment.yml`.

## Convenciones
- Estructura de cookiecutter-data-science v2. Las rutas se toman siempre de `predict_future_sales/config.py` (`RAW_DATA_DIR`, `INTERIM_DATA_DIR`, `FIGURES_DIR`…); nunca rutas absolutas.
- Datos crudos en `data/raw/` (no se versionan). Datos intermedios en `data/interim/` en formato parquet.
- Notebooks numerados: `01_exploratory_data_analysis.ipynb` (nombre exigido por el enunciado), luego `02_...`, etc.
- Las funciones reutilizables de gráficas y agregación van en el paquete `predict_future_sales/` (por ejemplo `plots.py`), no copiadas en los notebooks. Esto prepara la fase 2.
- Notebooks, markdown e interpretaciones en **español**. El código y los nombres de variables pueden ir en inglés.
- Estilo: ruff (line-length 99).
- Construir los notebooks por bloques y validar cada bloque antes de seguir.

## Datos (columnas)
- `sales_train.csv`: date (dd.mm.yyyy), date_block_num (0 = ene-2013 … 33 = oct-2015), shop_id, item_id, item_price, item_cnt_day (los negativos son devoluciones)
- `items.csv`: item_name, item_id, item_category_id
- `item_categories.csv`: item_category_name, item_category_id
- `shops.csv`: shop_name, shop_id
- `test.csv`: ID, shop_id, item_id (pares de nov-2015)
- No hay columna de ingresos; se construye como `revenue = item_price * item_cnt_day`.
