import pandas as pd

def clean_movie_data(file_path):
    """
    Clean movie data from a CSV file.

    :param file_path: Path to the CSV file containing the movie data.
    :return: Cleaned pandas DataFrame.
    """
    try:
        # Load the data from the CSV file
        data = pd.read_csv(file_path)

        # 1. Handling Missing Values: Remove rows where the 'Title' is missing
        data = data.dropna(subset=['Title'])

        # 2. Date Transformation: Convert 'Release Date' to datetime format
        data['Release Date'] = pd.to_datetime(data['Release Date'], format='%Y-%m-%d', errors='coerce')

        # 3. Duplicate Handling: Remove duplicate rows if any
        data = data.drop_duplicates()

        # 4. Genre Simplification and Binary Encoding
        # Splitting genres by comma and stripping extra spaces
        genre_split = data['Genres'].str.split(',').apply(lambda x: [genre.strip() for genre in x])

        # Defining the genre groups
        genre_groups = {
            'Action/Adventure': ['Action', 'Adventure'],
            'Drama': ['Drama'],
            'Comedy': ['Comedy'],
            'Science Fiction/Fantasy': ['Science Fiction', 'Fantasy'],
            'Romance': ['Romance'],
            'Horror/Thriller/Crime/Mystery': ['Horror', 'Thriller', 'Crime', 'Mystery'],
            'Others': ['Animation', 'Documentary', 'Family', 'History', 'Music', 'War', 'Western']
        }

        # Function to assign binary values based on genre groups
        def assign_genres(movie_genres, genres_to_check):
            return 1 if any(genre in movie_genres for genre in genres_to_check) else 0

        # Applying the function to create new binary columns
        for group, genres in genre_groups.items():
            data[group] = genre_split.apply(assign_genres, genres_to_check=genres)

        # Keep records that belong to any of the specified genre groups
        data = data[data[list(genre_groups.keys())].any(axis=1)]

        # Remove the original Genres column
        data = data.drop(columns=['Genres'])

        return data

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except pd.errors.EmptyDataError:
        print(f"No data found in {file_path}.")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing the data from {file_path}.")
        return None
    except Exception as e:
        print(f"An error occurred during the cleaning process: {e}")
        return None

def save_cleaned_data(data, output_file):
    """
    Save the cleaned DataFrame to a CSV file.

    :param data: Cleaned pandas DataFrame.
    :param output_file: Path to the output CSV file.
    """
    if data is not None:
        try:
            data.to_csv(output_file, index=False)
            print(f"Cleaned data saved to '{output_file}'")
        except Exception as e:
            print(f"An error occurred while saving the file {output_file}: {e}")

def main():
    # Define the file paths
    input_file = 'api_moviedata/api_moviedata_uncleaned.csv'
    output_file = 'api_moviedata/api_moviedata_cleaned.csv'

    # Clean the data
    cleaned_data = clean_movie_data(input_file)

    # Save cleaned data to a new CSV
    save_cleaned_data(cleaned_data, output_file)

if __name__ == "__main__":
    main()
