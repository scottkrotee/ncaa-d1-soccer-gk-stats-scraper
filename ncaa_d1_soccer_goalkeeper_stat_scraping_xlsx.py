### Author: Scott Krotee - June, 2024 ###
 
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape top 50 NCAA goalkeeper stats
url = 'https://www.ncaa.com/stats/soccer-men/d1/current/individual/421'

def scrape_ncaa_soccer_stats(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming statistics are in a table - find the first table as an example
        stats_table = soup.find('table')
        if not stats_table:
            print("Statistics table not found.")
            return

        # Extract headers
        headers = [header.text.strip() for header in stats_table.find_all('th')]

        # Extract rows
        rows = []
        for row in stats_table.find_all('tr')[1:]:  # skip the header row
            cols = [ele.text.strip() for ele in row.find_all('td')]
            if cols:  # ensure the row has data
                rows.append(cols)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(rows, columns=headers)

        # Save the DataFrame to an Excel file
        df.to_excel('ncaa_d1_soccer_goalkeeper_stats.xlsx', index=False)
        print("Data successfully saved to Excel.")

    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
    except requests.RequestException as e:
        print(f'Request exception: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Call the function with the URL
scrape_ncaa_soccer_stats(url)
