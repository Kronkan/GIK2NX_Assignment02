# Use https://www.wunderground.com/weather/se/borlänge for Assignment
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from bs4 import BeautifulSoup
import requests
import sqlite3
import json
import os
from datetime import datetime

# Database setup
db_path = "db/weather.db"
os.makedirs("db", exist_ok=True)

# Initialize SQLite Database
db_connection = sqlite3.connect(db_path)
cursor = db_connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    country TEXT,
    temperature TEXT,
    description TEXT,
    pressure TEXT,
    visibility TEXT,
    humidity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
db_connection.commit()

# Firebase URL
firebase_url = 'https://assignment2-gik2nx-cc2bd-default-rtdb.europe-west1.firebasedatabase.app/.json'


class HomeScreen(Screen):
    """
    Class for the Home Screen of the app.
    """
    temperature = StringProperty("N/A")
    description = StringProperty("N/A")
    humidity = StringProperty("N/A")
    pressure = StringProperty("N/A") 
    visibility = StringProperty("N/A")
    
    def validate_input(self, city_name, country_name):
        """
        Function for validating the input (city & country) from the user. 
        """
        # Validate the input from the user
        city_name = city_name.strip().lower()
        country_name = country_name.strip().lower()
        
        # Check if the city and country are provided in string format    
        if not city_name or not country_name:
            raise ValueError("City & Country must be provided.")
        if city_name.isnumeric() and country_name.isnumeric():
            raise ValueError("No numbers allowed in the input")
            
        # Replace special characters in city and country names
        city_name = city_name.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
        country_name = country_name.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
        
        return city_name, country_name
    
             
    def scrape_data(self, city_name, country_name):
        """
        Scrape weather data from the website for the given city & country.
        """
        try:
            # First, try and scrape data from timeanddate.com
            url = f'https://www.timeanddate.com/weather/{country_name}/{city_name}'
            response = requests.get(url=url, timeout=10)
            print(response.status_code)
            
            if(response.status_code == 200):           
                soup = BeautifulSoup(response.text,'html.parser')
                
                mainclass = soup.find(class_='bk-focus__qlook')
                secondclass = soup.find(class_='bk-focus__info')
                
                temperature = mainclass.find(class_="h2").get_text(strip=True) if mainclass else "N/A"
                description = mainclass.findAll("p")[0].get_text() if mainclass else "N/A"
                info_cells = secondclass.find_all("td")
                visibility = info_cells[3].get_text(strip=True)
                pressure = info_cells[4].get_text(strip=True)
                humidity = info_cells[5].get_text(strip=True)
                
                return {
                    "temperature": temperature,
                    "description": description,
                    "pressure": pressure,
                    "visibility": visibility,
                    "humidity": humidity,
                }
                 
            # Otherwise, if timeanddate.com fails, attempt wunderground.com 
            else:
                url = f'https://www.wunderground.com/weather/{country_name}/{city_name}'
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                temp_section = soup.find('lib-display-unit', {'type': 'temperature'}) 
                temperature = temp_section.find('span', class_='ng-star-inserted').get_text() if temp_section else "N/A"
                description_section = soup.find('p', class_='weather-quickie')
                description = description_section.get_text() if description_section else "N/A"
                
                conditions_section = soup.find('div', class_='data-module additional-conditions')
                
                pressure = conditions_section.find('div', string='Pressure').find_next('span', class_='ng-star-inserted').get_text().replace("°", "") if conditions_section else "N/A"
                visibility = conditions_section.find('div', string='Visibility').find_next('span', class_='ng-star-inserted').get_text().replace("°", "") if conditions_section else "N/A"
                humidity = conditions_section.find('div', string='Humidity').find_next('span', class_='ng-star-inserted').get_text().replace("°", "") if conditions_section else "N/A"
                
                return {
                    "temperature": temperature,
                    "description": description,
                    "pressure": pressure,
                    "visibility": visibility,
                    "humidity": humidity,
                }
   
        except Exception as e:
            print(f"Scraping error: {e}")
            return None
        
                    
    def search(self):
        """
        Search for weather data for a city and country. Check database first, scrape if not available.
        """
        try:
            # Get user input from Kivy UI and validate it using the validate_input method
            city_name = self.ids.city_name.text
            country_name = self.ids.country_name.text 
            
            city_name, country_name = self.validate_input(city_name, country_name)
            
            # Check SQLite for today's data 
            today_date = datetime.now().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
            cursor.execute("""
            SELECT temperature, description, pressure, visibility, humidity
            FROM weather_data
            WHERE city = ? AND country = ? AND strftime('%Y-%m-%d', timestamp) = ?
            """, (city_name, country_name, today_date))
            existing_data = cursor.fetchone()
            
            # Display cached data in the UI if available
            if existing_data:
                print("Using cached data from SQLite.")
                self.temperature, self.description, self.pressure, self.visibility, self.humidity = existing_data
                return  # Exit the function since data is already available
            
            # If no cached data, scrape the website
            print("No cached or up-to-date data found. Scraping new data...")
            scraped_data = self.scrape_data(city_name, country_name)
            
            if scraped_data:
                cursor.execute("""
                SELECT 1
                FROM weather_data
                WHERE city = ? AND country = ?
                """, (city_name, country_name))
                outdated_record = cursor.fetchone()
                
                # Update the data if it already exists in the database but is outdated  
                if outdated_record:
                    cursor.execute("""
                    UPDATE weather_data
                    SET temperature = ?, description = ?, pressure = ?, visibility = ?, humidity = ?
                    WHERE city = ? AND country = ?
                    """, (scraped_data['temperature'], scraped_data['description'], scraped_data['pressure'], 
                        scraped_data['visibility'], scraped_data['humidity'], city_name, country_name))
                    db_connection.commit()
                    
                    requests.patch(firebase_url, json=scraped_data, timeout=10)
                    
                    with open("db/weather_data.txt", "a") as file:
                        file.write(json.dumps(scraped_data) + "\n")
                    
                    print("Data successfully updated in the databases.")
                    
                # Store new data if no record exists
                else:
                    self.store_data(city_name, country_name, scraped_data)

                    # Update the UI
                    self.temperature = scraped_data["temperature"]
                    self.description = scraped_data["description"]
                    self.pressure = scraped_data["pressure"]
                    self.visibility = scraped_data["visibility"]
                    self.humidity = scraped_data["humidity"]
        
        except Exception as e:
            print(f"Error: {e}")

        
    def store_data(self, city_name, country_name, data):   
        """ Store scraped data in SQLite, Firebase, and text file."""
        try:
            # Store data in SQLite Database
            cursor.execute("""
            INSERT INTO weather_data (city, country, temperature, description, pressure, visibility, humidity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (city_name, country_name, data['temperature'], data['description'], data['pressure'], data['visibility'], data['humidity']))
            db_connection.commit()
            
            # Store data in Firebase
            requests.post(firebase_url, json=data, timeout=10)

            # Store data in a text file
            with open("db/weather_data.txt", "a") as file:
                file.write(json.dumps(data) + "\n")
            
            print("Scraped data successfully stored.")
            
        except Exception as e:
            print(f"Storage error: {e}") 


class MainApp(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        Window.size = (800, 1000)

MainApp().run()