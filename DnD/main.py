from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import requests
import webbrowser

Scene = ""

Builder.load_string("""
<MenuScreen>:
    FloatLayout:
        Image:
            source: 'dnd.png'
            pos_hint: {"x":0.2, "top":0.95}
            size_hint: [0.60,0.1]
        Button:
            text: 'Races'
            pos_hint: {"x":0.2, "top":0.8}
            size_hint: [0.60,0.1]
            on_press: root.ButtonPress(self)
        Button:
            text: 'Classes'
            pos_hint: {"x":0.2, "top":0.65}
            size_hint: [0.60,0.1]
            on_press: root.ButtonPress(self)
        Button:
            text: 'Skills'
            pos_hint: {"x":0.2, "top":0.50}
            size_hint: [0.60,0.1]
            on_press: root.ButtonPress(self)
        Button:
            text: 'Features'
            pos_hint: {"x":0.2, "top":0.35}
            size_hint: [0.60,0.1]
            on_press: root.ButtonPress(self)
        Button:
            text: 'Copyright'
            pos_hint: {"x":0.2, "top":0.15}
            size_hint: [0.60,0.1]
            on_press: root.Copyright()

""")

class MenuScreen(Screen):
    def ButtonPress(self, instance):
        global Scene
        Scene = instance.text
        self.manager.current = 'item'


    def Copyright(self):
        webbrowser.open("https://www.dnd5eapi.co/")

class ItemScreen(Screen):

    #Funktion til tilbageknap
    def BackButtonPress(self,instance):
        self.manager.current = 'menu'
    
    #Funktion til at vælge en specifik ting
    def ChangeButtonPress(self,instance):
        global Scene
        for item in self.items["results"]:
            if f"{instance.text}" in item.values():
                Scene = item["url"]

        self.manager.current = 'specificItem'

    def on_pre_enter(self, *args):
        self.clear_widgets()
        global Scene
        self.items = requests.get(f"https://dnd5eapi.co/api/{Scene}").json()
        
        #definere et gridlayout til api resultater 
        g = GridLayout(cols=1, spacing=10, size_hint_y=None)
        g.bind(minimum_height=g.setter('height'))
     
        #Definere tilbage knap
        btn = Button(text="Tilbage til start", size_hint_y=None, height=40)
        btn.bind(on_press=self.BackButtonPress)
        g.add_widget(btn)

        #Tilføjer alle resultater fra api'en som en knap i vores definerede gridlayout
        for item in self.items["results"]:
            print(str(item)+"\n")
            btn = Button(text=str(item["index"]), size_hint_y=None, height=40)
            btn.bind(on_press=self.ChangeButtonPress)
            g.add_widget(btn)

        root = ScrollView()
        root.add_widget(g)
        self.add_widget(root)

class SpecificItemScreen(Screen):

    #Funktion til tilbageknap
    def BackButtonPress(self,instance):
        self.manager.current = 'menu'

    def on_pre_enter(self, *args):
        self.clear_widgets()
        global Scene
        items = requests.get(f"https://dnd5eapi.co{Scene}").json()
        
        #definere et gridlayout til api resultater 
        g = GridLayout(cols=1, spacing=10, size_hint_y=None)
        g.bind(minimum_height=g.setter('height'))

        root = ScrollView()

        #Definere tilbage knap
        btn = Button(text="Tilbage til start", size_hint_y=None, height=40)
        btn.bind(on_press=self.BackButtonPress)
        g.add_widget(btn)
 
        g.add_widget(Label(text=str(items["name"]), size_hint_y=None, height=80))

        i = Scene.split("/")[2]
        if i == "races":
            g.add_widget(Label(text="Speed : " + str(items["speed"]), size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))
            
            n = "Ability Bonuses : \n"
            for item in items["ability_bonuses"]:
                n = n + "   " + str(item["name"]) + " : " + str(item["bonus"])+"\n"
            g.add_widget(Label(text=n, size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))

            g.add_widget(Label(text="Alignment : " + str(items["alignment"]), size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))
            g.add_widget(Label(text="Age : "+str(items["age"]), size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))
            g.add_widget(Label(text="Size : " + str(items["size"]), size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))
            g.add_widget(Label(text="Size Description : "+str(items["size_description"]), size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))
        
        elif i == "classes":

            n = "Proficiency Choices : \n"
            n = n +"   Choose : " + str(items["proficiency_choices"][0]["choose"]) + "\n       "
            for item in items["proficiency_choices"][0]["from"]:
                n = n + str(item["name"])+", "
            g.add_widget(Label(text=n, size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))

            n = "Proficiencies : \n   "
            for item in items["proficiencies"]:
                n = n + str(item["name"])+", "
            g.add_widget(Label(text=n, size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))

            n = "Saving Throws : \n"
            for item in items["saving_throws"]:
                n = n + "   " + str(item["name"])+"\n"
            g.add_widget(Label(text=n, size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))
        
        elif i == "skills":
            n = "Description : \n"
            for item in items["desc"]:
                n = n + str(item)+", "
            g.add_widget(Label(text=n, size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))

            n = f'Ability Score : {items["ability_score"]["name"]}'
            g.add_widget(Label(text=n, size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))

        elif i == "features":
            g.add_widget(Label(text="Level : " + str(items["level"]), size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))

            n = "Description : \n"
            for item in items["desc"]:
                n = n + str(item)+", "
            g.add_widget(Label(text=n, size_hint_y=None,text_size= [Window.width-80,None],height=-0.1468*Window.width+197.43))

        root.add_widget(g)
        self.add_widget(root)

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ItemScreen(name='item'))
sm.add_widget(SpecificItemScreen(name='specificItem'))

class DnDApp(App):
    def build(self):
        return sm


if __name__ =='__main__':
    DnDApp().run()