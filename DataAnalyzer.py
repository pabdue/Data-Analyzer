# ------------------------------------------------------------------------------
# Author: Pablo Duenas
# Date: August 8, 2023
# Description: This project is a data preprocessing and analysis tool that 
# provides features to remove outliers, clean string data, perform optional operations, 
# calculate basic statistics, and generate visualizations (scatter, histogram, boxplot).
# ------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def remove_outliers(df):
    # Create a copy of the DataFrame to avoid modifying the original
    df_cleaned = df.copy()

    # Iterate through columns to find which are numeric to detect outliers
    for column in df_cleaned.columns:
        # Find numeric dtype of column
        if pd.api.types.is_numeric_dtype(df_cleaned[column]):

            # Interquartile Range (IQR)
            Q1 = df_cleaned[column].quantile(0.25)
            Q3 = df_cleaned[column].quantile(0.75)
            IQR = Q3 - Q1

            # Outlier boundaries
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Remove outliers
            df_cleaned = df_cleaned[(df_cleaned[column] >= lower_bound) & (df_cleaned[column] <= upper_bound)]

    return df_cleaned

def clean_strings(column):
    # lowercase all Strings
    column = column.str.lower()
    # Remove whitespace
    column = column.str.strip()
    # Remove special characters
    column = column.str.replace('[^a-zA-Z0-9\s]', '', regex=True)
    return column

def optional_operations(df, file):
    # Create a copy of the DataFrame to avoid modifying the original
    df_final = df.copy()

    while True:
        # Options message 
        choice = int(input('\033[92m' + "\nEnter 0: Finish cleaning dataset\nEnter 1: Convert negative values to 0\nEnter 2: Remove a specific feature (column)\n" + '\033[0m'))
        match choice:
            case 0:
                # User-specified desired file format
                fileChoice = input('\033[92m' + "Would you like your dataset in csv or excel format?\nEnter csv or excel: " + '\033[0m')
                fileChoice = fileChoice.lower()
                match fileChoice:
                    # Save preprocessed dataset to CSV file
                    case 'csv':
                        cleanPath = 'Data-Analyzer/Cleaned_Dataset/{}_clean.csv'.format(file)
                        df_final.to_csv(cleanPath, index=False)

                        return df_final
                    # Save preprocessed dataset to Excel file
                    case 'excel':
                        cleanPath = 'Data-Analyzer/Cleaned_Dataset/{}_clean.xlsx'.format(file)
                        df_final.to_excel(cleanPath, index=False, sheet_name='Sheet1')

                        return df_final
                    case _:
                        print('\033[91m' + "\nInvalid choice, try again.\n" + '\033[0m')

            case 1:
                # Convert negative values to zero
                for column in df_final.columns:
                    # Find numeric dtype of column
                    if pd.api.types.is_numeric_dtype(df_final[column]):
                        # Replace negative values with zero
                        df_final[column] = df_final[column].apply(lambda x: 0 if x < 0 else x)

            case 2:
                # Remove user-specified column/feature
                features = '\033[93m' + "These are the features in your dataset:" + '\033[94m' + "\n{}\n" + '\033[0m'
                print(features.format(df_final.columns))
                try:
                    removeColumn = input('\033[92m' + "Which feature would you like to remove from the dataset? " + '\033[0m')
                    # Remove the specified column from the DataFrame
                    df_final = df_final.drop(removeColumn, axis=1)
                except:
                    print('\033[91m' + "\nInvalid choice, try again.\n" + '\033[0m')

            case _:
                print('\033[91m' + "\nInvalid choice, try again.\n" + '\033[0m')

def calculate_stats(df):
    # Select only the numeric columns
    numeric_columns = df.select_dtypes(include=['number'])

    # Calculate basic stats - mean, standard deviation, min, max, 25/50/75
    stats = numeric_columns.describe()
    return stats

def visualize(df, x_column, y_column, plot_type):
    if plot_type == 'scatter':
        sns.scatterplot(data=df, x=x_column, y=y_column)
        plt.show()
    elif plot_type == 'histogram':
        sns.histplot(data=df, x=x_column, y=y_column)
        plt.show()
    elif plot_type == 'boxplot':
        sns.boxplot(data=df, x=x_column, y=y_column)
        plt.show()
    else:
        print('\033[91m' + "Invalid plot type! Supported plots are 'scatter', 'histogram', 'boxplot'" + '\033[0m')

def main():
    # Intro message
    print("--------------------------------------------------")
    print('\033[94m' + "Welcome to Data Analyzer!" + '\033[0m')
    print('\033[93m' + "Note: Before proceeding, make sure your choosen dataset is in the 'Dataset' folder." + '\033[0m')
    print("--------------------------------------------------\n")

    # Retrieve file name and path
    fileName = input('\033[92m' + "Begin by entering your dataset's file name (incl. '.csv' or '.xlsx'):\n" + '\033[0m')
    path = "Data-Analyzer/Dataset/" 
    filePath = path + fileName

    # file format validation and creation of data frame
    try:
        if '.csv' in fileName:
            try:
                # Create data frame from csv 
                df = pd.read_csv(filePath)
            except(FileNotFoundError, UnicodeDecodeError):
                print('\033[91m' + "Error reading the dataset. Please check the file name and/or encoding." + '\033[0m')
        elif '.xlsx' in fileName:
            try:
                # Create data frame from excel
                sheet_name = input('\033[92m' + "Specify sheet name: " + '\033[0m')
                df = pd.read_excel(filePath, sheet_name=sheet_name)
            except:
                print('\033[91m' + "Error reading the dataset. Please check the file name and/or encoding." + '\033[0m')
        else:
            print('\033[91m' + "\nThis file format is not supported. Please try again with a CSV or Excel file." + '\033[0m')
    except:
        print('\033[93m' + "Try again." + '\033[0m')

    # Display number of rows before preprocessing
    numOfRows = df.shape[0]
    print('\033[93m' + "\nDataset was successfully loaded." + '\033[0m')
    print('\033[92m' + "Number of rows in the dataset: " + str(numOfRows) + '\033[0m')

    print("\n--------------------------------------------------")
    print('\033[1m' + "Data Preprocessing" + '\033[0m')
    print("--------------------------------------------------")

    # Drop rows with any missing values
    df = df.dropna()
    print('\033[93m' + "\nRows with missing values have been removed" + '\033[0m')

    # Drop outliers
    df = remove_outliers(df)
    print('\033[93m' + "\nOuliers have been removed" + '\033[0m')

    # Drop duplicate rows based on all columns
    df = df.drop_duplicates()
    print('\033[93m' + "\nDuplicate rows have been removed" + '\033[0m')

    # Display updated number of rows after removal of missing values, outliers, and duplicates
    updatedNumOfRows = df.shape[0]
    totalRowsRemoved = numOfRows - updatedNumOfRows
    print('\033[92m' + "\nUpdated number of rows in the dataset: " + str(updatedNumOfRows) + '\033[0m')
    print('\033[91m' + "Number of rows removed: " + str(totalRowsRemoved) + '\033[0m')

    # Remove whitespace and special characters. All Strings are lowercase
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = clean_strings(df[column])
    
    # Progress message for user
    print('\033[93m' + "\nWhitespace has been removed\n\nSpecial characters have been removed\n\nStrings have been lowercased\n" + '\033[0m')
    print('\033[93m' + "Here are optional operations you can conduct on the dataset or choose to finish preprocessing." + '\033[0m')
    
    # Final data frame after finishing preprocessing
    df = optional_operations(df, fileName)

    print("\n--------------------------------------------------")
    print('\033[1m' + "Statistical Summaries" + '\033[0m')
    print("--------------------------------------------------")

    # Display basic statistics on dataset
    stats = calculate_stats(df)
    print('\n', '\033[93m', 'Statistical summaries of numeric columns:\n\n', '\033[94m', stats, '\033[0m')

    print("\n--------------------------------------------------")
    print('\033[1m' + "Visualization" + '\033[0m')
    print("--------------------------------------------------")

    # Display preview of dataset
    print('\033[93m', "\nPreview of dataset:\n\n", '\033[94m', df.head(), '\033[0m\n')

    # Display features names
    print('\033[93m', "List of features:\n\n", '\033[94m', df.columns, '\033[0m\n')

    # Gather information from user to generate visualization
    plot_type = input('\033[92m' + "What kind of visual would you like to generate? (choices: 'scatter', 'histogram', 'boxplot'):\n" + '\033[0m')
    plot_type = plot_type.lower()
    x_column = input('\033[92m' + "What feature would you like to use for x:\n" + '\033[0m')
    y_column = input('\033[92m' + "What feature would you like to use for y:\n" + '\033[0m')

    visualize(df, x_column, y_column, plot_type)

if __name__ == "__main__":
    main()

