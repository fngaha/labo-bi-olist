import pandas as pd
from sqlalchemy import text

from .db_connection import get_engine


def load_fact_ventes_items(fact_df: pd.DataFrame, truncate: bool = True) -> None:
    """
    Charge la table de faits F_Ventes_Items dans Olist_DW.

    On suppose que dbo.F_Ventes_Items existe déjà avec la structure définie.
    """
    engine = get_engine("database_dw")

    with engine.begin() as conn:
        if truncate:
            conn.execute(text("TRUNCATE TABLE dbo.F_Ventes_Items;"))

        fact_df.to_sql(
            "F_Ventes_Items",
            con=conn,
            schema="dbo",
            if_exists="append",
            index=False,
        )
