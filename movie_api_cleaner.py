import pandas as pd


# DATA CLEANING SECTION ----------------------------------------------------------

def clean_movie_data(file_path):
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
        'Horror/Thriller/Crime/Mystery': ['Horror', 'Thriller', 'Crime', 'Mystery']
    }

    # Function to assign binary values based on genre groups
    def assign_genres(movie_genres, genres_to_check):
        return 1 if any(genre in movie_genres for genre in genres_to_check) else 0

    # Applying the function to create new binary columns
    for group, genres in genre_groups.items():
        data[group] = genre_split.apply(assign_genres, genres_to_check=genres)

    # # Removing records that do not belong to any of the specified genre groups
    # data = data[data[list(genre_groups.keys())].sum(axis=1) > 0]

    # Keep records that belong to any of the specified genre groups
    data = data[data[list(genre_groups.keys())].any(axis=1)]

    # Remove the original Genres column
    data = data.drop(columns=['Genres'])

    return data

# Clean the data
cleaned_data = clean_movie_data('api_moviedata/api_moviedata_uncleaned.csv')

# Save cleaned data to a new CSV
cleaned_data.to_csv('api_moviedata/api_moviedata_cleaned.csv', index=False)


print("Cleaned data saved to 'api_moviedata_cleaned.csv'")