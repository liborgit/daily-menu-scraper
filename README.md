# Daily Menu Scraper

This script scrapes lunch menu data from a specified webpage and saves it as a JSON file. It's designed for a webpage that lists menu items with prices in a consistent format. The script will log actions and save the extracted menu data to a JSON file at the specified output path.

## Features

- Fetches menu data from URL using `requests` and `BeautifulSoup`.
- Extracts menu item names and prices.
- Cleans up and formats data for better readability.
- Removes unwanted text (`TARGET_STRING`) from extracted data.
- Saves extracted data to a JSON file.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Example JSON Output

```json
[
    {
        "Dish": "1. Example Dish Name",
        "Price": "99"
    },
    ...
]
```
