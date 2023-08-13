# Data Analyzer

Author: <b>Pablo Duenas</b>
Date: <b>August 8, 2023</b>

## Description

The Data Analyzer is a data preprocessing and analysis tool designed to improve the quality and insightfulness of datasets. This python script can clean, process, and visualize data, making it a valuable tool for data exploration and preparation.

The key features of the Data Analyzer include:

1. **Outlier Removal:** Detects and removes outliers from numeric columns using the Interquartile Range (IQR) method.

2. **String Cleaning:** Converts all string data to lowercase, removes whitespace, and special characters.

3. **Optional Operations:** Allows users to choose from a set of optional operations, including converting negative values to 0 and removing specific columns.

4. **Basic Statistics:** Calculates basic statistics (mean, standard deviation, min, max, 25/50/75 percentiles) for numeric columns.

5. **Visualization:** Generates scatter plots, histograms, and box plots to visualize relationships in the data.

## Prerequisites

- Python 3.10
- Required Python libraries: pandas, matplotlib, seaborn

## Usage

1. Ensure that your dataset file (in CSV or Excel format) is placed in the 'Dataset' folder.

2. Run the `main()` function in the script to start the Data Analyzer.

3. Follow the interactive prompts to load your dataset, preprocess it, and perform optional operations.

4. View basic statistics and generate visualizations based on your preferences.

## Credits
- Example Dataset: [ds_salaries.csv](https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023) by RANDOMARNAB on Kaggle

## License
This project is licensed under the [MIT License](https://opensource.org/license/mit/).
