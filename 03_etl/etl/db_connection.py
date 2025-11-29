from pathlib import Path
import urllib.parse

import yaml
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_connection_url(database_key: str) -> str:
    """
    Construit l'URL SQLAlchemy pour SQL Server via pyodbc.
    database_key = 'database_staging' ou 'database_dw'
    """
    cfg = load_config()["sqlserver"]

    host = cfg["host"]                 # ex: GOS-VDI410\TFTIC
    db = cfg[database_key]            # Olist_Staging ou Olist_DW
    driver = urllib.parse.quote_plus(cfg["driver"])

    user = cfg.get("user") or ""
    password = cfg.get("password") or ""

    if user:
        # Auth SQL (login/mot de passe)
        password_enc = urllib.parse.quote_plus(password)
        auth_part = f"{user}:{password_enc}@"
        extra_params = f"driver={driver}&TrustServerCertificate=yes&Encrypt=no"
    else:
        # Auth Windows (Trusted Connection)
        auth_part = ""
        extra_params = f"driver={driver}&Trusted_Connection=yes&TrustServerCertificate=yes&Encrypt=no"

    # Note : pas de port ici, on laisse SQL Browser gérer l'instance nommée
    url = f"mssql+pyodbc://{auth_part}{host}/{db}?{extra_params}"
    return url


def get_engine(database_key: str = "database_staging") -> Engine:
    """
    Retourne un Engine SQLAlchemy pour la base choisie.
    """
    url = build_connection_url(database_key)
    engine = create_engine(url, fast_executemany=True)
    return engine
