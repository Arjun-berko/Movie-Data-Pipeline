import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_and_save_data(base_url, start_year, end_year, uncleaned_filename):
    """
    Scrape box office data from a given URL pattern and range of years, then save to a CSV file.

    :param base_url: The URL pattern to scrape data from, with '{}' placeholder for the year.
    :param start_year: The starting year for the data scraping.
    :param end_year: The ending year for the data scraping (inclusive).
    :param uncleaned_filename: Path to the CSV file to save the scraped data.
    """
    master_data_list = []

    for year in range(start_year, end_year + 1):
        url = base_url.format(year)
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('tr')

            for row in rows[1:]:
                columns = row.find_all('td')
                number_1_release = columns[6].a.get_text() if columns[6].a else None
                weekend_number = columns[10].a.get_text() if columns[10].a else None

                master_data_list.append({
                    'Year': year,
                    'Number_1_Release': number_1_release,
                    'Weekend_Number': weekend_number
                })

        except requests.HTTPError as http_err:
            print(f"HTTP error for year {year}: {http_err}")
        except Exception as err:
            print(f"An error occurred for year {year}: {err}")

    try:
        df = pd.DataFrame(master_data_list)
        with open(uncleaned_filename, 'w', newline='', encoding='utf-8') as file:
            df.to_csv(file, index=False)
        print(f"Raw data saved to '{uncleaned_filename}'")
    except Exception as e:
        print(f"An error occurred while saving the file {uncleaned_filename}: {e}")

def main():
    base_url_uk = 'https://www.boxofficemojo.com/weekend/by-year/{}/?area=GB'
    base_url_usa = 'https://www.boxofficemojo.com/weekend/by-year/{}/'

    scrape_and_save_data(base_url_uk, 2002, 2023, 'box_office_data_uncleaned/box_office_uncleaned_uk.csv')
    scrape_and_save_data(base_url_usa, 2002, 2023, 'box_office_data_uncleaned/box_office_uncleaned_usa.csv')

if __name__ == "__main__":
    main()
