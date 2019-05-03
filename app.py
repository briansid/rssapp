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
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.properties import ListProperty


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class ThirdScreen(Screen):
    pass


class Controller(FloatLayout):
    pass


class MyGrid(GridLayout):
    pass


class RSSBox(BoxLayout):
    title = StringProperty()
    feeds = ListProperty()

    def show_more(self):
        for feed in self.feeds[:5]:
            self.feeds.remove(feed)
            pd = datetime.now() - feed['published']
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

            self.rss_grid.add_widget(Label(text=text, font_size=20, text_size=(self.width/2, None), pos_hint={'x': 0, 'top': 1}))
            self.rss_grid.add_widget(AsyncImage(source=feed['media_content'][0]['url'], size_hint_y=None, height=150))

            if not self.feeds:
                self.rss_box.remove_widget(self.show_more_button)


class MyScreenManager(ScreenManager):
    hockey_rss = ObjectProperty()
    football_rss = ObjectProperty()
    rss_grid = ObjectProperty()
    show_more_button = ObjectProperty()
    single_rss = ObjectProperty()

    def open_rss(self):
        football = True if self.football_rss.state == "down" else False
        hockey = True if self.hockey_rss.state == "down" else False

        if hockey and football:
            football_feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')
            for feed in football_feeds['entries']:
                feed['published'] = datetime.strptime(feed['published'], '%Y-%m-%dT%H:%M:%S+00:00')
            hockey_feeds = feedparser.parse('https://www.sport.ru/rssfeeds/hockey.rss')
            for feed in hockey_feeds['entries']:
                feed['published'] = datetime.strptime(feed['published'], '%Y-%m-%dT%H:%M:%S+00:00')

            self.football_box.title = 'Футбол'
            self.football_box.feeds = football_feeds['entries']
            self.football_box.show_more()

            self.hockey_box.title = 'Хокей'
            self.hockey_box.feeds = hockey_feeds['entries']
            self.hockey_box.show_more()

            self.current = 'third'
        else:
            if football:
                feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')
                self.single_rss.title = 'Футбол'
            if hockey:
                self.single_rss.title = 'Хокей'
                feeds = feedparser.parse('https://www.sport.ru/rssfeeds/hockey.rss')

            for feed in feeds['entries']:
                feed['published'] = datetime.strptime(feed['published'], '%Y-%m-%dT%H:%M:%S+00:00')

            self.single_rss.feeds = feeds['entries']

            self.single_rss.show_more()

            self.current = 'second'



class PMApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    PMApp().run()
