# NCAA D1 Soccer Goalkeeper Stats Scraper
This Python script scrapes NCAA's official website to gather statistics about Division 1 soccer goalkeepers. It processes data from multiple pages, saves it to a CSV file, and displays it in a dark-themed table and scatter plot using Plotly.

## Functionality
- Web Scraping: Fetches goalkeeper stats from multiple pages of the NCAA's Division 1 men's soccer stats.
- Data Parsing: Parses the HTML to extract relevant statistics.
- Data Visualization:
    - Dark Mode Table: Displays goalkeeper stats in a dark-themed interactive table using Plotly.
    - Scatter Plot: Visualizes the relationship between goalkeeper saves and save percentage, with the player’s name displayed on the plot and detailed stats available on hover.
- CSV Export: Saves the gathered data into a CSV file named ncaa_goalkeeper_stats.csv.

## Features
- Pagination Support: The script now handles multiple pages (e.g., top 50 goalkeepers) by scraping data across different pages of the NCAA website.
- Dark Mode Visuals: Both the table and scatter plot are rendered in dark mode for a modern look using Plotly.
- Custom Hover Text: Detailed statistics (team, saves, goals against, minutes played, and save percentage) are available when hovering over the scatter plot points.

## Dependencies
To run this script, you will need Python installed on your system along with the following libraries:

requests: For performing HTTP requests.
BeautifulSoup from bs4: For parsing HTML content.
pandas: For data manipulation and CSV export.
plotly: For interactive visualizations (table and scatter plot).
You can install these dependencies using pip:

'''bash
pip install requests beautifulsoup4 pandas plotly
'''

## How to Run
1. Clone the repository or copy the script to your local machine.

2. Install the dependencies listed above.

3. un the Python script:

'''bash
python ncaa_d1_soccer_goalkeeper_stats_scraper.py
'''

4. Upon successful execution, the following will happen:

- The scraped data will be saved as ncaa_goalkeeper_stats.csv in the same directory as the script.
- The dark mode table and scatter plot will be displayed.

## Output
- CSV File: The script saves the goalkeeper stats into ncaa_goalkeeper_stats.csv.
- Dark Mode Table: A Plotly table in dark mode is displayed, showing the scraped goalkeeper stats.
- Scatter Plot: A scatter plot is displayed, showing each goalkeeper’s saves vs. save percentage, with player names visible on the plot and detailed stats available on hover.

## Error Handling
The script includes basic error handling for:
- HTTP Errors: If the webpage cannot be fetched, an appropriate error message is displayed.
- Missing Data: If the statistics table is not found on the page, the script will print a message indicating that no data is available.
- Other Exceptions: General exceptions are caught and handled gracefully with an error message.

## Limitations
- The script assumes that the statistics are always presented in a table format. If the website layout changes, modifications to the script may be required.
- Currently, the script only handles pages provided in the base URL and page identifiers.
- If the NCAA website changes its format or pagination structure, further adjustments will be needed.

## License
- This script is provided "as is", without warranty of any kind, express or implied. Feel free to modify and use it as needed.

## Example Visuals
- Dark Mode Table: Displays a sleek, modern table of goalkeeper stats.
- Scatter Plot: Visualizes saves vs. save percentage, with each goalkeeper’s name displayed above the corresponding data point.

## Summary of Updates:
- Pagination support added to fetch data from multiple pages.
- Dark mode added for both the table and scatter plot using Plotly.
- Data is saved in CSV format rather than Excel.
- New dependencies include plotly for enhanced visualizations.
