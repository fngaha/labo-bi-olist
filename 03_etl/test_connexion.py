from sqlalchemy import text
from etl.db_connection import get_engine

def test_conn():
    engine = get_engine("database_staging")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT TOP 1 * FROM dbo.orders;"))
        row = result.fetchone()
        print("Connexion OK, première ligne de orders :", row)

if __name__ == "__main__":
    test_conn()
