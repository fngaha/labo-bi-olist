USE Olist_DW;
GO

IF OBJECT_ID('dbo.F_Ventes_Items', 'U') IS NOT NULL
    DROP TABLE dbo.F_Ventes_Items;
GO

CREATE TABLE dbo.F_Ventes_Items
(
    -- Clé technique
    Fact_SK INT IDENTITY(1,1) PRIMARY KEY,

    -- Clés étrangères vers dimensions
    Date_SK              INT NOT NULL,   -- date d'achat (order_purchase_timestamp)
    Product_SK           INT NOT NULL,
    Customer_SK          INT NOT NULL,
    Seller_SK            INT NOT NULL,
    PaymentType_SK       INT NULL,
    OrderStatus_SK       INT NOT NULL,

    -- Identifiants opérationnels
    order_id             VARCHAR(50) NOT NULL,
    order_item_id        INT NOT NULL,

    -- Mesures
    price                DECIMAL(10,2) NOT NULL,
    freight_value        DECIMAL(10,2) NOT NULL,
    quantity             INT NOT NULL,
    total_item_value     AS (price * quantity) PERSISTED,
    total_weight_g       INT NULL,

    -- Timestamps opérationnels (optionnel dans la fact)
    order_purchase_timestamp DATETIME NULL,
    order_delivered_customer_date DATETIME NULL
);
GO

-- FK: Date
ALTER TABLE dbo.F_Ventes_Items
  ADD CONSTRAINT FK_Fact_Date
  FOREIGN KEY (Date_SK)
  REFERENCES dbo.D_Date(Date_SK);
GO

-- FK: Product
ALTER TABLE dbo.F_Ventes_Items
  ADD CONSTRAINT FK_Fact_Product
  FOREIGN KEY (Product_SK)
  REFERENCES dbo.D_Product(Product_SK);
GO

-- FK: Customer
ALTER TABLE dbo.F_Ventes_Items
  ADD CONSTRAINT FK_Fact_Customer
  FOREIGN KEY (Customer_SK)
  REFERENCES dbo.D_Customer(Customer_SK);
GO

-- FK: Seller
ALTER TABLE dbo.F_Ventes_Items
  ADD CONSTRAINT FK_Fact_Seller
  FOREIGN KEY (Seller_SK)
  REFERENCES dbo.D_Seller(Seller_SK);
GO

-- FK: PaymentType
ALTER TABLE dbo.F_Ventes_Items
  ADD CONSTRAINT FK_Fact_PaymentType
  FOREIGN KEY (PaymentType_SK)
  REFERENCES dbo.D_PaymentType(PaymentType_SK);
GO

-- FK: OrderStatus
ALTER TABLE dbo.F_Ventes_Items
  ADD CONSTRAINT FK_Fact_OrderStatus
  FOREIGN KEY (OrderStatus_SK)
  REFERENCES dbo.D_OrderStatus(OrderStatus_SK);
GO
