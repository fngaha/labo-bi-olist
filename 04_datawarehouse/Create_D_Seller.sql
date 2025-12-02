USE Olist_DW;
GO

IF OBJECT_ID('dbo.D_Seller', 'U') IS NOT NULL
    DROP TABLE dbo.D_Seller;
GO

CREATE TABLE dbo.D_Seller
(
    Seller_SK              INT IDENTITY(1,1) PRIMARY KEY,
    seller_id              VARCHAR(50)  NOT NULL,
    seller_zip_code_prefix VARCHAR(20)  NULL,
    seller_city            VARCHAR(100) NULL,
    seller_state           VARCHAR(10)  NULL
    -- plus tard, on peut ajouter latitude/longitude si on intègre la géoloc
);
GO
