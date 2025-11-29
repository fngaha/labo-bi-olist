from typing import Dict

import pandas as pd
from sqlalchemy import text

from .db_connection import get_engine


def load_d_category(dim_category: pd.DataFrame, truncate: bool = False) -> None:
    """
    Charge la dimension D_Category dans la base DW.

    - Si truncate=True : on vide la table avant d'insérer.
    - On suppose que la table dbo.D_Category existe déjà dans la base DW
      avec une colonne Category_SK en IDENTITY et les colonnes:
      - product_category_name
      - product_category_name_english
    """
    engine = get_engine("database_dw")

    with engine.begin() as conn:
        if truncate:
            conn.execute(text("TRUNCATE TABLE dbo.D_Category;"))

        # On insère uniquement les colonnes non-SK
        dim_category.to_sql(
            "D_Category",
            con=conn,
            schema="dbo",
            if_exists="append",
            index=False,
        )


def load_d_product(dim_product: pd.DataFrame, truncate: bool = True) -> None:
    """
    Charge la dimension D_Product dans Olist_DW.

    On suppose que dbo.D_Product existe déjà avec :
      - Product_SK (IDENTITY, PK)
      - les colonnes du DataFrame (sans Product_SK).
    """
    engine = get_engine("database_dw")

    with engine.begin() as conn:
        if truncate:
            conn.execute(text("TRUNCATE TABLE dbo.D_Product;"))

        dim_product.to_sql(
            "D_Product",
            con=conn,
            schema="dbo",
            if_exists="append",
            index=False,
        )


def load_d_customer(dim_customer: pd.DataFrame, truncate: bool = True) -> None:
    """
    Charge la dimension D_Customer dans Olist_DW.

    On suppose que dbo.D_Customer existe déjà avec :
      - Customer_SK (IDENTITY, PK)
      - les colonnes du DataFrame (sans Customer_SK).
    """
    engine = get_engine("database_dw")

    with engine.begin() as conn:
        if truncate:
            conn.execute(text("TRUNCATE TABLE dbo.D_Customer;"))

        dim_customer.to_sql(
            "D_Customer",
            con=conn,
            schema="dbo",
            if_exists="append",
            index=False,
        )


def load_d_seller(dim_seller: pd.DataFrame, truncate: bool = True) -> None:
    """
    Charge la dimension D_Seller dans Olist_DW.

    On suppose que dbo.D_Seller existe déjà avec :
      - Seller_SK (IDENTITY, PK)
      - les colonnes du DataFrame (sans Seller_SK).
    """
    engine = get_engine("database_dw")

    with engine.begin() as conn:
        if truncate:
            conn.execute(text("TRUNCATE TABLE dbo.D_Seller;"))

        dim_seller.to_sql(
            "D_Seller",
            con=conn,
            schema="dbo",
            if_exists="append",
            index=False,
        )


def load_d_payment_type(dim_payment_type: pd.DataFrame, truncate: bool = True) -> None:
    """
    Charge la dimension D_PaymentType dans Olist_DW.
    """
    engine = get_engine("database_dw")

    with engine.begin() as conn:
        if truncate:
            conn.execute(text("TRUNCATE TABLE dbo.D_PaymentType;"))

        dim_payment_type.to_sql(
            "D_PaymentType",
            con=conn,
            schema="dbo",
            if_exists="append",
            index=False,
        )


def load_d_order_status(dim_order_status: pd.DataFrame, truncate: bool = True) -> None:
    """
    Charge la dimension D_OrderStatus dans Olist_DW.
    """
    engine = get_engine("database_dw")

    with engine.begin() as conn:
        if truncate:
            conn.execute(text("TRUNCATE TABLE dbo.D_OrderStatus;"))

        dim_order_status.to_sql(
            "D_OrderStatus",
            con=conn,
            schema="dbo",
            if_exists="append",
            index=False,
        )


def load_all_dimensions(dims: Dict[str, pd.DataFrame]) -> None:
    """
    Charge toutes les dimensions construites dans la base DW.
    Pour l'instant on ne gère que D_Category.
    """
    if "D_Category" in dims:
        load_d_category(dims["D_Category"], truncate=True)

    # TODO: ajouter D_Product, D_Customer, etc. quand elles seront prêtes.
