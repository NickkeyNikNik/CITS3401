# CITS3401

# Crime Data Warehouse and Analysis - CITS3401 Project 1

This project involves the design and implementation of a crime data warehouse to analyze crime patterns based on crime severity and geographical zones. The project incorporates various stages of data warehousing, including concept hierarchy creation, schema design, fact and dimension table generation, and the application of ETL (Extract, Transform, Load) processes. Additionally, the project includes data mining techniques such as rule association mining to identify patterns and trends in crime data.

## Project Overview

The objective of this project is to create a crime data warehouse that allows for the efficient organization and querying of large datasets related to crime statistics. The data warehouse is structured around several key dimensions, such as crime type, crime severity, geographical zones, and time periods. This structure enables the user to perform complex queries to analyze crime patterns, crime severity distributions, and the relationships between various crime types across different regions.

The project covers the following key areas:
1. **Concept Hierarchy and Schema Design**: Crime types are organized into a hierarchy based on their severity (Low, Medium, High), enabling more effective analysis of crime trends.
2. **Fact and Dimension Tables**: These tables allow for the aggregation of data across multiple dimensions, such as time, location, and crime severity, making querying and analysis more efficient.
3. **ETL Processes**: A comprehensive ETL pipeline is implemented to clean and preprocess the raw data, ensuring that the data is ready for insertion into the data warehouse.
4. **Business Queries**: Various business intelligence queries are created to extract insights from the data, such as identifying the zones with the highest homicide rates or analyzing the distribution of crimes across different time periods.
5. **Association Rule Mining**: Rule mining is used to discover patterns and correlations between different types of crimes, providing insights into the likelihood of certain crimes occurring together.

## Key Components

### 1. Concept Hierarchy
The project utilizes a concept hierarchy to classify crimes into three categories: **Low**, **Medium**, and **High**. Crimes were ranked based on their potential harm and impact on society, with the most severe crimes such as homicide categorized as "High" and less severe crimes like larceny-non-vehicle categorized as "Low."

### 2. StarNet and Database Design
The design includes a StarNet model where crimes are organized into dimensions such as time, location (zones and streets), and crime severity. The dimension tables allow for detailed querying of the dataset, such as crime counts by zone or year.

### 3. Fact and Dimension Tables
The fact table stores the quantitative data of crimes, such as the number of occurrences, while the dimension tables store qualitative data, such as the crime type, date, and location. Foreign keys are used to link the fact table to its corresponding dimension tables.

### 4. ETL Processes
The ETL process cleans and transforms the raw crime data from multiple CSV files, removing irrelevant or malformed data and formatting the dataset for efficient loading into the data warehouse. This process ensures that the data adheres to the schema of the warehouse and is ready for analysis.

### 5. Business Intelligence Queries
The project includes several business intelligence queries that answer important questions about crime patterns. Examples include:
- **Crime Severity Analysis**: How many crimes fall under Low, Medium, and High categories?
- **Homicide Distribution by Zone**: Which zones have the highest number of homicides?
- **Quarterly Crime Distribution**: What is the percentage distribution of crimes across the four quarters of a year?

### 6. Association Rule Mining
Rule association mining is used to uncover relationships between different crimes. For instance, if a burglary and auto theft occur together, there is a high probability of a larceny occurring in the same region. The top 10 rules based on importance are identified to predict the likelihood of certain crimes happening together.

## ETL Process
The ETL process, implemented in a Python script (`ETL.py`), performs the following steps:
1. **Extract**: Raw crime data from multiple CSV files is loaded.
2. **Transform**: The data is cleaned by dropping irrelevant columns, fixing data inconsistencies, and replacing incorrect or missing data.
3. **Load**: The cleaned data is inserted into the fact and dimension tables of the database.

## Data Mining Process
The data mining process involves creating case and nested tables to explore the combinations of crimes that occur on specific dates. Rules are then generated based on this analysis to predict future crime occurrences based on historical data.

## Files in this Repository
- `ETL.py`: The Python script that implements the ETL process to clean and load the data into the database.
- `bulk_insert.sql`: The SQL script for performing bulk inserts into the fact and dimension tables.
- `crime_data.csv`: Example dataset used in this project.
- `project_report.pdf`: Detailed project report documenting the design, implementation, and results of the project.

## Requirements
- Python 3.x
- Pandas library
- SQL Server for database operations
- Data files (CSV format)

## Usage
1. Run the `ETL.py` script to process and clean the raw data.
2. Use the SQL scripts provided to bulk insert the data into the database.
3. Execute the provided business queries and rule mining processes to analyze the data.

## Conclusion
This project demonstrates the effective design and implementation of a data warehouse for crime data analysis. By utilizing concept hierarchies, dimension tables, and data mining techniques, this project provides valuable insights into crime patterns and trends, making it a useful tool for law enforcement and policy makers.

# Crime Data Analysis with Graph Databases - CITS3401 Project 2

This project is a continuation of the crime data analysis from Project 1 but with a focus on implementing a graph database to represent crime data. The project explores the design, implementation, and querying of a graph database, comparing its capabilities to traditional relational databases. The aim is to leverage the power of graph databases to explore relationships within the data and perform advanced analysis.

## Project Overview

The objective of this project is to transform the crime data warehouse, previously implemented using relational database techniques, into a graph database. This transition allows for better representation and analysis of interconnected data, such as the relationships between crimes, locations, and time periods. The project utilizes Neo4j for graph database implementation and focuses on designing an efficient graph structure using nodes and relationships. Additionally, Cypher queries are used to extract meaningful insights from the graph.

### Key Components:
1. **Graph Database Design**: The graph database was designed to represent crime data, with nodes representing entities like crimes, neighborhoods, streets, and years. Relationships represent the connections between these entities, such as crimes occurring in specific neighborhoods or during certain years.
2. **Graph Database Implementation**: Two approaches were considered for implementing the graph database:
   - Direct conversion of the existing data warehouse tables into graph nodes, labels, and properties.
   - Reprocessing the CSV files and adapting them to the graph database format.
   The second approach was chosen to optimize query performance by tailoring the graph database structure to specific queries.
3. **Cypher Queries**: Various Cypher queries were designed to explore the graph data and extract insights, such as crime patterns, neighborhood analysis, and crime rates over time.
4. **Graph Data Science**: Graph algorithms and analytics were applied to uncover hidden patterns and relationships in the data, providing deeper insights into crime trends.

## Graph Database Design

The graph database model uses nodes to represent entities such as:
- **Crime**: Individual crimes committed, categorized by type.
- **Year**: The year in which the crime occurred.
- **Neighborhood**: The geographic area where the crime took place.
- **Street and Beat**: Further geographic details within a neighborhood.

Relationships in the graph represent how these entities are connected. For example, a crime node is related to a neighborhood node by the "OCCURRED_IN" relationship, while a year node is connected to a crime node via the "OCCURRED_ON" relationship.

### Design Considerations:
- **Pros**:
  - Graph databases handle complex relationships efficiently, enabling fast querying and traversal of interconnected data.
  - The flexible schema of graph databases allows for easy addition of new nodes and relationships without impacting the existing data.
- **Cons**:
  - There is a learning curve for understanding graph database concepts and Cypher query language.
  - Deletion of nodes and relationships can be time-consuming in large datasets.

## ETL Process

The project includes an ETL (Extract, Transform, Load) process implemented in Python (`ETL.py`). This process extracts raw data from CSV files, transforms it into a format suitable for the graph database, and loads it into Neo4j. The fact table was adapted to fit the graph structure, with certain columns left in the fact table to serve as "measures" for creating relationships between nodes.

### Key Steps in ETL:
1. **Data Cleaning**: The raw CSV files are cleaned and transformed to ensure compatibility with the graph database.
2. **Data Loading**: Nodes and relationships are created using the Cypher `LOAD CSV` command, and larger datasets can be handled with APOC procedures for better performance.

## Graph Database Queries

Several Cypher queries were developed to analyze crime data and retrieve insights. Some examples include:
1. **Crime Type Query**: Retrieves the count of specific crimes in a neighborhood for a given time period.
2. **Neighborhood Comparison**: Identifies neighborhoods that share the same crime types and organizes them in descending order by the number of common crimes.
3. **Top 5 Neighborhoods**: Finds the top 5 neighborhoods with the highest occurrences of a specific crime type.
4. **Crime Patterns by Month**: Determines the month with the highest crime rate for each beat.
5. **Property Type Analysis**: Returns the types of crimes associated with different property types.

## Capabilities of Graph Databases vs. Relational Databases

Graph databases offer several advantages over relational databases, particularly in handling complex relationships:
- **Efficient Traversal**: Graph databases are optimized for traversing relationships, making queries involving multiple joins much faster compared to relational databases.
- **Flexible Schema**: Graph databases allow for dynamic schema changes, where new nodes and relationships can be added without affecting existing data.
- **Relationship Analysis**: Graph algorithms such as community detection and centrality measures provide deeper insights into the data by analyzing relationships and clusters.
- **Performance**: Graph databases scale better for large datasets with complex relationships, as they avoid the performance bottlenecks of multiple join operations in relational databases.

## Graph Data Science Applications

Graph Data Science techniques were applied to analyze crime patterns, identify clusters, and predict future trends:
1. **Crime Pattern Analysis**: Using graph algorithms like community detection and clustering, the project identifies patterns in crime data, such as groups of crimes that frequently occur together.
2. **Predictive Analysis**: Link prediction techniques are used to forecast potential crime hotspots based on historical data and neighborhood connections.
3. **Resource Allocation**: Insights from the graph database can help optimize resource allocation, such as targeting high-crime areas for law enforcement interventions.

## Files in this Repository
- `ETL.py`: Python script for the ETL process to clean and load the crime data into the graph database.
- `Cypher_queries.txt`: Collection of Cypher queries used for analyzing the graph database.
- `project_report.pdf`: Detailed report documenting the design, implementation, and results of the project.
- `crime_data.csv`: Example dataset used in the project.

## Requirements
- Python 3.x
- Neo4j database (with APOC procedures for large datasets)
- CSV files containing crime data

## Usage
1. Run the `ETL.py` script to clean and load the data into Neo4j.
2. Use the Cypher queries provided in `Cypher_queries.txt` to perform analysis and extract insights from the graph database.
3. Explore the graph visually using the Neo4j Browser.
