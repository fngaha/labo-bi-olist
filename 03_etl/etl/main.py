import argparse
import logging
from pathlib import Path
from .db_connection import get_engine
from sqlalchemy import text

LOG_PATH = Path(__file__).resolve().parent.parent / "etl_olist.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    filename=str(LOG_PATH),
    filemode="a",
)

logger = logging.getLogger("etl_olist")

from .extract_staging import (
    extract_categories,
    extract_products,
    extract_customers,
    extract_sellers,
    extract_order_payments,
    extract_orders,
    extract_order_items,
)
from .transform_dimensions import (
    build_d_category,
    build_d_product,
    build_d_customer,
    build_d_seller,
    build_d_payment_type,
    build_d_order_status,
)
from .load_dimensions import (
    load_d_category,
    load_d_product,
    load_d_customer,
    load_d_seller,
    load_d_payment_type,
    load_d_order_status,
)
from .extract_dw import (
    read_d_category,
    read_d_date,
    read_d_product,
    read_d_customer,
    read_d_seller,
    read_d_payment_type,
    read_d_order_status,
)
from .transform_facts import build_fact_ventes_items
from .load_facts import load_fact_ventes_items


def run_etl_d_category():
    logger.info("ETL D_Category - démarrage...")

    categories = extract_categories()
    logger.info(
        f"EXTRACT: {len(categories)} lignes lues depuis product_category_name_translation."
    )

    dim_category = build_d_category(categories)
    logger.info(f"TRANSFORM: {len(dim_category)} catégories distinctes construites.")

    load_d_category(dim_category, truncate=True)
    logger.info("LOAD: D_Category chargée dans Olist_DW.")


def run_etl_d_product():
    logger.info("ETL D_Product - démarrage...")

    # 1. EXTRACT
    products = extract_products()
    logger.info(f"EXTRACT: {len(products)} produits lus depuis products (staging).")

    dim_category_dw = read_d_category()
    logger.info(f"EXTRACT: {len(dim_category_dw)} lignes lues depuis D_Category (DW).")

    # 2. TRANSFORM
    dim_product = build_d_product(products, dim_category_dw)
    logger.info(f"TRANSFORM: {len(dim_product)} produits dimensionnels construits.")

    # 3. LOAD
    load_d_product(dim_product, truncate=True)
    logger.info("LOAD: D_Product chargée dans Olist_DW.")


def run_etl_d_customer():
    logger.info("ETL D_Customer - démarrage...")

    customers = extract_customers()
    logger.info(f"EXTRACT: {len(customers)} lignes lues depuis customers (staging).")

    dim_customer = build_d_customer(customers)
    logger.info(
        f"TRANSFORM: {len(dim_customer)} clients dimensionnels construits "
        f"(1 ligne par customer_unique_id)."
    )

    load_d_customer(dim_customer, truncate=True)
    logger.info("LOAD: D_Customer chargée dans Olist_DW.")


def run_etl_d_seller():
    logger.info("ETL D_Seller - démarrage...")

    sellers = extract_sellers()
    logger.info(f"EXTRACT: {len(sellers)} lignes lues depuis sellers (staging).")

    dim_seller = build_d_seller(sellers)
    logger.info(f"TRANSFORM: {len(dim_seller)} vendeurs dimensionnels construits.")

    load_d_seller(dim_seller, truncate=True)
    logger.info("LOAD: D_Seller chargée dans Olist_DW.")


def run_etl_d_payment_type():
    logger.info("ETL D_PaymentType - démarrage...")

    order_payments = extract_order_payments()
    logger.info(
        f"EXTRACT: {len(order_payments)} lignes lues depuis order_payments (staging)."
    )

    dim_payment_type = build_d_payment_type(order_payments)
    logger.info(
        f"TRANSFORM: {len(dim_payment_type)} types de paiement distincts construits."
    )

    load_d_payment_type(dim_payment_type, truncate=True)
    logger.info("LOAD: D_PaymentType chargée dans Olist_DW.")


def run_etl_d_order_status():
    logger.info("ETL D_OrderStatus - démarrage...")

    orders = extract_orders()
    logger.info(f"EXTRACT: {len(orders)} lignes lues depuis orders (staging).")

    dim_order_status = build_d_order_status(orders)
    logger.info(
        f"TRANSFORM: {len(dim_order_status)} statuts de commande distincts construits."
    )

    load_d_order_status(dim_order_status, truncate=True)
    logger.info("LOAD: D_OrderStatus chargée dans Olist_DW.")


def run_etl_dimensions():
    logger.info("=== ETL DIMENSIONS - DÉBUT ===")
    run_etl_d_category()
    run_etl_d_product()
    run_etl_d_customer()
    run_etl_d_seller()
    run_etl_d_payment_type()
    run_etl_d_order_status()
    logger.info("=== ETL DIMENSIONS - FIN ===")


def run_etl_fact_ventes_items():
    logger.info("ETL F_Ventes_Items - démarrage")
    orders = extract_orders()
    order_items = extract_order_items()
    order_payments = extract_order_payments()
    products = extract_products()
    customers = extract_customers()
    sellers = extract_sellers()

    d_date = read_d_date()
    d_product = read_d_product()
    d_customer = read_d_customer()
    d_seller = read_d_seller()
    d_payment_type = read_d_payment_type()
    d_order_status = read_d_order_status()

    fact_df = build_fact_ventes_items(
        orders,
        order_items,
        order_payments,
        products,
        customers,
        sellers,
        d_date,
        d_product,
        d_customer,
        d_seller,
        d_payment_type,
        d_order_status,
    )
    load_fact_ventes_items(fact_df, truncate=True)
    logger.info("ETL F_Ventes_Items - terminé")

    # Contrôles qualité rapides
    engine = get_engine("database_dw")
    with engine.connect() as conn:
        # Nombre de lignes
        res = conn.execute(text("SELECT COUNT(*) AS cnt FROM dbo.F_Ventes_Items;"))
        cnt = res.fetchone().cnt
        logger.info("QC: F_Ventes_Items contient %d lignes", cnt)

        # Recherche de SK NULL
        res_null = conn.execute(
            text(
                """
            SELECT COUNT(*) AS cnt_null
            FROM dbo.F_Ventes_Items
            WHERE Date_SK IS NULL
               OR Product_SK IS NULL
               OR Customer_SK IS NULL
               OR Seller_SK IS NULL
               OR OrderStatus_SK IS NULL
        """
            )
        )
        cnt_null = res_null.fetchone().cnt_null

        if cnt_null > 0:
            logger.warning(
                "QC: %d lignes dans F_Ventes_Items ont au moins une SK NULL", cnt_null
            )
        else:
            logger.info("QC: aucune SK NULL détectée dans F_Ventes_Items.")


def run_etl_all():
    logger.info("=== ETL COMPLET OLIST - DÉBUT ===")
    run_etl_dimensions()
    run_etl_fact_ventes_items()
    logger.info("=== ETL COMPLET OLIST - FIN ===")


def main():
    parser = argparse.ArgumentParser(description="ETL Olist DW")
    parser.add_argument(
        "--job",
        type=str,
        default="all",
        choices=[
            "all",
            "dimensions",
            "fact",
            "d_category",
            "d_product",
            "d_customer",
            "d_seller",
            "d_paymenttype",
            "d_orderstatus",
        ],
        help="Job ETL à exécuter",
    )
    args = parser.parse_args()

    if args.job == "all":
        run_etl_all()
    elif args.job == "dimensions":
        run_etl_dimensions()
    elif args.job == "fact":
        run_etl_fact_ventes_items()
    elif args.job == "d_category":
        run_etl_d_category()
    elif args.job == "d_product":
        run_etl_d_product()
    elif args.job == "d_customer":
        run_etl_d_customer()
    elif args.job == "d_seller":
        run_etl_d_seller()
    elif args.job == "d_paymenttype":
        run_etl_d_payment_type()
    elif args.job == "d_orderstatus":
        run_etl_d_order_status()
    else:
        raise ValueError(f"Job ETL invalide: {args.job}")


if __name__ == "__main__":
    main()
