import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_and_save_data(BASE_URL, uncleaned_filename):
    # List to store the scraped data from all years
    master_data_list = []

    # Loop over the range of years
    for year in range(2002, 2024):
        # Update the URL for the specific year
        URL = BASE_URL.format(year)

        # Send an HTTP request to the URL
        response = requests.get(URL)

        # If request was successful
        if response.status_code == 200:
            # Initialize BeautifulSoup object to parse the content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all rows in the table
            rows = soup.find_all('tr')

            # Iterate over rows to extract data
            for row in rows[1:]:  # Skip the header row
                columns = row.find_all('td')

                # Extract the number 1 release and weekend number
                number_1_release = columns[6].a.get_text() if columns[6].a else None
                weekend_number = columns[10].a.get_text() if columns[10].a else None

                # Append data to the master list
                master_data_list.append({'Year': year,
                                         'Number_1_Release': number_1_release,
                                         'Weekend_Number': weekend_number})

    # Convert master list of dictionaries to DataFrame
    df = pd.DataFrame(master_data_list)

    # Save raw data to CSV
    df.to_csv(uncleaned_filename, index=False)
    print(f"Raw data saved to '{uncleaned_filename}'")


# UK data
BASE_URL_UK = 'https://www.boxofficemojo.com/weekend/by-year/{}/?area=GB'
scrape_and_save_data(BASE_URL_UK, 'box_office_data_uncleaned/box_office_uncleaned_uk.csv')

# USA data
BASE_URL_USA = 'https://www.boxofficemojo.com/weekend/by-year/{}/'
scrape_and_save_data(BASE_URL_USA, 'box_office_data_uncleaned/box_office_uncleaned_usa.csv')
