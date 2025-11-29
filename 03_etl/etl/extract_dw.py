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
