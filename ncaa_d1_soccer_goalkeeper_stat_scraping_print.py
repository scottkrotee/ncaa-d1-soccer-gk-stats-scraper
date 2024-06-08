import requests
from bs4 import BeautifulSoup

# URL to scrape top 50 ncaa goalkeeper stats
url = 'https://www.ncaa.com/stats/soccer-men/d1/current/individual/421'

def scrape_ncaa_soccer_stats(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming statistics are in a table - find the first table as an example
        # You'll need to inspect the actual page and adjust the selector as needed
        stats_table = soup.find('table')
        if not stats_table:
            print("Statistics table not found.")
            return

        # Extract and print the headers
        headers = [header.text for header in stats_table.find_all('th')]
        print(headers)

        # Extract and print each row of statistics
        for row in stats_table.find_all('tr')[1:]:  # skip the header row
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            print(cols)


    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
    except requests.RequestException as e:
        print(f'Request exception: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Call the function with the URL
scrape_ncaa_soccer_stats(url)
