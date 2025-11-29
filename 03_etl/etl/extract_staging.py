import pandas as pd
from .db_connection import get_engine


import pandas as pd
from .db_connection import get_engine


def extract_categories() -> pd.DataFrame:
    engine = get_engine("database_staging")
    query = "SELECT * FROM dbo.product_category_name_translation;"
    df = pd.read_sql(query, engine)
    return df


def extract_products() -> pd.DataFrame:
    """
    Lit la table products dans le staging.
    """
    engine = get_engine("database_staging")
    query = "SELECT * FROM dbo.products;"
    df = pd.read_sql(query, engine)
    return df


def read_table(table_name: str) -> pd.DataFrame:
    """
    Lit une table du schéma dbo de la base de staging.
    """
    engine = get_engine("database_staging")
    query = f"SELECT * FROM dbo.{table_name};"
    df = pd.read_sql(query, engine)
    return df


def extract_customers() -> pd.DataFrame:
    """
    Lit la table customers dans le staging.
    """
    engine = get_engine("database_staging")
    query = "SELECT * FROM dbo.customer;"
    df = pd.read_sql(query, engine)
    return df


def extract_sellers() -> pd.DataFrame:
    """
    Lit la table sellers dans le staging.
    """
    engine = get_engine("database_staging")
    query = "SELECT * FROM dbo.sellers;"
    df = pd.read_sql(query, engine)
    return df

def extract_order_payments() -> pd.DataFrame:
    """
    Lit la table order_payments dans le staging.
    """
    engine = get_engine("database_staging")
    query = "SELECT * FROM dbo.order_payments;"
    df = pd.read_sql(query, engine)
    return df

def extract_orders() -> pd.DataFrame:
    """
    Lit la table orders dans le staging.
    """
    engine = get_engine("database_staging")
    query = "SELECT * FROM dbo.orders;"
    df = pd.read_sql(query, engine)
    return df


def extract_order_items() -> pd.DataFrame:
    """
    Lit la table order_items dans le staging.
    """
    engine = get_engine("database_staging")
    query = "SELECT * FROM dbo.order_item;"
    df = pd.read_sql(query, engine)
    return df


def extract_all_staging() -> dict:
    """
    Charge toutes les tables de staging nécessaires dans des DataFrames.
    """
    tables = [
        "orders",
        "order_items",
        "order_payments",
        "order_reviews",
        "products",
        "customers",
        "sellers",
        "geolocation",
        "product_category_name_translation",
    ]

    data = {}
    for t in tables:
        data[t] = read_table(t)

    return data
