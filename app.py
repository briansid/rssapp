from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.clock import Clock
import feedparser
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from datetime import datetime


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class Controller(FloatLayout):
    pass


class MyGrid(GridLayout):
    feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        # hockey = self.ids['_hockey']
        # print(hockey.state)
        # if hockey.state == 'down':
        for feed in self.feeds['entries']:
            self.add_widget(Label(text=feed['title'], text_size=(self.width, None), size_hint_y=None, height=100))
            self.add_widget(AsyncImage(source=feed['media_content'][0]['url'], size_hint=(None,None), size=(100,100)))


class MyScreenManager(ScreenManager):
    pass


class PMApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    PMApp().run()
