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
            pd = datetime.strptime(feed['published'], '%Y-%m-%dT%H:%M:%S+00:00')
            pd = datetime.now() - pd
            pd = int(pd.total_seconds())

            if pd <= 60:
                pd = '%d секунд назад' % pd

            elif pd <= 60*60:
                pd = '%d минут назад' % pd/60

            elif pd <= 60*60*24:
                pd = pd/60/60
                if pd == 1 or pd == 21:
                    pd = '%d час назад' % pd
                elif 5 > pd > 1 or pd > 21:
                    pd = '%d часа назад' % pd
                else:
                    pd = '%d часов назад' % pd
            else:
                pd = '%d день назад' % (pd/60/60/24)

            text = feed['title']
            text += '\n'
            text += pd

            self.add_widget(Label(text=text, font_size=20, text_size=(self.width*3, None), pos_hint={'x': 0, 'top': 1}))
            self.add_widget(AsyncImage(source=feed['media_content'][0]['url'], size_hint_y=None, height=150))


class MyScreenManager(ScreenManager):
    pass


class PMApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    PMApp().run()
