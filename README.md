# NCAA D1 Soccer Goalkeeper Stats Scraper

This Python script scrapes the NCAA’s official website to gather statistics about Division 1 soccer goalkeepers. It processes data from multiple pages, saves it to a CSV file, and displays it in a dark-themed table and scatter plot using Plotly.

## Functionality

- Fetches the webpage containing the top 50 NCAA D1 goalkeeper stats.
- Parses the HTML to extract relevant data.
- Saves the data to an Excel file named `ncaa_d1_soccer_goalkeeper_stats.xlsx`.

## Dependencies

To run this script, you'll need Python installed on your system along with the following libraries:

- `requests` for performing HTTP requests.
- `BeautifulSoup` from `bs4` for parsing HTML content.
- `pandas` for data manipulation and exporting to Excel.

You can install these dependencies using pip:

pip install requests beautifulsoup4 pandas

## Output
Upon successful execution, the script will save the scraped data into an Excel file named ncaa_d1_soccer_goalkeeper_stats.xlsx in the same directory as the script. If there is an error during fetching or processing, the script will output an appropriate error message.

## Error Handling
The script includes basic error handling for HTTP errors and unexpected issues during the request or data processing phase. Specific error messages will be printed to the console.

## Limitations
The script assumes that the statistics are always presented in a table format. Changes to the website's layout or the data presentation format might require modifications to the script.
The script currently only fetches the data from the specified URL and does not support pagination or fetching from multiple pages.

## License
This script is provided "as is", without warranty of any kind, express or implied. Feel free to modify and use it as needed.
