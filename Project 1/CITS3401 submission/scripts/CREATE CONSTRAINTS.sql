
ALTER TABLE [dbo].[FactCrime] ADD CONSTRAINT
FK_CRIME_ID FOREIGN KEY (CRIME_ID) REFERENCES [dbo].[DimCrime] (CRIME_ID);

ALTER TABLE [dbo].[FactCrime] ADD CONSTRAINT
FK_ZONE_ID FOREIGN KEY (ZONE_ID) REFERENCES [dbo].[DimZone] (ZONE_ID);

ALTER TABLE [dbo].[FactCrime] ADD CONSTRAINT
FK_NPU_ID FOREIGN KEY (NPU_ID) REFERENCES [dbo].[DimNPU] (NPU_ID);

ALTER TABLE [dbo].[FactCrime] ADD CONSTRAINT
FK_STREET_ID FOREIGN KEY (STREET_ID) REFERENCES [dbo].[DimStreet] (STREET_ID);

ALTER TABLE [dbo].[FactCrime] ADD CONSTRAINT
FK_DATE_ID FOREIGN KEY (DATE_ID) REFERENCES [dbo].[DimDate] (DATE_ID);

GO