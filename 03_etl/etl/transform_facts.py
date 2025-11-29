import pandas as pd


def build_fact_ventes_items(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    order_payments: pd.DataFrame,
    products: pd.DataFrame,
    customers: pd.DataFrame,
    sellers: pd.DataFrame,
    d_date: pd.DataFrame,
    d_product: pd.DataFrame,
    d_customer: pd.DataFrame,
    d_seller: pd.DataFrame,
    d_payment_type: pd.DataFrame,
    d_order_status: pd.DataFrame,
) -> pd.DataFrame:
    """
    Construit la table de faits F_Ventes_Items à partir :
    - des tables de staging (orders, order_items, etc.)
    - des dimensions du DW (D_Date, D_Product, ...)

    Grain : 1 ligne par (order_id, order_item_id).
    """

    # 1) Base : order_items + orders
    base = order_items.merge(
        orders[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
                "order_delivered_customer_date",
            ]
        ],
        on="order_id",
        how="left",
        suffixes=("", "_order"),
    )

    # 2) Ajouter le customer_unique_id via customers
    base = base.merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left",
    )

    # 3) Ajouter le poids du produit via products
    base = base.merge(
        products[["product_id", "product_weight_g"]],
        on="product_id",
        how="left",
    )

    # 4) Ajouter les infos seller (pour être sûr qu'on a seller_id cohérent)
    base = base.merge(
        sellers[["seller_id"]],
        on="seller_id",
        how="left",
    )

    # 5) Paiement principal : payment_sequential = 1
    payments_sorted = order_payments.sort_values(
        ["order_id", "payment_sequential"]
    )
    payments_main = payments_sorted.drop_duplicates(
        subset=["order_id"], keep="first"
    )
    payments_main = payments_main[["order_id", "payment_type"]]

    base = base.merge(
        payments_main,
        on="order_id",
        how="left",
    )

    # 6) Cast des timestamps et dérivation de la date d'achat (pour D_Date)
    base["order_purchase_timestamp"] = pd.to_datetime(
        base["order_purchase_timestamp"]
    )
    base["order_delivered_customer_date"] = pd.to_datetime(
        base["order_delivered_customer_date"]
    )

    base["order_purchase_date"] = base["order_purchase_timestamp"].dt.date

    # 7) Préparation D_Date (on s'assure que Date_Actual est en date pure)
    d_date = d_date.copy()
    d_date["Date_Actual"] = pd.to_datetime(d_date["Date_Actual"]).dt.date

    base = base.merge(
        d_date[["Date_SK", "Date_Actual"]],
        left_on="order_purchase_date",
        right_on="Date_Actual",
        how="left",
    )

    # 8) Lookups SK vers les dimensions

    # Product_SK
    base = base.merge(
        d_product[["Product_SK", "product_id"]],
        on="product_id",
        how="left",
    )

    # Customer_SK
    base = base.merge(
        d_customer[["Customer_SK", "customer_unique_id"]],
        on="customer_unique_id",
        how="left",
    )

    # Seller_SK
    base = base.merge(
        d_seller[["Seller_SK", "seller_id"]],
        on="seller_id",
        how="left",
    )

    # PaymentType_SK
    base = base.merge(
        d_payment_type[["PaymentType_SK", "payment_type"]],
        on="payment_type",
        how="left",
    )

    # OrderStatus_SK
    base = base.merge(
        d_order_status[["OrderStatus_SK", "order_status"]],
        on="order_status",
        how="left",
    )

    # 9) Mesures
    base["quantity"] = 1
    base["total_weight_g"] = base["product_weight_g"] * base["quantity"]

    # 10) Construction de la DataFrame finale pour la fact
    fact = base[
        [
            "Date_SK",
            "Product_SK",
            "Customer_SK",
            "Seller_SK",
            "PaymentType_SK",
            "OrderStatus_SK",
            "order_id",
            "order_item_id",
            "price",
            "freight_value",
            "quantity",
            "total_weight_g",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
        ]
    ].copy()

    return fact
