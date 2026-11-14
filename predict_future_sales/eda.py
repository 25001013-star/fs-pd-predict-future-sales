"""Funciones reutilizables para el EDA de Predict Future Sales.

El notebook ``01_exploratory_data_analysis.ipynb`` usa estas funciones para que el análisis
quede limpio y para que la fase 2 del curso (pasar de notebooks a scripts) parta de código
ya modularizado.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from predict_future_sales.config import RAW_DATA_DIR

# Tiendas con el mismo nombre (o casi) y distinto ID. El ID de la izquierda solo existe en
# meses en los que el de la derecha no tiene ventas, por lo que se trata de la misma tienda.
SHOP_DUPLICATES: dict[int, int] = {0: 57, 1: 58, 11: 10}

# Traducción al español del grupo principal de cada categoría (texto antes de " - ").
CATEGORY_GROUP_ES: dict[str, str] = {
    "Книги": "Libros",
    "Подарки": "Regalos",
    "Игровые консоли": "Consolas",
    "Игры": "Juegos consola",
    "Аксессуары": "Accesorios",
    "Музыка": "Música",
    "Программы": "Programas",
    "Кино": "Cine",
    "Игры PC": "Juegos PC",
    "Карты оплаты": "Tarjetas de pago",
    "Карты оплаты (Кино, Музыка, Игры)": "Tarjetas de pago",
    "Служебные": "Servicio",
    "PC": "PC",
    "Билеты (Цифра)": "Boletos",
    "Доставка товара": "Envío",
    "Игры Android": "Juegos móviles",
    "Игры MAC": "Juegos PC",
    "Чистые носители (шпиль)": "Medios vírgenes",
    "Чистые носители (штучные)": "Medios vírgenes",
    "Элементы питания": "Baterías",
}

SPANISH_WEEKDAYS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
SPANISH_MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                  "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def load_raw(raw_dir: Path = RAW_DATA_DIR) -> dict[str, pd.DataFrame]:
    """Carga los cinco archivos del dataset y los devuelve en un diccionario."""
    files = {
        "sales_train": "sales_train.csv",
        "items": "items.csv",
        "item_categories": "item_categories.csv",
        "shops": "shops.csv",
        "test": "test.csv",
    }
    return {name: pd.read_csv(raw_dir / fname) for name, fname in files.items()}


def add_category_info(categories: pd.DataFrame) -> pd.DataFrame:
    """Agrega a ``item_categories`` el grupo principal en ruso y en español."""
    out = categories.copy()
    out["category_group_ru"] = out["item_category_name"].str.split(" - ").str[0].str.strip()
    out["category_group"] = out["category_group_ru"].map(CATEGORY_GROUP_ES).fillna("Otros")
    return out


def add_shop_info(shops: pd.DataFrame) -> pd.DataFrame:
    """Agrega la ciudad (primera palabra del nombre de la tienda)."""
    out = shops.copy()
    out["city"] = (out["shop_name"].str.replace("!", "", regex=False)
                   .str.split().str[0])
    return out


def build_sales_table(
    sales: pd.DataFrame,
    items: pd.DataFrame,
    categories: pd.DataFrame,
    shops: pd.DataFrame,
) -> pd.DataFrame:
    """Une las ventas con los catálogos, convierte la fecha y calcula los ingresos.

    No elimina ni corrige registros: esa limpieza se hace aparte con ``clean_sales``.
    """
    df = sales.copy()
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
    df["revenue"] = df["item_price"] * df["item_cnt_day"]
    df = (df.merge(items[["item_id", "item_category_id"]], on="item_id", how="left")
            .merge(add_category_info(categories), on="item_category_id", how="left")
            .merge(add_shop_info(shops)[["shop_id", "city"]], on="shop_id", how="left"))
    return df


def clean_sales(
    df: pd.DataFrame,
    max_price: float = 100_000,
    max_cnt: float = 1_000,
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Aplica la estrategia de limpieza definida en el EDA.

    1. Elimina los duplicados exactos.
    2. Elimina los precios <= 0.
    3. Elimina los outliers extremos (precio > ``max_price`` o cantidad > ``max_cnt``).
    4. Unifica los IDs de tiendas duplicadas (``SHOP_DUPLICATES``).

    Las devoluciones (``item_cnt_day`` < 0) se conservan porque el objetivo mensual es neto.
    Devuelve el DataFrame limpio y un resumen con cuántas filas afectó cada paso.
    """
    report: dict[str, int] = {"filas_iniciales": len(df)}
    out = df.drop_duplicates()
    report["duplicados_eliminados"] = report["filas_iniciales"] - len(out)

    mask = out["item_price"] <= 0
    report["precio_no_positivo_eliminados"] = int(mask.sum())
    out = out[~mask]

    mask = (out["item_price"] > max_price) | (out["item_cnt_day"] > max_cnt)
    report["outliers_extremos_eliminados"] = int(mask.sum())
    out = out[~mask]

    report["filas_con_tienda_reasignada"] = int(out["shop_id"].isin(SHOP_DUPLICATES).sum())
    out = out.assign(shop_id=out["shop_id"].replace(SHOP_DUPLICATES))
    out["revenue"] = out["item_price"] * out["item_cnt_day"]

    report["filas_finales"] = len(out)
    return out.reset_index(drop=True), report


def monthly_series(df: pd.DataFrame, by: list[str] | None = None,
                   value: str = "item_cnt_day") -> pd.DataFrame | pd.Series:
    """Suma ``value`` por mes (``date_block_num``) y, opcionalmente, por otras llaves.

    Con ``by`` devuelve una tabla ancha (meses × llaves) con ceros donde no hubo ventas.
    """
    if not by:
        return df.groupby("date_block_num")[value].sum()
    wide = df.pivot_table(index="date_block_num", columns=by, values=value,
                          aggfunc="sum", fill_value=0)
    return wide.reindex(range(df["date_block_num"].max() + 1), fill_value=0)


def plot_acf_pacf(series: pd.Series, lags: int, title: str,
                  axes: tuple[plt.Axes, plt.Axes] | None = None) -> tuple[plt.Axes, plt.Axes]:
    """Grafica ACF y PACF de una serie, lado a lado."""
    if axes is None:
        _, axes = plt.subplots(1, 2, figsize=(14, 3.6))
    lags = min(lags, len(series) // 2 - 1)
    plot_acf(series, lags=lags, ax=axes[0], title=f"ACF · {title}")
    plot_pacf(series, lags=lags, ax=axes[1], title=f"PACF · {title}", method="ywm")
    for ax in axes:
        ax.set_xlabel("Rezago")
    return axes


def save_fig(fig: plt.Figure, name: str, figures_dir: Path | None = None) -> Path:
    """Guarda una figura en ``reports/figures`` y devuelve la ruta."""
    from predict_future_sales.config import FIGURES_DIR

    figures_dir = figures_dir or FIGURES_DIR
    figures_dir.mkdir(parents=True, exist_ok=True)
    path = figures_dir / f"{name}.png"
    fig.savefig(path, dpi=120, bbox_inches="tight")
    return path
