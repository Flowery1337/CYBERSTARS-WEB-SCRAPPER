# README.md

# Parking Price Simplr Scraper for contest

## Overview
This Python script scrapes parking price information from two specific websites, Telpark and Parclick, for selected cities in Spain. The data extracted includes parking names, prices, ratings, and reviews for 24-hour reservations. The data is stored in an SQLite database for easy access and analysis.

## Features
- Extracts parking price information for cities specified by the user.
- Scrapes data from two parking websites: Telpark and Parclick.
- Saves parking details such as price, rating, and reviews into an SQLite database.
- Easy to modify list of cities to scrape.

## Requirements
To run this script, you will need the following Python libraries:
- `beautifulsoup4`: For parsing the HTML content.
- `selenium`: For scraping dynamic content rendered by JavaScript.
- `requests`: For making HTTP requests.
- `webdriver-manager`: To automatically manage browser drivers.
- `sqlite3`: For local database storage.

You can install all required packages using:
```sh
pip install -r requirements.txt
```

## Setup
1. Make sure Python 3.x is installed on your system.
2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To run the scraper:
1. Modify the list of cities in the script as per your requirement.
2. Run the script:
    ```sh
    python scraper.py
    ```

The script will collect parking data and store it in a SQLite database named `parking_prices.db`.

## Output
- The data scraped from the websites will be saved in `parking_prices.db` with the following fields:
  - `city`: The city name.
  - `parking_name`: Name of the parking.
  - `price`: Price for 24-hour reservations.
  - `rating`: User rating (if available).
  - `reviews`: User reviews (if available).
  - `reservation_duration`: Duration of reservation (currently set to '24-hour').

## Notes
- The scraper includes a waiting time (`time.sleep(5)`) to ensure the dynamic content is loaded completely by the browser.
- Make sure you have a stable internet connection, as Selenium uses a web browser to load content dynamically.

## Disclaimer
This script is for educational purposes only. Please make sure to comply with the terms and conditions of the websites being scraped.
