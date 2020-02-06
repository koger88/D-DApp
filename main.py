from kivy.app import App
kivy.uix.widget import Widget

class DnD(Widget):
    pass

class DnDApp(App):
    def build(self):
        return DnD()

if __name__ == "__main__":
    DnDApp().run()