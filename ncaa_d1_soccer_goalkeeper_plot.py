import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go

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
    
    # Convert relevant columns to numeric for plotting
    df['Saves'] = pd.to_numeric(df['Saves'], errors='coerce')
    df['Pct.'] = pd.to_numeric(df['Pct.'].str.rstrip('%'), errors='coerce')  # Remove '%' and convert to float

    ### Display Dark Mode Table Using Plotly ###
    def display_table(df):
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='black',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[df[col] for col in df.columns],
                       fill_color='darkslategray',
                       font=dict(color='white', size=11),
                       align='left'))
        ])

        fig.update_layout(
            title='Top NCAA Goalkeepers Stats (Dark Mode)',
            title_x=0.5,
            paper_bgcolor='black',
            font=dict(color='white')
        )
        fig.show()

    ### Scatter Plot Using Plotly ###
    def display_scatter(df):
        fig = go.Figure()

        # Create hover text using the available columns
        hover_text = [
            f"Name: {row['Name']}<br>Team: {row['Team']}<br>Saves: {row['Saves']}<br>GA: {row['GA']}<br>Minutes Played: {row['Goalie Min. Plyd']}<br>Save Pct: {row['Pct.']}"
            for i, row in df.iterrows()
        ]

        # Scatter plot with player names shown on the plot
        fig.add_trace(go.Scatter(
            x=df['Saves'], y=df['Pct.'], 
            mode='markers+text',  # markers and text
            marker=dict(size=10, color='blue', opacity=0.7, line=dict(width=2, color='white')),
            text=df['Name'],  # Display player name directly on the plot
            textposition='top center',  # Position text above the markers
            textfont=dict(color='white'),  # Text color
            hovertext=hover_text,  # Use custom hover text
            hoverinfo='text'  # Show only the hover text
        ))

        # Set plot background and styles
        fig.update_layout(
            title='Goalkeepers: Saves vs. Save Percentage',
            xaxis_title='Saves',
            yaxis_title='Save Percentage (%)',
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white')
        )

        fig.update_xaxes(showgrid=False, zeroline=False, color='white')
        fig.update_yaxes(showgrid=False, zeroline=False, color='white')

        fig.show()

    # Display the dark mode table
    display_table(df)

    # Display the scatter plot
    display_scatter(df)

else:
    print("No data to display.")
