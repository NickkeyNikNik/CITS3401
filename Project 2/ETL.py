"""
CITS3401 Project 2 ETL Script
Name: Nicodemus Ong
Student ID: 22607943
"""

import csv
import datetime
import os
import pandas as pd


def determining_severity(data):
    """
    Determine the severity level based on the data in the crime column.

    Args:
        data (str): Data in the second column.

    Returns:
        str: Severity level.
    """
    # Logic for determining severity level
    if data == "HOMICIDE" or data == "RAPE" or data == "AGG ASSAULT":  # Check if data matches high severity crimes
        return "High"
    elif data == "ROBBERY-PEDESTRIAN" or data == "ROBBERY-RESIDENCE" or data == "ROBBERY-COMMERCIAL" or data == "BURGLARY-RESIDENCE":  # Check if data matches medium severity crimes
        return "Medium"
    else:
        return "Low"  # If data does not match high or medium severity crimes, assign low severity


def delete_files():
    """
    Delete all existing csv files.
    """

    files_to_delete = ['DimNPU.csv', 'DimDate.csv', 'complete_data.csv',
                       'DimZone.csv', 'DimStreet.csv', 'DimCrime.csv',
                       'FactCrime.csv']
    """
    Deletes the specified files from the current directory.
    """
    for file in files_to_delete:
        if os.path.exists(file):  # Check if file exists
            os.remove(file)  # Remove the file
            print(f"{file} deleted successfully.")
        else:
            print(f"{file} does not exist.")
    print("===========================================================================================")


def remove_csv_headers(file_path):
    """
    Removes the headers from a CSV file.

    Args:
        file_path (str): The file path of the CSV file.

    Returns:
        None
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Write the DataFrame back to the CSV file without headers
    df.to_csv(file_path, index=False, header=False)

    print(f"Headers removed from {file_path}")


import random

def combine_files(folder_path, output_file):
    """
    Combine all provided csv file into a single file while cleaning and processing the data

    Args:
        data (folder_path, outer_file): Folder path where all the excel sheets are located, outer_file determines the name of the output file once processing and cleaning is done

    Returns:
        outer_file
    """

    # concatenate all the files together
    combined_df = None
    for file in os.listdir(folder_path):
        if file.endswith(".csv") and file != 'npu_clean.csv':
            file_path = os.path.join(folder_path, file)
            print(file_path)
            df = pd.read_csv(file_path)
            if combined_df is None:
                combined_df = df
            else:
                combined_df = pd.concat([combined_df, df], ignore_index=True)
    print(combined_df)

    # Open clean NPU file to replace existing NPU as it is broken, file generated from
    # https://citycouncil.atlantaga.gov/other/neighborhood-planning-unit
    clean_npu_df = pd.read_csv('npu_clean.csv')

    # Replace blank entries in 'neighbourhood_lookup' with neighborhood data from the same row
    combined_df['neighbourhood_lookup'].fillna(combined_df['neighborhood'], inplace=True)

    # Add new column "Severity", results based of crime committed
    combined_df['Severity'] = combined_df['crime'].apply(determining_severity)

    # Add new column "zone" based on data of beat || First digit of beat is the zone that that record belongs in
    combined_df['zone'] = combined_df['beat'].astype(str).str[0]

    # drop county cause its broken based on lab tutor JiChuYang recommendations. remove NPU as well as it will be added
    # back later. NPU is broken as well. Other columns has been dropped as well as it is irrelevant
    combined_df.drop(columns=['county', 'Unnamed: 0.1', 'Unnamed: 0', 'npu', 'location'], inplace=True)

    # Merge 'combined_df' with 'clean_npu_df' based on 'neighborhood' column
    combined_df = combined_df.merge(clean_npu_df[['neighborhood', 'npu']], on='neighborhood', how='inner')

    # Format the date to YYYY-MM-DD for SQL processing
    combined_df['date'] = pd.to_datetime(combined_df['date'], format='mixed').dt.strftime('%Y-%m-%d')

    # Replace all city values to Atlanta as to avoid error in data processing later on
    combined_df['city'] = 'Atlanta'

    # Drop remaining rows with missing values
    combined_df.dropna(inplace=True)

    # Reset the index after dropping rows with missing data
    combined_df.reset_index(drop=True, inplace=True)

    # Format crime number as int. by default, number is being formatted as a float
    combined_df['number'] = combined_df['number'].astype(int)

    # Formats the postcode section to ensure that all entries of a neighborhood has the same postcode
    # This is determined by taking the majority postcode, transform data after with transform keyword
    most_common_postcode = combined_df.groupby('neighbourhood_lookup')['postcode'].agg(
        lambda x: x.value_counts().index[0])
    combined_df['postcode'] = combined_df.groupby('neighbourhood_lookup')['postcode'].transform(
        lambda x: most_common_postcode[x.name]).astype(int)

    # declare pattern to check against street name. remove any entries that do not fit format
    pattern = r'^\d+$'

    # Apply the regular expression pattern to the 'street_name' column using str.replace()
    combined_df['road'] = combined_df['road'].str.replace(pattern, '', regex=True)

    # Rename the column 'road' to 'street' as it is more accurate
    combined_df.rename(columns={'road': 'street'}, inplace=True)

    # Filter the dataframe to include only lines from the year 2017
    # combined_df = combined_df.loc[combined_df['date'].str.startswith('2016')]

    # Get 1000 random lines from the filtered dataframe
    combined_df = combined_df.sample(n=1000, random_state=42)

    # Write the random lines to CSV file
    combined_df.to_csv(output_file, index=False)
    print("Written to CSV file:", output_file)

    # Verify data is cleaned and no blanks are left in the file
    blank_count = combined_df.isna().sum()
    total_rows = combined_df.shape[0]
    print("Total count of rows in the DataFrame: ", total_rows)
    # Print the result
    print(blank_count)



def npu_DIM():
    """
    Generate npu_DIM csv

    Returns:
        npu_DIM.csv file
    """

    df = pd.read_csv('complete_data.csv')

    # Drop duplicate rows based on 'country', 'city', 'npu', 'neighborhood' columns
    df.drop_duplicates(subset=['country', 'city', 'npu', 'neighborhood'], inplace=True)

    # Reset the index after dropping duplicates
    df.reset_index(drop=True, inplace=True)

    # Add a new column with sequential values in the format "1" to "n"
    num_entries = len(df)

    df['NPU_ID'] = [(i + 1) for i in range(num_entries)]

    # Extract country, city, npu, neighborhood columns and add in NPU_ID
    selected_columns = df[['NPU_ID', 'npu', 'neighborhood']].copy()

    # Export to CSV file
    selected_columns.to_csv('DimNPU.csv', index=False)

    # Print a message upon successful export
    print("CSV file exported successfully as npu_DIM.csv")


def date_DIM():
    """
    Generate date_DIM from 2009 till 2017 as data set sits in that range

    Returns:
        returns data.csv file
    """

    # Define the start and end dates
    start_date = datetime.date(2009, 1, 1)
    end_date = datetime.date(2017, 12, 31)

    # Calculate the total number of days between start and end date
    total_days = (end_date - start_date).days

    # Create a list to store the values
    dates_list = []

    # Loop through each day and append the current_date, date, year, quarter, month, day to the list
    for i in range((end_date - start_date).days + 1):
        date_ID = i + 1
        current_date = start_date + datetime.timedelta(days=i)
        date = current_date.strftime("%Y-%m-%d")
        year = current_date.year
        quarter = (current_date.month - 1) // 3 + 1
        month = current_date.strftime("%B")
        dates_list.append([date_ID, date, year, quarter, month])

    # Define the CSV file name
    csv_file = "DimDate.csv"

    # Write the dates to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DATE_ID', 'date', 'year', 'quarter', 'month'])
        writer.writerows(dates_list)

    print(f'Successfully generated dates to {csv_file}')


def zone_DIM():
    """
    Generate zone_DIM from the 'complete_data.csv' file

    Returns:
        None
    """

    # Read the 'complete_data.csv' file into a DataFrame
    df = pd.read_csv('complete_data.csv')

    # Drop duplicate rows based on 'beat' columns
    df.drop_duplicates(subset=['beat'], inplace=True)

    # Reset the index after dropping duplicates
    df.reset_index(drop=True, inplace=True)

    # Extract the first digit of the 'beat' column to create a new 'zone' column
    df['zone'] = df['beat'].astype(str).str[0]

    # Add a new column 'ZONE_ID' with sequential values from "1" to "n"
    num_entries = len(df)
    df['ZONE_ID'] = [(i + 1) for i in range(num_entries)]

    # Reorder the columns to have 'ZONE_ID' as the first column
    df = df[['ZONE_ID', 'zone', 'beat']]

    # Export the DataFrame to a CSV file named 'zone_DIM.csv' without index
    df.to_csv('DimZone.csv', index=False)

    # Print a message upon successful export
    print("CSV file exported successfully as zone_DIM.csv")


def street_DIM():
    """
    Generate street_DIM from the 'complete_data.csv' file

    Returns:
        None
    """

    # Read the 'complete_data.csv' file into a DataFrame
    df = pd.read_csv('complete_data.csv')

    # Drop duplicate rows based on 'street' column
    df.drop_duplicates(subset=['street'], inplace=True)

    # Reset the index after dropping duplicates
    df.reset_index(drop=True, inplace=True)

    # Add a new column 'STREET_ID' with sequential values from "1" to "n"
    num_entries = len(df)
    df['STREET_ID'] = [(i + 1) for i in range(num_entries)]

    # Extract only the 'STREET_ID' and 'street' columns into a new DataFrame
    selected_columns = df[['STREET_ID', 'street']].copy()

    # Convert 'STREET_ID' column to integer
    selected_columns['STREET_ID'] = selected_columns['STREET_ID'].astype(int)

    # Export the selected columns DataFrame to a CSV file named 'street_DIM.csv' without index
    selected_columns.to_csv('DimStreet.csv', index=False)

    # Print a message upon successful export
    print("CSV file exported successfully as street_DIM.csv")


def crimeInfo_DIM():
    """
    Generate crimeInfo_DIM from the 'complete_data.csv' file

    Returns:
        None
    """

    # Read the 'complete_data.csv' file into a DataFrame
    df = pd.read_csv('complete_data.csv')

    # Drop duplicate rows based on 'crime', 'type', 'Severity' columns
    df.drop_duplicates(subset=['crime', 'type', 'Severity'], inplace=True)

    # Reset the index after dropping duplicates
    df.reset_index(drop=True, inplace=True)

    # Add a new column 'CRIME_ID' with sequential values from "1" to "n"
    num_entries = len(df)
    df['CRIME_ID'] = [(i + 1) for i in range(num_entries)]

    # Extract only the 'CRIME_ID', 'crime', 'type', 'Severity' columns into a new DataFrame
    selected_columns = df[['CRIME_ID', 'crime', 'type', 'Severity']].copy()

    # Export the selected columns DataFrame to a CSV file named 'crimeInfo_DIM.csv' without index
    selected_columns.to_csv('DimCrime.csv', index=False)

    # Print a message upon successful export
    print("CSV file exported successfully as crimeInfo_DIM.csv")


def crimes_FACT():
    """
    Generate crimes_FACT from the 'crimeInfo_DIM.csv', 'zone_DIM.csv', 'npu_DIM.csv', 'dates_DIM.csv', and
    'complete_data.csv' files.

    Returns:
        None
    """

    # Open CSV files to be matched
    crimeInfo_df = pd.read_csv('DimCrime.csv')  # Read 'crimeInfo_DIM.csv' into a DataFrame
    zone_df = pd.read_csv('DimZone.csv')  # Read 'zone_DIM.csv' into a DataFrame
    npu_df = pd.read_csv('DimNPU.csv')  # Read 'npu_DIM.csv' into a DataFrame
    date_df = pd.read_csv('DimDate.csv')  # Read 'dates_DIM.csv' into a DataFrame
    street_df = pd.read_csv('DimStreet.csv')  # Read street_DIM.csv

    master_df = pd.read_csv('complete_data.csv')  # Read 'complete_data.csv' into a DataFrame

    # Replace 'NPU' column in master_df with 'ID' from npu_df by matching on 'country', 'city', 'npu', 'neighborhood'
    tmp_df = pd.merge(npu_df, master_df, on=['npu', 'neighborhood'], how='inner').drop(
        ['country', 'city', 'neighborhood'], axis=1)

    # Replace 'crime' and 'type' columns in tmp_df with 'ID' from crimeInfo_df by matching on 'crime', 'type', 'Severity'
    tmp_df = pd.merge(crimeInfo_df, tmp_df, on=['crime', 'type', 'Severity'], how='inner').drop(
        ['Severity'], axis=1)

    # Add 'ZONE_ID' column in tmp_df and populate with the first digit of 'beat' column from zone_df
    tmp_df = pd.merge(zone_df, tmp_df, on=['zone', 'beat'], how='inner').drop(['beat'], axis=1)

    # Replace 'Date' column in tmp_df with 'ID' from date_df by matching on 'date'
    tmp_df = pd.merge(date_df, tmp_df, on=['date'], how='inner')
    # Replace road with ID
    tmp_df = pd.merge(street_df, tmp_df, on=['street'], how='inner').drop(['street'], axis=1)
    # Drop unwanted columns from tmp_df

    tmp_df = tmp_df.drop(['lat', 'long', 'neighbourhood_lookup', 'state', 'postcode'], axis=1)

    # Write tmp_df to a new CSV file named 'crime_FACT.csv' without index
    tmp_df.to_csv('FactCrime.csv', index=False)

    # Print a message upon successful export
    print("CSV file exported successfully for crime_FACT table")


def execute():
    # Input folder path containing CSV files
    folder_path = "/Users/nathanielong/Desktop/CIT3401_PROJECT_2"
    # Output CSV file name
    output_file = "complete_data.csv"

    # Call the function to delete existing CSV files
    delete_files()

    # Call functions to combine files, clean and transform data, and write to CSV
    combine_files(folder_path, output_file)  # Combine CSV files and create complete_data.csv
    npu_DIM()  # Clean and transform data for npu_DIM.csv
    date_DIM()  # Clean and transform data for dates_DIM.csv
    crimeInfo_DIM()  # Clean and transform data for crimeInfo_DIM.csv
    zone_DIM()  # Clean and transform data for zone_DIM.csv
    street_DIM()  # Clean and transform data for street_DIM.csv
    crimes_FACT()  # Clean and transform data for crime_FACT.csv

    # # Call functions to remove headers from CSV files
    # remove_csv_headers('complete_data.csv')  # Remove header from complete_data.csv
    # remove_csv_headers('npu_DIM.csv')  # Remove header from npu_DIM.csv
    # remove_csv_headers('dates_DIM.csv')  # Remove header from dates_DIM.csv
    # remove_csv_headers('crimeInfo_DIM.csv')  # Remove header from crimeInfo_DIM.csv
    # remove_csv_headers('zone_DIM.csv')  # Remove header from zone_DIM.csv
    # remove_csv_headers('street_DIM.csv')  # Remove header from street_DIM.csv
    # remove_csv_headers('crime_FACT.csv')  # Remove header from crime_FACT.csv

    print(
        "Data processing has been done successfully. all 6 files has been generated with headers removed and keys replaced")


execute()
