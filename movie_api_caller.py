import os
import pandas as pd
import requests
import time
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

def get_unique_titles(file_path):
    """
    Extract unique movie titles from a CSV file.

    :param file_path: Path to the CSV file.
    :return: A list of unique movie titles.
    """
    try:
        df = pd.read_csv(file_path)
        return df['Number_1_Release'].unique()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []


def fetch_movie_details(title, api_key):
    """
    Fetch movie details from TMDB API.

    :param title: The movie title.
    :param api_key: Your TMDB API key.
    :return: A dictionary with movie details or None if an error occurs.
    """
    search_params = {
        "api_key": api_key,
        "query": title
    }

    try:
        search_response = requests.get(SEARCH_ENDPOINT, params=search_params)
        search_response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        search_results = search_response.json()['results']

        if search_results:
            movie_id = search_results[0]['id']
            details_response = requests.get(DETAILS_ENDPOINT.format(movie_id), params={"api_key": api_key})
            details_response.raise_for_status()
            details_data = details_response.json()

            return {
                "Release Date": details_data.get('release_date'),
                "Runtime": details_data.get('runtime'),
                "Genres": ', '.join([genre['name'] for genre in details_data.get('genres', [])]),
                "Revenue": details_data.get('revenue')
            }
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"Other error occurred: {e}")
    return None


def save_data_to_csv(data, file_path):
    """
    Save the movie data to a CSV file.

    :param data: Dictionary containing movie data.
    :param file_path: Path to the CSV file to save the data.
    """
    try:
        df_movie_data = pd.DataFrame.from_dict(data, orient='index')
        df_movie_data.to_csv(file_path, index_label='Title')
        print(f"Original data saved to '{file_path}'")
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


if __name__ == "__main__":
    uk_titles = get_unique_titles('box_office_data_cleaned/box_office_cleaned_uk.csv')
    usa_titles = get_unique_titles('box_office_data_cleaned/box_office_cleaned_usa.csv')

    movie_titles = list(set(uk_titles) | set(usa_titles))

    API_KEY = os.getenv('TMDB_API_KEY')
    SEARCH_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
    DETAILS_ENDPOINT = "https://api.themoviedb.org/3/movie/{}"

    movie_data = {}

    for title in movie_titles:
        if title and title not in movie_data:
            details = fetch_movie_details(title, API_KEY)
            if details:
                movie_data[title] = details
                print(f"Fetched data for: {title}")
            time.sleep(0.2)

    save_data_to_csv(movie_data, 'api_moviedata/api_moviedata_uncleaned.csv')
