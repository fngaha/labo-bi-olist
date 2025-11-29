from .extract_staging import (
    extract_categories,
    extract_products,
    extract_customers,
    extract_sellers,
    extract_order_payments,
    extract_orders,
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
from .extract_dw import read_d_category
# plus tard: from .transform_facts import build_fact_ventes_items
# plus tard: from .load_facts import load_fact_ventes_items


def run_etl_d_category():
    print("ETL D_Category - démarrage...")

    categories = extract_categories()
    print(f"EXTRACT: {len(categories)} lignes lues depuis product_category_name_translation.")

    dim_category = build_d_category(categories)
    print(f"TRANSFORM: {len(dim_category)} catégories distinctes construites.")

    load_d_category(dim_category, truncate=True)
    print("LOAD: D_Category chargée dans Olist_DW.")


def run_etl_d_product():
    print("ETL D_Product - démarrage...")

    # 1. EXTRACT
    products = extract_products()
    print(f"EXTRACT: {len(products)} produits lus depuis products (staging).")

    dim_category_dw = read_d_category()
    print(f"EXTRACT: {len(dim_category_dw)} lignes lues depuis D_Category (DW).")

    # 2. TRANSFORM
    dim_product = build_d_product(products, dim_category_dw)
    print(f"TRANSFORM: {len(dim_product)} produits dimensionnels construits.")

    # 3. LOAD
    load_d_product(dim_product, truncate=True)
    print("LOAD: D_Product chargée dans Olist_DW.")


def run_etl_d_customer():
    print("ETL D_Customer - démarrage...")

    customers = extract_customers()
    print(f"EXTRACT: {len(customers)} lignes lues depuis customers (staging).")

    dim_customer = build_d_customer(customers)
    print(f"TRANSFORM: {len(dim_customer)} clients dimensionnels construits "
          f"(1 ligne par customer_unique_id).")

    load_d_customer(dim_customer, truncate=True)
    print("LOAD: D_Customer chargée dans Olist_DW.")


def run_etl_d_seller():
    print("ETL D_Seller - démarrage...")

    sellers = extract_sellers()
    print(f"EXTRACT: {len(sellers)} lignes lues depuis sellers (staging).")

    dim_seller = build_d_seller(sellers)
    print(f"TRANSFORM: {len(dim_seller)} vendeurs dimensionnels construits.")

    load_d_seller(dim_seller, truncate=True)
    print("LOAD: D_Seller chargée dans Olist_DW.")


def run_etl_d_payment_type():
    print("ETL D_PaymentType - démarrage...")

    order_payments = extract_order_payments()
    print(f"EXTRACT: {len(order_payments)} lignes lues depuis order_payments (staging).")

    dim_payment_type = build_d_payment_type(order_payments)
    print(f"TRANSFORM: {len(dim_payment_type)} types de paiement distincts construits.")

    load_d_payment_type(dim_payment_type, truncate=True)
    print("LOAD: D_PaymentType chargée dans Olist_DW.")


def run_etl_d_order_status():
    print("ETL D_OrderStatus - démarrage...")

    orders = extract_orders()
    print(f"EXTRACT: {len(orders)} lignes lues depuis orders (staging).")

    dim_order_status = build_d_order_status(orders)
    print(f"TRANSFORM: {len(dim_order_status)} statuts de commande distincts construits.")

    load_d_order_status(dim_order_status, truncate=True)
    print("LOAD: D_OrderStatus chargée dans Olist_DW.")


def run_etl_dimensions_only():
    """
    Pipeline ETL pour les dimensions uniquement (première étape).
    """
    print("ETL - Démarrage (dimensions)...")

    # 1. EXTRACT
    staging = extract_all_staging()
    print("EXTRACT terminé.")

    # 2. TRANSFORM
    dims = build_all_dimensions(staging)
    print("TRANSFORM des dimensions terminé.")

    # 3. LOAD
    load_all_dimensions(dims)
    print("LOAD des dimensions terminé.")


if __name__ == "__main__":
    # run_etl_d_category()
    #run_etl_d_product()
    #run_etl_d_customer()
    #run_etl_d_seller()
    #run_etl_d_payment_type()
    #run_etl_d_order_status()
    run_etl_dimensions_only()
