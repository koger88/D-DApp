from kivy.app import App
from kivy.uix.widget import Widget
import requests

class DnD():
    res = requests.get("http://www.dnd5eapi.co/api/")
    for i in res.json():
        print(i)

class DnDApp(App):
    def build(self):
        return DnD()

if __name__ == "__main__":
    #DnDApp().run()
    DnD()