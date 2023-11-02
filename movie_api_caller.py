import pandas as pd
import requests
import time

# Function to extract unique movie titles from a CSV file
def get_unique_titles(file_path):
    df = pd.read_csv(file_path)
    return df['Number_1_Release'].unique()

# Getting unique titles from both UK and USA files
uk_titles = get_unique_titles('box_office_data_cleaned/box_office_cleaned_uk.csv')
usa_titles = get_unique_titles('box_office_data_cleaned/box_office_cleaned_usa.csv')

# Combining the titles and removing any duplicates
movie_titles = list(set(uk_titles).union(set(usa_titles)))

# Your TMDB API key
API_KEY = "592bde84a4420dce5cc06ea4587b161b"

# Endpoint for movie search
SEARCH_ENDPOINT = "https://api.themoviedb.org/3/search/movie"

# Endpoint for movie details
DETAILS_ENDPOINT = "https://api.themoviedb.org/3/movie/{}"

# Dictionary to store movie data
movie_data = {}

# Loop over unique movie titles
for title in movie_titles:
    if title not in movie_data:
        # Search for the movie on TMDB
        search_params = {
            "api_key": API_KEY,
            "query": title
        }
        search_response = requests.get(SEARCH_ENDPOINT, params=search_params).json()

        # If there are results, get details of the first result
        if search_response['results']:
            movie_id = search_response['results'][0]['id']
            details_response = requests.get(DETAILS_ENDPOINT.format(movie_id), params={"api_key": API_KEY}).json()

            # Extract desired data
            release_date = details_response.get('release_date', None)
            runtime = details_response.get('runtime', None)
            genres = ', '.join([genre['name'] for genre in details_response.get('genres', [])])
            revenue = details_response.get('revenue', None)

            # Store data in dictionary
            movie_data[title] = {
                "Release Date": release_date,
                "Runtime": runtime,
                "Genres": genres,
                "Revenue": revenue
            }

            # Wait for a moment to respect the rate limit
            print(movie_data)
            time.sleep(0.2)

# Convert dictionary to DataFrame
df_movie_data = pd.DataFrame.from_dict(movie_data, orient='index')

# Save to CSV
df_movie_data.to_csv('api_moviedata/api_moviedata_uncleaned.csv', index_label='Title')

# ... (your existing code for cleaning and saving the cleaned data)


#
# # DATA CLEANING SECTION ----------------------------------------------------------
#
# def clean_movie_data(file_path):
#     # Load the data from the CSV file
#     data = pd.read_csv(file_path)
#
#     # 1. Handling Missing Values: Remove rows where the 'Title' is missing
#     data = data.dropna(subset=['Title'])
#
#     # 2. Date Transformation: Convert 'Release Date' to datetime format
#     data['Release Date'] = pd.to_datetime(data['Release Date'], format='%Y-%m-%d', errors='coerce')
#
#     # 3. Duplicate Handling: Remove duplicate rows if any
#     data = data.drop_duplicates()
#
#     # 4. Genre Simplification and Binary Encoding
#
#     # Splitting genres by comma and stripping extra spaces
#     genre_split = data['Genres'].str.split(',').apply(lambda x: [genre.strip() for genre in x])
#
#     # Defining the genre groups
#     genre_groups = {
#         'Action/Adventure': ['Action', 'Adventure'],
#         'Drama': ['Drama'],
#         'Comedy': ['Comedy'],
#         'Science Fiction/Fantasy': ['Science Fiction', 'Fantasy'],
#         'Romance': ['Romance'],
#         'Horror/Thriller/Crime/Mystery': ['Horror', 'Thriller', 'Crime', 'Mystery']
#     }
#
#     # Function to assign binary values based on genre groups
#     def assign_genres(movie_genres, genres_to_check):
#         return 1 if any(genre in movie_genres for genre in genres_to_check) else 0
#
#     # Applying the function to create new binary columns
#     for group, genres in genre_groups.items():
#         data[group] = genre_split.apply(assign_genres, genres_to_check=genres)
#
#     # # Removing records that do not belong to any of the specified genre groups
#     # data = data[data[list(genre_groups.keys())].sum(axis=1) > 0]
#
#     # Keep records that belong to any of the specified genre groups
#     data = data[data[list(genre_groups.keys())].any(axis=1)]
#
#     # Remove the original Genres column
#     data = data.drop(columns=['Genres'])
#
#     return data
#
# # Clean the data
# cleaned_data = clean_movie_data('api_moviedata/api_moviedata_uncleaned.csv')
#
# # Save cleaned data to a new CSV
# cleaned_data.to_csv('api_moviedata/api_moviedata_cleaned.csv', index=False)
#
# print("Original data saved to 'api_moviedata_uncleaned.csv'")
# print("Cleaned data saved to 'api_moviedata_cleaned.csv'")


print("Original data saved to 'api_moviedata_uncleaned.csv'")