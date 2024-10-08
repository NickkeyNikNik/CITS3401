USE [CITS3401-2023-1_22607943_Project1]
GO
 
-- Drop existing tables
 
IF OBJECT_ID('FactCrime', 'U') IS NOT NULL
 
    DROP TABLE FactCrime;
 
 
IF OBJECT_ID('DimNPU', 'U') IS NOT NULL
 
    DROP TABLE DimNPU;
 
 
IF OBJECT_ID('DimStreet', 'U') IS NOT NULL
 
    DROP TABLE DimStreet;
 
 
IF OBJECT_ID('DimCrime', 'U') IS NOT NULL
 
    DROP TABLE DimCrime;
 
 
IF OBJECT_ID('DimZone', 'U') IS NOT NULL
 
    DROP TABLE DimZone;
 
 
IF OBJECT_ID('DimDate', 'U') IS NOT NULL
 
    DROP TABLE DimDate;
 
 
-- Recreate tables
 
CREATE TABLE DimNPU (
 
    NPU_ID INT IDENTITY(1,1) PRIMARY KEY,
 
    country VARCHAR(50),
 
    city VARCHAR(50),
 
    npu CHAR(1),
 
    neighborhood VARCHAR(50)
 
);
 
 
CREATE TABLE DimStreet (
 
    STREET_ID INT IDENTITY(1,1) PRIMARY KEY,
 
    street VARCHAR(MAX)
 
);
 
 
CREATE TABLE DimCrime (
 
    CRIME_ID INT IDENTITY(1,1) PRIMARY KEY,
 
    crime VARCHAR(MAX),
 
    type VARCHAR(50),
 
    severity VARCHAR(50)
 
);
 
 
CREATE TABLE DimZone (
 
    ZONE_ID INT IDENTITY(1,1) PRIMARY KEY,
 
    zone VARCHAR(50),
 
    beat VARCHAR(50)
 
);
 
 
CREATE TABLE DimDate (
 
    DATE_ID INT IDENTITY(1,1) PRIMARY KEY,
 
    date VARCHAR(50),
 
    year VARCHAR(50),
 
    quarter VARCHAR(50),
 
    month VARCHAR(50)
 
);
 
 
CREATE TABLE FactCrime
 
(
 
  FactCrime_ID INT IDENTITY(1,1) PRIMARY KEY,
  STREET_ID INT,

  DATE_ID INT,
 
  ZONE_ID INT,
 
  CRIME_ID INT,
 
  NPU_ID INT,
 
  number VARCHAR(50)
 
);
 
GO
