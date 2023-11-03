import pandas as pd

def clean_and_save_data(uncleaned_filename, cleaned_filename):
    """
    Clean box office data by removing rows with missing values and duplicates, then save to a CSV file.

    :param uncleaned_filename: Path to the CSV file containing the uncleaned data.
    :param cleaned_filename: Path to the CSV file to save the cleaned data.
    """
    try:
        # Load the raw data
        df = pd.read_csv(uncleaned_filename)

        # Clean the data: Remove rows with missing values in the "Number_1_Release" column
        cleaned_df = df.dropna(subset=['Number_1_Release'])

        # Remove duplicate rows based on all columns
        cleaned_df = cleaned_df.drop_duplicates()

        # Save cleaned data to CSV
        cleaned_df.to_csv(cleaned_filename, index=False)
        print(f"Cleaned data saved to '{cleaned_filename}'")
    except pd.errors.EmptyDataError:
        print(f"No data found in {uncleaned_filename}.")
    except FileNotFoundError:
        print(f"The file {uncleaned_filename} does not exist.")
    except pd.errors.ParserError:
        print(f"Error parsing the data from {uncleaned_filename}.")
    except Exception as e:
        print(f"An error occurred while cleaning the data: {e}")

def main():
    # Paths to the uncleaned and cleaned data files
    uncleaned_files = [
        'box_office_data_uncleaned/box_office_uncleaned_uk.csv',
        'box_office_data_uncleaned/box_office_uncleaned_usa.csv'
    ]
    cleaned_files = [
        'box_office_data_cleaned/box_office_cleaned_uk.csv',
        'box_office_data_cleaned/box_office_cleaned_usa.csv'
    ]

    for uncleaned, cleaned in zip(uncleaned_files, cleaned_files):
        clean_and_save_data(uncleaned, cleaned)

if __name__ == "__main__":
    main()
