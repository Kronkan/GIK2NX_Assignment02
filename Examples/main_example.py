# Use https://www.wunderground.com/weather/se/borlänge for Assignment
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from bs4 import BeautifulSoup
from kivy.properties import StringProperty
import requests


class HomeScreen(Screen):
    weather = StringProperty()
    description = StringProperty()
    humidity = StringProperty()
    pressure = StringProperty()
    visibility = StringProperty()

    def search(self):
        city_name = self.ids.city_name.text
        country_name = self.ids.country_name.text
        url = f'https://www.timeanddate.com/weather/{country_name}/{city_name}'
        response = requests.get(url=url)
        print(response.status_code)
        soup = BeautifulSoup(response.text,'html.parser')
        mainclass = soup.find(class_='bk-focus__qlook')
        secondclass = soup.find(class_='bk-focus__info')
        self.weather = mainclass.find(class_='h2').get_text()
        self.visibility = secondclass.findAll('td')[3].get_text()  # can also try slicing
        self.pressure = secondclass.findAll('td')[4].get_text()
        self.humidity = secondclass.findAll('td')[5].get_text()

class BajsApp(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        Window.size = (800, 1000)

BajsApp().run()
