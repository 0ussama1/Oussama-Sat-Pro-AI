from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MainInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Oussama Sat Pro AI\nReady for Service', halign='center'))

class OussamaSatApp(App):
    def build(self):
        return MainInterface()

if __name__ == '__main__':
    OussamaSatApp().run()
