USE Olist_DW;
GO

IF OBJECT_ID('dbo.D_Customer', 'U') IS NOT NULL
    DROP TABLE dbo.D_Customer;
GO

CREATE TABLE dbo.D_Customer
(
    Customer_SK              INT IDENTITY(1,1) PRIMARY KEY,
    customer_unique_id       VARCHAR(50)  NOT NULL,
    customer_id              VARCHAR(50)  NULL,  -- un ID représentatif (ex: le plus récent)
    customer_zip_code_prefix VARCHAR(20)  NULL,
    customer_city            VARCHAR(100) NULL,
    customer_state           VARCHAR(10)  NULL
    -- plus tard, on pourra ajouter latitude/longitude si on veut intégrer la géoloc
);
GO
