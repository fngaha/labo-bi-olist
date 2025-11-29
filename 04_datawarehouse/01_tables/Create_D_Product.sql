USE Olist_DW;
GO

IF OBJECT_ID('dbo.D_Product', 'U') IS NOT NULL
    DROP TABLE dbo.D_Product;
GO

CREATE TABLE dbo.D_Product
(
    Product_SK                 INT IDENTITY(1,1) PRIMARY KEY,
    product_id                 VARCHAR(50)  NOT NULL,
    Category_SK                INT          NULL,  -- FK vers D_Category
    product_category_name      VARCHAR(100) NULL,
    product_name_lenght        INT          NULL,
    product_description_lenght INT          NULL,
    product_photos_qty         INT          NULL,
    product_weight_g           INT          NULL,
    product_length_cm          INT          NULL,
    product_height_cm          INT          NULL,
    product_width_cm           INT          NULL
);

-- Optionnel : FK vers D_Category si tu veux renforcer l'intégrité
ALTER TABLE dbo.D_Product
  ADD CONSTRAINT FK_D_Product_D_Category
  FOREIGN KEY (Category_SK) REFERENCES dbo.D_Category(Category_SK);
GO
