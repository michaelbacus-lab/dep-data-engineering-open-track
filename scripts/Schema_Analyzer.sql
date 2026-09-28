SELECT * FROM bronze.dpwh_flood_control_projects;

-- Analyzer: runs per-column stats for a table
DECLARE @schema SYSNAME = N'bronze';
DECLARE @table  SYSNAME = N'dpwh_flood_control_projects';

DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql = @sql +
'SELECT ' + QUOTENAME(c.name,'''') + ' AS ColumnName,
       COUNT(*) AS TotalRows,
       SUM(CASE WHEN [' + c.name + '] IS NULL THEN 1 ELSE 0 END) AS NullCount,
       MAX(LEN(CAST([' + c.name + '] AS nvarchar(max)))) AS MaxLen,
       MIN(LEN(CAST([' + c.name + '] AS nvarchar(max)))) AS MinLen,
       SUM(CASE WHEN TRY_CAST([' + c.name + '] AS bigint) IS NOT NULL THEN 1 ELSE 0 END) AS IntCount,
       SUM(CASE WHEN TRY_CAST([' + c.name + '] AS float) IS NOT NULL THEN 1 ELSE 0 END) AS FloatCount,
       SUM(CASE WHEN TRY_CAST([' + c.name + '] AS date) IS NOT NULL THEN 1 ELSE 0 END) AS DateCount,
       COUNT(DISTINCT [' + c.name + ']) AS DistinctCount
FROM ' + QUOTENAME(@schema) + '.' + QUOTENAME(@table) + '
UNION ALL
'
FROM sys.columns c
JOIN sys.tables t ON c.object_id = t.object_id
JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE s.name = @schema AND t.name = @table
ORDER BY c.column_id;

-- remove trailing UNION ALL
IF LEN(@sql) > 0 SET @sql = LEFT(@sql, LEN(@sql) - LEN('UNION ALL'));

PRINT '--- Executing per-column diagnostics ---';
EXEC sp_executesql @sql;