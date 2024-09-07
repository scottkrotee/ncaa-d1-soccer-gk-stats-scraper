import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import math

# Base URL and page identifiers for top 50 NCAA goalkeeper stats
base_url = 'https://www.ncaa.com/stats/soccer-men/d1/current/individual/421/'
pages = ['p1', 'p2', 'p3']  # Page identifiers

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

# Initialize an empty list to collect all the data
all_rows = []
all_headers = None

# Loop through each page and scrape the data
for page in pages:
    url = base_url + page
    headers, rows = scrape_ncaa_soccer_stats(url)
    
    if headers and rows:
        all_headers = headers  # Save headers once
        all_rows.extend(rows)  # Collect rows from all pages

if all_headers and all_rows:
    # Create a DataFrame from the concatenated data
    df = pd.DataFrame(all_rows, columns=all_headers)
    
    # Save the DataFrame to a CSV file
    df.to_csv('ncaa_goalkeeper_stats.csv', index=False)
    print("Data saved to ncaa_goalkeeper_stats.csv")
    
    # Debugging: Print the columns to verify correct extraction
    print("Extracted columns:", df.columns)

    # Convert relevant columns to numeric for plotting
    df['Saves'] = pd.to_numeric(df['Saves'], errors='coerce')
    df['Pct.'] = pd.to_numeric(df['Pct.'].str.rstrip('%'), errors='coerce')  # Remove '%' and convert to float

    ### Pagination Function ###
    def display_paginated_table(df, rows_per_page=50):
        total_pages = math.ceil(len(df) / rows_per_page)
        
        for page in range(total_pages):
            start_row = page * rows_per_page
            end_row = start_row + rows_per_page
            df_chunk = df.iloc[start_row:end_row]  # Get the subset of the DataFrame

            fig, ax = plt.subplots(figsize=(18, 12))
            ax.axis('tight')
            ax.axis('off')

            # Create the table for the current chunk
            table = ax.table(cellText=df_chunk.values, colLabels=df_chunk.columns, cellLoc='center', loc='center')

            # Styling the table
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.5, 1.5)

            fig.patch.set_facecolor('black')
            ax.patch.set_facecolor('black')

            for (i, j), cell in table.get_celld().items():
                if i == 0:
                    cell.set_facecolor('#333333')
                    cell.set_fontsize(12)
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#E6E6E6' if i % 2 == 0 else '#F2F2F2')
                    cell.set_text_props(color='black')

            table.auto_set_column_width(col=list(range(len(df.columns))))
            for cell in table.get_celld().values():
                cell.set_edgecolor('white')
                cell.set_linewidth(1.5)

            plt.title(f'Top NCAA Goalkeepers Stats (Page {page + 1})', fontsize=20, color='white', pad=20)
            plt.show()

    # Call the function to display the table in paginated format
    display_paginated_table(df)

    ### Scatter Plot Visualization ###
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(df['Saves'], df['Pct.'], color='darkblue', edgecolor='white', s=100, alpha=0.75)

    # Annotate each point with the goalkeeper's name
    for i, row in df.iterrows():
        ax.annotate(row['Name'], (row['Saves'], row['Pct.']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

    # Set grid and labels for scatter plot
    ax.set_title('Goalkeepers: Saves vs. Save Percentage', fontsize=16)
    ax.set_xlabel('Saves', fontsize=12)
    ax.set_ylabel('Save Percentage (%)', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7)

    # Customize axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.tick_params(colors='grey', which='both')

    plt.show()

else:
    print("No data to display.")
