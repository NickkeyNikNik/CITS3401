Use [CITS3401-2023-1_22607943_Project1]
:setvar SqlSamplesSourceDataPath "\\uniwa.uwa.edu.au\userhome\students3\22607943\CITS3401\CITS3401Project1\excelfiles\"
:setvar DatabaseName "CITS3401-2023-1_22607943_Project1"
 
BULK INSERT [dbo].[DimCrime] FROM '$(SqlSamplesSourceDataPath)DimCrime.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    KEEPIDENTITY,
    TABLOCK
);
 
BULK INSERT [dbo].[DimDate] FROM '$(SqlSamplesSourceDataPath)DimDate.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    KEEPIDENTITY,
    TABLOCK
);
 
BULK INSERT [dbo].[DimNPU] FROM '$(SqlSamplesSourceDataPath)DimNPU.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    KEEPIDENTITY,
    TABLOCK
);
BULK INSERT [dbo].[DimStreet] FROM '$(SqlSamplesSourceDataPath)DimStreet.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    KEEPIDENTITY,
    TABLOCK
);
 
BULK INSERT [dbo].[DimZone] FROM '$(SqlSamplesSourceDataPath)DimZone.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);
 
GO
