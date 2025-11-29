import pandas as pd


def build_d_category(categories: pd.DataFrame) -> pd.DataFrame:
    """
    Construit la dimension D_Category à partir de la table
    Category_name_translation du staging.

    On ne gère pas ici la surrogate key (Category_SK) : on la laissera
    à SQL Server (IDENTITY) ou on la gérera dans un 2e temps.
    """
    # On ne garde que les colonnes utiles et on enlève les doublons
    dim = categories[
        ["product_category_name", "product_category_name_english"]
    ].drop_duplicates()

    # Optionnel : trier
    dim = dim.sort_values("product_category_name").reset_index(drop=True)

    return dim


def build_d_product(products: pd.DataFrame, dim_category_with_sk: pd.DataFrame) -> pd.DataFrame:
    """
    Construit la dimension D_Product à partir de la table products
    et de D_Category (avec Category_SK).
    """

    # 1. Une ligne par product_id
    base = products.drop_duplicates(subset=["product_id"]).copy()

    # 2. Join pour récupérer Category_SK à partir de product_category_name
    dim = base.merge(
        dim_category_with_sk[["product_category_name", "Category_SK"]],
        how="left",
        on="product_category_name"
    )

    # 3. Sélection des colonnes dans l'ordre de la table SQL (sans Product_SK)
    dim = dim[
        [
            "product_id",
            "Category_SK",
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]
    ].copy()

    # 4. Forcer les types numériques proprement

    # Colonnes numériques
    numeric_cols = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    # Conversion en numérique (avec coercition pour gérer les valeurs invalides)
    for col in numeric_cols:
        dim[col] = pd.to_numeric(dim[col], errors="coerce")

    # Category_SK doit être un entier (SK) mais peut contenir des NULL
    dim["Category_SK"] = dim["Category_SK"].astype("Int64")  # entier nullable

    return dim


def build_d_customer(customers: pd.DataFrame) -> pd.DataFrame:
    """
    Construit la dimension D_Customer à partir de la table customers du staging.

    Grain : 1 ligne par customer_unique_id.
    Si plusieurs customer_id pour un même customer_unique_id, on garde la première occurrence.
    """
    # On trie pour rendre le choix déterministe (par exemple par customer_unique_id, puis customer_id)
    df = customers.sort_values(
        ["customer_unique_id", "customer_id"]
    ).copy()

    # On garde la première ligne par customer_unique_id
    df_unique = df.drop_duplicates(subset=["customer_unique_id"], keep="first")

    dim = df_unique[
        [
            "customer_unique_id",
            "customer_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ]
    ].reset_index(drop=True)

    return dim


def build_d_seller(sellers: pd.DataFrame) -> pd.DataFrame:
    """
    Construit la dimension D_Seller à partir de la table sellers du staging.

    Grain : 1 ligne par seller_id.
    """
    df = sellers.drop_duplicates(subset=["seller_id"]).copy()

    dim = df[
        [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state",
        ]
    ].reset_index(drop=True)

    return dim

def build_d_payment_type(order_payments: pd.DataFrame) -> pd.DataFrame:
    """
    Construit la dimension D_PaymentType à partir de order_payments.

    Grain : 1 ligne par payment_type distinct.
    """
    dim = (
        order_payments[["payment_type"]]
        .drop_duplicates()
        .sort_values("payment_type")
        .reset_index(drop=True)
    )
    return dim

def build_d_order_status(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Construit la dimension D_OrderStatus à partir de orders.

    Grain : 1 ligne par order_status distinct.
    """
    dim = (
        orders[["order_status"]]
        .drop_duplicates()
        .sort_values("order_status")
        .reset_index(drop=True)
    )
    return dim


def build_all_dimensions(staging: dict) -> dict:
    """
    Construit toutes les dimensions sous forme de DataFrames.
    Pour l'instant, on ne remplit que D_Category, les autres viendront après.
    """
    dims = {}

    categories = staging["Category_name_translation"]
    dims["D_Category"] = build_d_category(categories)

    # TODO: dims["D_Product"] = build_d_product(...)
    # TODO: dims["D_Customer"] = build_d_customer(...)
    # etc.

    return dims
