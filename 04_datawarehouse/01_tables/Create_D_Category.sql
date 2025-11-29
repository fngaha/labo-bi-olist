USE Olist_DW;
GO

IF OBJECT_ID('dbo.D_Category', 'U') IS NOT NULL
    DROP TABLE dbo.D_Category;
GO

CREATE TABLE dbo.D_Category
(
    Category_SK INT IDENTITY(1,1) PRIMARY KEY,
    product_category_name VARCHAR(100) NOT NULL,
    product_category_name_english VARCHAR(100) NULL
);
GO
