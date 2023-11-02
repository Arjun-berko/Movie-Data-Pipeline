import pandas as pd

def clean_and_save_data(uncleaned_filename, cleaned_filename):
    # Load the raw data
    df = pd.read_csv(uncleaned_filename)

    # Clean the data: Remove rows with missing values in the "Number_1_Release" column
    cleaned_df = df.dropna(subset=['Number_1_Release'])

    # Remove duplicate rows based on all columns
    cleaned_df = cleaned_df.drop_duplicates()

    # Save cleaned data to CSV
    cleaned_df.to_csv(cleaned_filename, index=False)
    print(f"Cleaned data saved to '{cleaned_filename}'")


# UK data
clean_and_save_data('box_office_data_uncleaned/box_office_uncleaned_uk.csv',
                    'box_office_data_cleaned/box_office_cleaned_uk.csv')

# USA data
clean_and_save_data('box_office_data_uncleaned/box_office_uncleaned_usa.csv',
                    'box_office_data_cleaned/box_office_cleaned_usa.csv')
