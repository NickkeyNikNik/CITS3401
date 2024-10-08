USE [CITS3401-2023-1_22607943_Project1]
GO

/****** Object:  View [dbo].[vNestTable]    Script Date: 23/04/2023 8:36:57 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

 -- creating views for association rule mining

CREATE VIEW [dbo].[vNestTable] AS
SELECT DISTINCT DATE.[date], CRIME.[crime], CRIME.[type], CRIME.[severity], NPU.neighborhood
FROM [dbo].[FactCrime] AS FACT
LEFT JOIN [dbo].[DimDate] AS DATE ON FACT.DATE_ID = DATE.DATE_ID
LEFT JOIN [dbo].[DimCrime] AS CRIME ON FACT.CRIME_ID = CRIME.CRIME_ID
LEFT JOIN [dbo].[DimNPU] AS NPU ON FACT.NPU_ID = NPU.NPU_ID





GO


