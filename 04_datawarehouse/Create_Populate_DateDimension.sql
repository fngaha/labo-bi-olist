/* ===========================================================
   Script : Create_Populate_DateDimension.sql
   Objet  : Créer et peupler la dimension D_Date
   Contexte : Labo BI Olist (période 2016–2018)
   =========================================================== */

-- (Optionnel) Pour avoir les noms de jours/mois en français
-- Si tu préfères en anglais, commente cette ligne
SET LANGUAGE French;
SET DATEFIRST 1; -- 1 = lundi

------------------------------------------------------------
-- 1. Suppression de la table si elle existe déjà
------------------------------------------------------------
IF OBJECT_ID('dbo.D_Date', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.D_Date;
END;
GO

------------------------------------------------------------
-- 2. Création de la table D_Date
------------------------------------------------------------
CREATE TABLE dbo.D_Date
(
    Date_SK            INT           NOT NULL PRIMARY KEY, -- AAAAMMJJ
    Date_Actual        DATE          NOT NULL,

    -- Composantes de date
    Year               SMALLINT      NOT NULL,
    Quarter            TINYINT       NOT NULL,
    Quarter_Name       VARCHAR(20)   NOT NULL,   -- ex: 'T1 2017'
    Month              TINYINT       NOT NULL,
    Month_Name         VARCHAR(20)   NOT NULL,   -- ex: 'janvier'
    Month_Year         CHAR(7)       NOT NULL,   -- ex: '2017-01'
    WeekOfYear         TINYINT       NOT NULL,   -- ISO ou standard

    DayOfMonth         TINYINT       NOT NULL,
    DayOfWeek          TINYINT       NOT NULL,   -- 1 = lundi (avec DATEFIRST 1)
    Day_Name           VARCHAR(20)   NOT NULL,   -- ex: 'lundi'

    -- Indicateurs
    IsWeekend          BIT           NOT NULL,
    IsMonthStart       BIT           NOT NULL,
    IsMonthEnd         BIT           NOT NULL,
    IsQuarterStart     BIT           NOT NULL,
    IsQuarterEnd       BIT           NOT NULL,
    IsYearStart        BIT           NOT NULL,
    IsYearEnd          BIT           NOT NULL
);
GO

------------------------------------------------------------
-- 3. Paramètres de plage de dates
--    Pour Olist : environ 2016-01-01 à 2018-12-31
------------------------------------------------------------
DECLARE @StartDate DATE = '2016-01-01';
DECLARE @EndDate   DATE = '2018-12-31';
DECLARE @CurrentDate DATE = @StartDate;

------------------------------------------------------------
-- 4. Boucle de peuplement
------------------------------------------------------------
WHILE @CurrentDate <= @EndDate
BEGIN
    DECLARE @DateKey       INT;
    DECLARE @Year          SMALLINT;
    DECLARE @Quarter       TINYINT;
    DECLARE @Month         TINYINT;
    DECLARE @DayOfMonth    TINYINT;
    DECLARE @DayOfWeek     TINYINT;
    DECLARE @WeekOfYear    TINYINT;

    SET @Year       = YEAR(@CurrentDate);
    SET @Quarter    = DATEPART(QUARTER, @CurrentDate);
    SET @Month      = MONTH(@CurrentDate);
    SET @DayOfMonth = DAY(@CurrentDate);
    SET @DayOfWeek  = DATEPART(WEEKDAY, @CurrentDate);
    SET @WeekOfYear = DATEPART(WEEK, @CurrentDate);    -- ou ISO_WEEK selon besoin

    -- Clé AAAAMMJJ
    SET @DateKey = (@Year * 10000) + (@Month * 100) + @DayOfMonth;

    INSERT INTO dbo.D_Date
    (
        Date_SK,
        Date_Actual,
        Year,
        Quarter,
        Quarter_Name,
        Month,
        Month_Name,
        Month_Year,
        WeekOfYear,
        DayOfMonth,
        DayOfWeek,
        Day_Name,
        IsWeekend,
        IsMonthStart,
        IsMonthEnd,
        IsQuarterStart,
        IsQuarterEnd,
        IsYearStart,
        IsYearEnd
    )
    VALUES
    (
        @DateKey,
        @CurrentDate,
        @Year,
        @Quarter,
        CONCAT('T', @Quarter, ' ', @Year),                            -- ex: 'T1 2017'
        @Month,
        DATENAME(MONTH, @CurrentDate),                                -- ex: 'janvier'
        CONCAT(@Year, '-', RIGHT('0' + CAST(@Month AS VARCHAR(2)), 2)), -- ex: '2017-01'
        @WeekOfYear,
        @DayOfMonth,
        @DayOfWeek,
        DATENAME(WEEKDAY, @CurrentDate),                              -- ex: 'lundi'
        CASE WHEN @DayOfWeek IN (6, 7) THEN 1 ELSE 0 END,             -- samedi/dimanche
        CASE WHEN @DayOfMonth = 1 THEN 1 ELSE 0 END,
        CASE WHEN @DayOfMonth = DAY(EOMONTH(@CurrentDate)) THEN 1 ELSE 0 END,
        CASE WHEN @Month IN (1, 4, 7, 10) AND @DayOfMonth = 1 THEN 1 ELSE 0 END,
        CASE WHEN @Month IN (3, 6, 9, 12)
                  AND @DayOfMonth = DAY(EOMONTH(@CurrentDate)) THEN 1 ELSE 0 END,
        CASE WHEN @Month = 1 AND @DayOfMonth = 1 THEN 1 ELSE 0 END,
        CASE WHEN @Month = 12 AND @DayOfMonth = 31 THEN 1 ELSE 0 END
    );

    SET @CurrentDate = DATEADD(DAY, 1, @CurrentDate);
END;
GO

------------------------------------------------------------
-- 5. Vérification rapide
------------------------------------------------------------
SELECT TOP 10 * FROM dbo.D_Date ORDER BY Date_Actual;

SELECT MIN(Date_Actual) AS MinDate, MAX(Date_Actual) AS MaxDate
FROM dbo.D_Date;
GO
