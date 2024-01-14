import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def get_temperature():
    url = "https://meteofor.com.ua/weather-ternopil-4951/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    temperature_element = soup.find("/html/body/section/div[1]/section[2]/div/a[1]/div/div[1]")
    temperature = temperature_element.text.strip()

    return temperature

def create_and_update_database():
    conn = sqlite3.connect('weather_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time DATETIME,
            temperature TEXT
        )
    ''')

    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    temperature = get_temperature()

    cursor.execute('''
        INSERT INTO weather_data (date_time, temperature)
        VALUES (?, ?)
    ''', (current_date_time, temperature))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_and_update_database()