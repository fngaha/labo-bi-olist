import pandas as pd
from .db_connection import get_engine


def read_d_category() -> pd.DataFrame:
    """
    Lit la dimension D_Category dans le DW pour récupérer Category_SK.
    """
    engine = get_engine("database_dw")
    query = """
        SELECT Category_SK, product_category_name
        FROM dbo.D_Category;
    """
    df = pd.read_sql(query, engine)
    return df


def read_d_date() -> pd.DataFrame:
    engine = get_engine("database_dw")
    query = "SELECT Date_SK, Date_Actual FROM dbo.D_Date;"
    return pd.read_sql(query, engine)


def read_d_product() -> pd.DataFrame:
    engine = get_engine("database_dw")
    query = "SELECT Product_SK, product_id FROM dbo.D_Product;"
    return pd.read_sql(query, engine)


def read_d_customer() -> pd.DataFrame:
    engine = get_engine("database_dw")
    query = "SELECT Customer_SK, customer_unique_id FROM dbo.D_Customer;"
    return pd.read_sql(query, engine)


def read_d_seller() -> pd.DataFrame:
    engine = get_engine("database_dw")
    query = "SELECT Seller_SK, seller_id FROM dbo.D_Seller;"
    return pd.read_sql(query, engine)


def read_d_payment_type() -> pd.DataFrame:
    engine = get_engine("database_dw")
    query = "SELECT PaymentType_SK, payment_type FROM dbo.D_PaymentType;"
    return pd.read_sql(query, engine)


def read_d_order_status() -> pd.DataFrame:
    engine = get_engine("database_dw")
    query = "SELECT OrderStatus_SK, order_status FROM dbo.D_OrderStatus;"
    return pd.read_sql(query, engine)