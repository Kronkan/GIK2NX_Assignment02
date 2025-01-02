# Use https://www.wunderground.com/weather/se/borlänge for Assignment
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from bs4 import BeautifulSoup
import pycountry
import requests
import sqlite3
import json
import os
from datetime import date, datetime

# Database setup
db_path = "db/weather.db"
os.makedirs("db", exist_ok=True)

# Initialize SQLite Database
db_connection = sqlite3.connect(db_path)
cursor = db_connection.cursor()
cursor.execute("""
               DROP TABLE IF EXISTS weather_data
                """)
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
    timestamp DATE DEFAULT (DATE('now'))
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
    
   
    def is_db_connection_open(self):
        """
        Function for checking if the SQLite connection is open.
        """
        try:
            db_connection.execute("SELECT 1")
            return True
        except sqlite3.ProgrammingError:
            return False
        except Exception:
            return False
      
      
    def get_country_code(self, country_name):
        """
        Function for getting the country code from the country name.
        """
        try:
            country_code = pycountry.countries.lookup(country_name)
            return country_code.alpha_2.lower()
        except LookupError as e:
            print(f"Country code not found: {e}") 
            return country_name.lower()       
    
    
    def validate_input(self, city_name, country_name):
        """
        Function for validating the input (city & country) from the user. 
        """
        try:
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
        
        except ValueError as e:
            print(f"Validation error: {e}")
            return None, None 
        
            
    # def fetch_firebase_data(self, city_name, country_name, today_date):
    #     """
    #     Fetch data from Firebase.
    #     """
    #     try:    
    #         print("Checking firebase for data...")
    #         firebase_response = requests.get(firebase_url, timeout=10)
    #         if firebase_response.status_code == 200:
    #             firebase_data = firebase_response.json() 
    #             for key, value in firebase_data.items():
    #                 if value.get("city") == city_name and value.get("country") == country_name:
    #                     firebase_timestamp = datetime.strptime(value.get("timestamp"), '%Y-%m-%d')
    #                     if firebase_timestamp.strftime('%Y-%m-%d') < today_date:
    #                         print("Firebase data is outdated. Scraping new data...")
    #                         scraped_data = self.scrape_data(city_name, country_name)
    #                         if scraped_data:
    #                             self.update_data(city_name, country_name, scraped_data)
    #                             self.update_UI(value)
    #                         else:
    #                             print("Using data from Firebase.")
    #                             self.update_UI(value)

    #         else:
    #             print(f"Firebase request failed with status code: {firebase_response.status_code}")         
    #     except Exception as e:
    #         print(f"Could not fetch data from Firebase: {e}")      
     
     
            
    # def fetch_sqlite_data(self, city_name, country_name, today_date):
    #     """
    #     Fetch data from the SQLite database.
    #     """
    #     if not self.is_db_connection_open():
    #             print("SQLite connection is closed. Attempting secondary sources...")
    #     else:
    #         try:
    #             print("Checking SQLite for data...")   
    #             cursor.execute(""" 
    #             SELECT temperature, description, pressure, visibility, humidity
    #             FROM weather_data
    #             WHERE city = ? AND country = ? AND strftime('%Y-%m-%d', timestamp) = ?
    #             """, (city_name, country_name, today_date))
    #             existing_data = cursor.fetchone()
            
    #             # Display cached data in the UI if available
    #             if existing_data:
    #                 db_timestamp = datetime.strptime(existing_data[-1], '%Y-%m-%d')
    #                 if db_timestamp.date() < datetime.now().date():
    #                     print("SQLite data is outdated. Scraping new data...")
    #                     scraped_data = self.scrape_data(city_name, country_name)
    #                     if scraped_data:
    #                         self.update_data(city_name, country_name, scraped_data)
    #                         self.update_UI(scraped_data)
    #                         print("SQLite data updated.")
    #                 else:
    #                     print("Using cached data from SQLite.")
    #                     self.update_UI(existing_data)
    #                 return
    #         except Exception as e:
    #             print(f"SQLite error: {e}")
                     
    
    # def fetch_txtfile_data(self, city_name, country_name):
    #     """
    #     Fetch data from the txt file.
    #     """
    #     print("Checking text file for data...")
    #     try:
    #         with open("db/weather_data.txt", "r") as file:
    #             for line in file:
    #                 if not line.strip():
    #                     continue
    #                 data = json.loads(line.strip())
    #                 if data["city"] == city_name and data["country"] == country_name:
    #                     timestamp = datetime.strptime(data["timestamp"], '%Y-%m-%d')
    #                     if timestamp.date() < datetime.now().date():
    #                         print("Text file data is outdated. Scraping new data...")
    #                         scraped_data = self.scrape_data(city_name, country_name)
    #                         if scraped_data:
    #                             self.store_data(city_name, country_name, scraped_data)
    #                             print("Text file data updated.")
    #                             self.update_UI(scraped_data)
    #                     else:
    #                         print("Using data from text file.")
    #                         self.update_UI(data)
    #                     return
    #     except FileNotFoundError:
    #         print("Text file not found.") 
    #     except Exception as e:
    #         print(f"Text file error: {e}")
        
             
    def search(self):
        """
        Search for weather data for a city and country. Check database first, scrape if not available.
        """
        # Get user input from Kivy UI and validate it using the validate_input method
        city_name = self.ids.city_name.text
        country_name = self.ids.country_name.text 
        city_name, country_name = self.validate_input(city_name, country_name)
        
        # Save the current date in the format YYYY-MM-DD
        # today_date = datetime.now().strftime('%Y-%m-%d')
        today_date = date.today()
         
        try:    
            print("Checking firebase for data...")
            firebase_response = requests.get(firebase_url, timeout=10)
            if firebase_response.status_code == 200:
                firebase_data = firebase_response.json() 
                for key, value in firebase_data.items():
                    if value.get("city") == city_name and value.get("country") == country_name:
                        firebase_timestamp = datetime.strptime(value.get("timestamp"), '%Y-%m-%d').date()
                        if firebase_timestamp < today_date:
                            print("Firebase data is outdated. Scraping new data...")
                            scraped_data = self.scrape_data(city_name, country_name)
                            if scraped_data:
                                self.update_data(city_name, country_name, scraped_data)
                                self.update_UI(value)
                            else:
                                print("Using data from Firebase.")
                                self.update_UI(value)
                        # if(value.get("timestamp") < today_date):
                        #     scraped_data = self.scrape_data(city_name, country_name)
                        #     self.update_data(scraped_data)
                        #     firebase_data = firebase_response.json()
                        #     for key, value in firebase_data.items():
                        #         if value.get("city") == city_name and value.get("country") == country_name:
                        #             print("Using data from Firebase.")
                        #             self.update_UI(value)
                        #             return
            else:
                print(f"Firebase request failed with status code: {firebase_response.status_code}")         
        except Exception as e:
            print(f"Could not fetch data from Firebase: {e}")      
        
        # db_connection.close() # Test för att se vad som händer om databasen inte är åtkomlig
        
        if not self.is_db_connection_open():
                print("SQLite connection is closed. Attempting secondary sources...")
        else:
            try:
                print("Checking SQLite for data...")   
                cursor.execute(""" 
                SELECT temperature, description, pressure, visibility, humidity
                FROM weather_data
                WHERE city = ? AND country = ? AND timestamp = ?
                """, (city_name, country_name, today_date))
                existing_data = cursor.fetchone()
            
                # Display cached data in the UI if available
                if existing_data:
                    db_timestamp = datetime.strptime(existing_data[-1], '%Y-%m-%d').date()
                    # if db_timestamp < datetime.now.date():
                    if db_timestamp < today_date:
                        print("SQLite data is outdated. Scraping new data...")
                        scraped_data = self.scrape_data(city_name, country_name)
                        if scraped_data:
                            self.update_data(city_name, country_name, scraped_data)
                            self.update_UI(scraped_data)
                            print("SQLite data updated.")
                    else:
                        print("Using cached data from SQLite.")
                        self.update_UI(existing_data)
                    return
            except Exception as e:
                print(f"SQLite error: {e}")
            
        # Fetch data from the txt file
        print("Checking text file for data...")
        try:
            with open("db/weather_data.txt", "r") as file:
                for line in file:
                    if not line.strip():
                        continue
                    data = json.loads(line.strip())
                    if data["city"] == city_name and data["country"] == country_name:
                        timestamp = datetime.strptime(data["timestamp"], '%Y-%m-%d').date()
                        # if timestamp.date() < datetime.now.date():
                        if timestamp < today_date:
                            print("Text file data is outdated. Scraping new data...")
                            scraped_data = self.scrape_data(city_name, country_name)
                            if scraped_data:
                                self.store_data(city_name, country_name, scraped_data)
                                print("Text file data updated.")
                                self.update_UI(scraped_data)
                        else:
                            print("Using data from text file.")
                            self.update_UI(data)
                        return
        except FileNotFoundError:
            print("Text file not found.")
        except Exception as e:
            print(f"Text file error: {e}")
        
        # if not self.is_db_connection_open():
        #         print("SQLite connection is closed. Attempting secondary sources...")
        # else:
            # try:
                
        # If no cached data, scrape the website as a last resort
        print("No cached or up-to-date data found. Scraping new data...")
        try:
            scraped_data = self.scrape_data(city_name, country_name)
            if scraped_data:
                self.store_data(city_name, country_name, scraped_data)
                self.update_UI(scraped_data)
        except Exception as e:
            print(f"Scraping error: {e}")
                    
            #     print("No cached or up-to-date data found. Scraping new data...")
            #     scraped_data = self.scrape_data(city_name, country_name) 
            
            #     if scraped_data:
            #         cursor.execute("""
            #         SELECT 1
            #         FROM weather_data
            #         WHERE city = ? AND country = ?
            #         """, (city_name, country_name))
            #         outdated_record = cursor.fetchone()
                    
            #         # Update the data if it already exists in the database but is outdated 
            #         if outdated_record:
            #             self.update_data(city_name, country_name, scraped_data)
            #         # Store new data if no record exists
            #         else:
            #             self.store_data(city_name, country_name, scraped_data)
                    
            #         # Update the UI
            #         self.update_UI(scraped_data)
                        
            # except Exception as e:
            #     print(f"Scraping error: {e}")  

                  
    def scrape_data(self, city_name, country_name):
        """
        Scrape weather data from the website for the given city & country.
        """
        try:
            # First, try and scrape data from timeanddate.com
            url = f'https://www.timeanddate.com/weather/{country_name}/{city_name}'
            response = requests.get(url=url, timeout=10)
            print(response.status_code)
            
            # If the request is successful, scrape the data
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
                
                # Return the scraped data as a dictionary
                return {
                    "temperature": temperature,
                    "description": description,
                    "pressure": pressure,
                    "visibility": visibility,
                    "humidity": humidity,
                }
                 
            # Otherwise, if timeanddate.com fails, attempt wunderground.com 
            else:
                country_code = self.get_country_code(country_name)
                url = f'https://www.wunderground.com/weather/{country_code}/{city_name}'
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
     
          
    def store_data(self, city_name, country_name, data):   
        """ Store scraped data in SQLite, Firebase, and text file."""

        # Add city, country and timestamp to the data dictionary
        data['city'] = city_name
        data['country'] = country_name
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d")
      
        try:
            # Store data in Firebase
            firebase_response = requests.post(firebase_url, json=data, timeout=10)
            if firebase_response.status_code == 200:
                print("Scraped data successfully stored in Firebase.")
            else:
                print(f"Firebase storage failed with status code: {firebase_response.status_code}")
        except Exception as e:
            print(f"Firebase storage error: {e}")
            
        if not self.is_db_connection_open():
            print("SQLite connection is closed. Attempting secondary sources...")
        else:
            try:    
                # Store data in SQLite Database
                cursor.execute("""
                INSERT INTO weather_data (city, country, temperature, description, pressure, visibility, humidity, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (data['city'], data['country'], data['temperature'], data['description'], 
                      data['pressure'], data['visibility'], data['humidity'], data['timestamp']
                      ))
                db_connection.commit()
                print("Scraped data successfully stored in SQLite.")
            except sqlite3.ProgrammingError as e:
                print(f"SQLite storage error: {e} - Connection may be closed.")
            except Exception as e: 
                print(f"General SQLite storage error: {e}") 
   
        try:
            # Store data in a text file
            with open("db/weather_data.txt", "a") as file:
                file.write(json.dumps(data) + "\n")
                print("Scraped data successfully stored in txt file.")
        except Exception as e:
            print(f"Txt file storage error: {e}")
    
            
    def update_data(self, city_name, country_name, data):
        """
        Update the weather data in the databases (SQLite, Firebase, and txt file).
        """
        # Add city, country and timestamp to the data dictionary
        data['city'] = city_name
        data['country'] = country_name
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Update Firebase
            firebase_response = requests.patch(firebase_url, json=data, timeout=10)
            if firebase_response.status_code == 200:
                print("Firebase data successfully updated.")
            else:
                print(f"Firebase update failed with status code: {firebase_response.status_code}")
        except Exception as e:
            print(f"Firebase update error: {e}")
        
        if not self.is_db_connection_open():
            print("SQLite connection is closed. Attempting secondary sources...")
        else:        
            try:
                # Update SQLite Database
                    cursor.execute("""
                    UPDATE weather_data 
                    SET temperature = ?, description = ?, pressure = ?, visibility = ?, humidity = ?, timestamp = ?
                    WHERE city = ? AND country = ?
                    """, (data['city'], data['country'], data['temperature'], data['description'], data['pressure'], 
                        data['visibility'], data['humidity'], data['timestamp']
                        ))
                    db_connection.commit()
            except Exception as e:
                print(f"SQLite update error: {e}")
    
        # Explain why we dont update the txt file in the presentation    
        try:
            # "Update" the text file
            with open("db/weather_data.txt", "a") as file:
                file.write(json.dumps(data) + "\n")
            print("Data successfully updated in the databases.")
        except Exception as e:
            print(f"Txt file update error: {e}")
    
            
    def update_UI(self, data):
        """
        Update the UI with the scraped weather data.
        """
        try:
            if isinstance(data, dict):
                self.temperature = data["temperature"]
                self.description = data["description"]
                self.pressure = data["pressure"]
                self.visibility = data["visibility"]
                self.humidity = data["humidity"]
            elif isinstance(data, tuple):
                self.temperature, self.description, self.pressure, self.visibility, self.humidity = data
            else:
                raise ValueError("Invalid data type.")
        except Exception as e:
            print(f"UI update error: {e}")    

        
# Main App Class
class MainApp(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        Window.size = (800, 1000)

MainApp().run()
