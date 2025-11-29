USE Olist_DW;
GO

IF OBJECT_ID('dbo.D_OrderStatus', 'U') IS NOT NULL
    DROP TABLE dbo.D_OrderStatus;
GO

CREATE TABLE dbo.D_OrderStatus
(
    OrderStatus_SK INT IDENTITY(1,1) PRIMARY KEY,
    order_status   VARCHAR(50) NOT NULL
    -- plus tard: status_label_fr, status_category si tu veux enrichir
);
GO
