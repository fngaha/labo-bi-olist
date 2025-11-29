USE Olist_DW;
GO

IF OBJECT_ID('dbo.D_PaymentType', 'U') IS NOT NULL
    DROP TABLE dbo.D_PaymentType;
GO

CREATE TABLE dbo.D_PaymentType
(
    PaymentType_SK INT IDENTITY(1,1) PRIMARY KEY,
    payment_type   VARCHAR(50) NOT NULL
);
GO
