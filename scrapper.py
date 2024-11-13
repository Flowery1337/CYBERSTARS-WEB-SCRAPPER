import time
import sqlite3
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re

conn = sqlite3.connect('parking_prices.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS parking_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    parking_name TEXT,
    price REAL,
    rating TEXT,
    reviews TEXT,
    reservation_duration TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

def store_data(city, parking_name, price, rating, reviews, reservation_duration):
    cursor.execute('''INSERT INTO parking_prices (city, parking_name, price, rating, reviews, reservation_duration)
                      VALUES (?, ?, ?, ?, ?, ?)''', (city, parking_name, price, rating, reviews, reservation_duration))
    conn.commit()

def scrape_telpark(city):
    url = f"https://reserva.telpark.com/es/search?city={city}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        parkings = soup.find_all('div', class_='parking-info')
        for parking in parkings:
            name = parking.find('h3', class_='parking-name').text.strip()
            price_match = re.search(r'\d+\.\d+', parking.text)
            price = float(price_match.group()) if price_match else None
            rating = parking.find('span', class_='rating').text.strip() if parking.find('span', class_='rating') else 'N/A'
            reviews = parking.find('span', class_='reviews').text.strip() if parking.find('span', class_='reviews') else 'N/A'
            store_data(city, name, price, rating, reviews, '24-hour')
    else:
        print(f"Failed to retrieve data from Telpark for city {city}. Status code: {response.status_code}")

def scrape_parclick(city):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        url = f"https://parclick.es/search?q={city}"
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        parkings = soup.find_all('div', class_='parking')
        for parking in parkings:
            name = parking.find('div', class_='parking-name').text.strip()
            price = parking.find('div', class_='parking-price').text.strip().replace('EUR', '').strip()
            rating = parking.find('span', class_='rating').text.strip() if parking.find('span', class_='rating') else 'N/A'
            reviews = parking.find('span', class_='reviews').text.strip() if parking.find('span', class_='reviews') else 'N/A'
            store_data(city, name, float(price), rating, reviews, '24-hour')
    except Exception as e:
        print(f"Failed to retrieve data from Parclick for city {city}. Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    cities = ["Madrid", "Logro\u00f1o"]
    for city in cities:
        print(f"Scraping data for {city}...")
        scrape_telpark(city)
        scrape_parclick(city)
    print("Data scraping completed.")
    conn.close()
