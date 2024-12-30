    # def search(self):
    #     try:
    #         city_name = self.ids.city_name.text.strip().lower()
    #         country_name = self.ids.country_name.text.strip().lower()
            
    #         if not city_name or not country_name:
    #             raise ValueError("City & Country must be provided.")
    #         if city_name.isnumeric() and country_name.isnumeric():
    #             raise ValueError("No numbers allowed in the input")
            
    #         city_name = city_name.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
    #         country_name = country_name.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')

    #         #  Här bör vi kolla om datan redan finns och om den behöver patchas 
            
    #         url = f'https://www.timeanddate.com/weather/{country_name}/{city_name}'
    #         response = requests.get(url=url, timeout=10)
    #         print(response.status_code)

    #         if(response.status_code == 200):           
    #             soup = BeautifulSoup(response.text,'html.parser')
                
    #             mainclass = soup.find(class_='bk-focus__qlook')
    #             secondclass = soup.find(class_='bk-focus__info')
                
    #             if mainclass:
    #                 self.temperature = mainclass.find(class_="h2").get_text(strip=True)
    #                 self.description = mainclass.findAll("p")[0].get_text()
    #             else:
    #                 print("Main temperature data not found.")
                    
    #             if secondclass:
    #                 info_cells = secondclass.find_all("td")
    #                 #if len(info_cells) > 4:
    #                 self.visibility = info_cells[3].get_text(strip=True)
    #                 self.pressure = info_cells[4].get_text(strip=True)
    #                 self.humidity = info_cells[5].get_text(strip=True)
    #                 #else:
    #                     #print("Weather info cells are incomplete.")
    #             else:
    #                 print("Secondary temperature data not found.")
            
    #         else:
    #             # Attempt wunderground.com
    #             url = f'https://www.wunderground.com/weather/{country_name}/{city_name}'
    #             response = requests.get(url, timeout=10)
    #             soup = BeautifulSoup(response.text, 'html.parser')

    #             temp_section = soup.find('lib-display-unit', {'type': 'temperature'})
    #             if temp_section:
    #                 temp = temp_section.find('span', class_='ng-star-inserted')
    #                 self.temperature = temp.get_text() if temp else "N/A"
                
    #             description_section = soup.find('p', class_='weather-quickie')
    #             self.description = description_section.get_text() if description_section else "N/A"

    #             # Extract additional conditions (pressure, visibility, humidity)
    #             conditions_section = soup.find('div', class_='data-module additional-conditions')
                 
    #             pressure_row = conditions_section.find('div', string='Pressure')
    #             if pressure_row:
    #                 pressure_span = pressure_row.find_next('span', class_='test-false wu-unit wu-unit-pressure ng-star-inserted')
    #                 self.pressure = pressure_span.get_text().replace("°", "") if pressure_span else "N/A"
                    
    #             visibility_row = conditions_section.find('div', string='Visibility')
    #             if visibility_row:
    #                 visibility_span = visibility_row.find_next('span', class_='test-false wu-unit wu-unit-distance ng-star-inserted')
    #                 self.visibility = visibility_span.get_text().replace("°", "") if visibility_span else "N/A"
                    
    #             humidity_row = conditions_section.find('div', string='Humidity')
    #             if humidity_row:
    #                 humidity_span = humidity_row.find_next('span', class_='test-false wu-unit wu-unit-humidity ng-star-inserted')
    #                 self.humidity = humidity_span.get_text().replace("°", "") if humidity_span else "N/A"
        
    #         data = {
    #             "city": city_name,
    #             "country": country_name,
    #             "temperature": self.temperature,
    #             "description": self.description,
    #             "pressure": self.pressure,
    #             "visibility": self.visibility,
    #             "humidity": self.humidity
    #         }
    #         self.store_data(data)
                
        # except Exception as e:
        #     print(f"Error: {e}")
        
        # def store_data(self, data): 
    #     try: 
    #         # if(cursor.execute(f"SELECT city and country WHERE EXISTS country = {data.country_name} AND city = {data.city_name} FROM weather_data")): 
    #         #     current_timestamp = cursor.execute(f"SELECT CURRENT_TIMESTAMP WHERE country = {data.country_name} AND city = {data.city_name}FROM weather_data")
    #         #     if (current_timestamp < datetime.datetime.today):
    #         # Store data in SQLite Database
    #         cursor.execute("""
    #         INSERT INTO weather_data (city, country, temperature, description, pressure, visibility, humidity)
    #         VALUES (?, ?, ?, ?, ?, ?, ?)
    #         """, (data['city'], data['country'], data['temperature'], data['description'], data['pressure'], data['visibility'], data['humidity']))
    #         db_connection.commit()
                    
    #         # Store data in Firebase
    #         requests.post(firebase_url, json=data, timeout=10)
                
    #         # def create_get(self): 
    #         #     res=requests.get(url=self.firebase_url)
    #         #     print(res.json())

    #         # def create_patch(self):
    #         #     flname = self.ids.flname.text
    #         #     age = self.ids.age.text
    #         #     salary = self.ids.salary.text
    #         #     print(salary)
    #         #     json_data = '{"Table1":{"Name": "'+flname+'", "Age": "'+age+'", "Salary": "'+salary+'"}}'
    #         #     res=requests.patch(url=self.firebase_url, json=json.loads(json_data))
    #         #     print(res)

    #         # def create_post(self):
    #         #     flname = self.ids.flname.text
    #         #     age = self.ids.age.text
    #         #     salary = self.ids.salary.text
    #         #     print(salary)
    #         #     json_data = '{"Table1":{"Name": "'+flname+'", "Age": "'+age+'", "Salary": "'+salary+'"}}'
    #         #     res=requests.post(url=self.firebase_url, json=json.loads(json_data)) 
    #         #     print(res) 

    #         # def create_put(self):
    #         #     json_data = '{"Table1":{"Name": "test4", "Age": "33", "Salary": "3333"}}'
    #         #     res=requests.put(url=self.firebase_url, json=json.loads(json_data))
    #         #     print(res)

    #         # def create_delete(self):
    #         #     delete_url = 'https://assignment2-gik2nx-cc2bd-default-rtdb.europe-west1.firebasedatabase.app/'
    #         #     #res=requests.delete(url=delete_url+"Table1/Salary"+".json")
    #         #     res = requests.delete(url=self.firebase_url)
    #         #     print(res)
            
    #         with open("db/weather_data.txt", "a") as file:
    #             file.write(json.dumps(data) + "\n")
            
    #     except Exception as e:
    #         print(f"Error: {e}")
    
        # def check_existing_data(self, city_name, country_name):
    #     try:
    #         today_date = datetime.today().strftime('%Y-%m-%d')
    #         cursor.execute("""
    #         SELECT temperature, description, pressure, visibility, humidity 
    #         FROM weather_data WHERE city = ? AND country = ? AND DATE(timestamp) = ?
    #         """, (city_name, country_name, today_date))
    #         data = cursor.fetchone()
            
    #         if data:
    #             self.temperature, self.description, self.pressure, self.visibility, self.humidity = data
    #             return True
    #         else: 
    #             return False 
        
    #     except Exception as e:
    #         print(f"Error while reading data: {e}")

    # def read_data(self, city_name, country_name):
    #     weather_data = cursor.execute("""
    #         SELECT temperature, description, pressure, visibility, humidity 
    #         FROM weather_data WHERE city = {city_name} AND country = {country_name}
    #         """
    #         )
        
    #     self.temperature = weather_data.temperature
    #     self.description = weather_data.description
    #     self.humidity = weather_data.humidity
    #     self.pressure = weather_data.pressure
    #     self.visibility = weather_data.visibility
    
    # def patch_data(self, city_name, country_name):
    #     patch_data = self.search()
    
    
    # OLD SEARCH FUNCTION
    
             # temp_section = soup.find('lib-display-unit', {'type': 'temperature'})
                # if temp_section:
                #     temp = temp_section.find('span', class_='ng-star-inserted')
                #     self.temperature = temp.get_text() if temp else "N/A"
                
                # description_section = soup.find('p', class_='weather-quickie')
                # self.description = description_section.get_text() if description_section else "N/A"

                # Extract additional conditions (pressure, visibility, humidity)
                # conditions_section = soup.find('div', class_='data-module additional-conditions')
                 
                # pressure_row = conditions_section.find('div', string='Pressure')
                # if pressure_row:
                #     pressure_span = pressure_row.find_next('span', class_='test-false wu-unit wu-unit-pressure ng-star-inserted')
                #     self.pressure = pressure_span.get_text().replace("°", "") if pressure_span else "N/A"
                    
                # visibility_row = conditions_section.find('div', string='Visibility')
                # if visibility_row:
                #     visibility_span = visibility_row.find_next('span', class_='test-false wu-unit wu-unit-distance ng-star-inserted')
                #     self.visibility = visibility_span.get_text().replace("°", "") if visibility_span else "N/A"
                    
                # humidity_row = conditions_section.find('div', string='Humidity')
                # if humidity_row:
                #     humidity_span = humidity_row.find_next('span', class_='test-false wu-unit wu-unit-humidity ng-star-inserted')
                #     self.humidity = humidity_span.get_text().replace("°", "") if humidity_span else "N/A"

            # Create data dictionary
            # data = {
            #     "city": city_name,
            #     "country": country_name,
            #     "temperature": self.temperature,
            #     "description": self.description,
            #     "pressure": self.pressure,
            #     "visibility": self.visibility,
            #     "humidity": self.humidity
            # }
            
            # if mainclass:
                #     self.temperature = mainclass.find(class_="h2").get_text(strip=True)
                #     self.description = mainclass.findAll("p")[0].get_text()
                # else:
                #     print("Main temperature data not found.")
                    
                # if secondclass:
                #     info_cells = secondclass.find_all("td")
                #     self.visibility = info_cells[3].get_text(strip=True)
                #     self.pressure = info_cells[4].get_text(strip=True)
                #     self.humidity = info_cells[5].get_text(strip=True)
                # else:
                #     print("Secondary temperature data not found.")
                
            # else: 
            #     print("Cached data is outdated. Scraping new data...")
            #     new_data = self.scrape_data(city_name, country_name)
            #     if new_data:
            #         cursor.execute("""
            #         UPDATE weather_date
            #         SET temperature = ?, description = ?, pressure = ?, visibility = ?, humidity = ?
            #         WHERE city = ? AND country = ?
            #         """, (new_data['temperature'], new_data['description'], new_data['pressure'], 
            #             new_data['visibility'], new_data['humidity'], city_name, country_name))
            #         db_connection.commit()
            #         print("Data successfully updated in SQLite.") 
                    
            #         self.temperature = new_data["temperature"]
            #         self.description = new_data["description"]
            #         self.pressure = new_data["pressure"]
            #         self.visibility = new_data["visibility"]
            #         self.humidity = new_data["humidity"]
            #     return  # Exit the function since data is now updated and available
                
            # # If no cached data, scrape the website
            # print("No cached data. Scraping website...")
            # scraped_data = self.scrape_data(city_name, country_name)
            
            # if scraped_data:
            #     # Store the scraped data
            #     self.store_data(city_name, country_name, scraped_data)
                
            #     # Update the UI
            #     self.temperature = scraped_data["temperature"]
            #     self.description = scraped_data["description"]
            #     self.pressure = scraped_data["pressure"]
            #     self.visibility = scraped_data["visibility"]
            #     self.humidity = scraped_data["humidity"]