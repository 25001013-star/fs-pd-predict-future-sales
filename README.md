# predict-future-sales

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

EDA y forecasting de ventas mensuales por tienda-producto (Kaggle Predict Future Sales) - Product Development

**Autor:** Fabio Suruy · Maestría, curso Product Development

## Cómo reproducir

```bash
git clone <url-del-repo>
cd predict-future-sales
conda env create -f environment.yml      # crea el entorno predict_future_sales
conda activate predict_future_sales
python -m ipykernel install --user --name predict_future_sales
```

1. Descarga los datos desde [Kaggle](https://www.kaggle.com/competitions/competitive-data-science-predict-future-sales/data). Primero hay que unirse a la competencia y aceptar sus reglas.
2. Copia los CSV (`sales_train.csv`, `items.csv`, `item_categories.csv`, `shops.csv`, `test.csv`) en `data/raw/`. Los datos **no** se versionan.
3. Abre `notebooks/01_exploratory_data_analysis.ipynb` con el kernel *Python (predict_future_sales)*.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         predict_future_sales and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── predict_future_sales   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes predict_future_sales a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

