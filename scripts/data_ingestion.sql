/*
    Bronze load: dpwh_flood_control_projects.csv -> bronze.dpwh_flood_control_projects
    Source file : UTF-8, no BOM, LF line endings, all fields double-quoted, header row, 22 columns, 9,855 data rows.
    Bronze rule : nothing is converted or cleaned here. Every column is NVARCHAR.
                  Cast to real types in silver (TRY_CAST).
    Note        : ApprovedBudgetForContract and ContractCost contain text such as
                  'Clustered with Contract ID 21FA0059' and 'MYCA with Project ID P00448930LZ',
                  which is why numeric columns fail to load.
*/

-- USE DataWarehouse;   -- <- put your database name here
-- GO

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'bronze')
    EXEC('CREATE SCHEMA bronze');
GO

IF OBJECT_ID('bronze.dpwh_flood_control_projects', 'U') IS NOT NULL
    DROP TABLE bronze.dpwh_flood_control_projects;
GO

CREATE TABLE bronze.dpwh_flood_control_projects (
    MainIsland                  NVARCHAR(50),
    Region                      NVARCHAR(100),
    Province                    NVARCHAR(100),
    LegislativeDistrict         NVARCHAR(150),
    Municipality                NVARCHAR(150),
    DistrictEngineeringOffice   NVARCHAR(150),
    ProjectId                   NVARCHAR(50),
    ProjectName                 NVARCHAR(1000),
    TypeOfWork                  NVARCHAR(200),
    FundingYear                 NVARCHAR(20),
    ContractId                  NVARCHAR(50),
    ApprovedBudgetForContract   NVARCHAR(200),
    ContractCost                NVARCHAR(200),
    ActualCompletionDate        NVARCHAR(50),
    Contractor                  NVARCHAR(500),
    ContractorCount             NVARCHAR(20),
    StartDate                   NVARCHAR(50),
    ProjectLatitude             NVARCHAR(50),
    ProjectLongitude            NVARCHAR(50),
    ProvincialCapital           NVARCHAR(100),
    ProvincialCapitalLatitude   NVARCHAR(50),
    ProvincialCapitalLongitude  NVARCHAR(50)
);
GO

TRUNCATE TABLE bronze.dpwh_flood_control_projects;
GO

BULK INSERT bronze.dpwh_flood_control_projects
FROM 'C:\Users\Precision\Documents\RAHUR DATA PROJECTS\DEP Project\data\raw\dpwh_flood_control_projects.csv'
WITH (
    FORMAT          = 'CSV',
    FIELDQUOTE      = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR   = '0x0a',
    FIRSTROW        = 2,
    CODEPAGE        = '65001',
    TABLOCK
);
GO

-- Sanity check: expect 9855 rows
SELECT COUNT(*) AS row_count FROM bronze.dpwh_flood_control_projects;


SELECT c.column_id, c.name, t.name AS data_type, c.max_length
FROM sys.columns c
JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('bronze.dpwh_flood_control_projects')
ORDER BY c.column_id;


-- checking the table inserts
SELECT * FROM bronze.dpwh_flood_control_projects
