### Author: Scott Krotee - July 23rd, 2024 ###

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
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

        # Find the table containing the statistics
        stats_table = soup.find('table')
        if not stats_table:
            print("Statistics table not found.")
            return None, None

        # Extract headers
        headers = [header.text.strip() for header in stats_table.find_all('th')]

        # Extract rows
        rows = []
        for row in stats_table.find_all('tr')[1:]:  # skip the header row
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            rows.append(cols)
        
        return headers, rows

    except requests.HTTPError as e:
        print(f'HTTP Error occurred: {e.response.status_code}')
        return None, None
    except requests.RequestException as e:
        print(f'Request exception: {e}')
        return None, None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None

# Call the function with the URL
headers, rows = scrape_ncaa_soccer_stats(url)

if headers and rows:
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(rows, columns=headers)
    
    # Debugging: Print the columns to verify correct extraction
    print("Extracted columns:", df.columns)

    # Convert relevant columns to numeric for plotting
    df['Saves'] = pd.to_numeric(df['Saves'], errors='coerce')
    df['Pct.'] = pd.to_numeric(df['Pct.'].str.rstrip('%'), errors='coerce')  # Remove '%' and convert to float

    # Plotting the table using Matplotlib
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('tight')
    ax.axis('off')

    # Create table with the DataFrame values
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Styling the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Set table background color
    fig.patch.set_facecolor('black')
    ax.patch.set_facecolor('black')

    # Set the color of the cells
    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_facecolor('grey')
            cell.set_fontsize(12)
            cell.set_text_props(weight='bold', color='white')
        else:
            cell.set_facecolor('lightgrey' if i % 2 == 0 else 'darkgrey')
            cell.set_text_props(color='black')

    # Set the color of the lines
    table.auto_set_column_width(col=list(range(len(headers))))
    for cell in table.get_celld().values():
        cell.set_edgecolor('white')
        cell.set_linewidth(1.5)

    plt.show()

    # Plotting the scatter plot of Saves vs. Save Percentage with goalkeeper names
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Saves'], df['Pct.'], color='blue')

    for i, row in df.iterrows():
        ax.annotate(row['Name'], (row['Saves'], row['Pct.']), textcoords="offset points", xytext=(0,10), ha='center')

    ax.set_title('Goalkeepers: Saves vs. Save Percentage')
    ax.set_xlabel('Saves')
    ax.set_ylabel('Save Percentage')
    plt.grid(True)
    plt.show()
else:
    print("No data to display.")
