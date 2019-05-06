from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
import feedparser
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.clock import Clock


class MenuScreen(Screen):
    football_subscription = ObjectProperty()
    hockey_subscription = ObjectProperty()

    def next_screen(self):
        print(self.football_subscription.state)
        print(self.hockey_subscription.state)

    def print(self):
        print('Im clicked')


class RssBox(BoxLayout):
    feeds = ListProperty()
    title = StringProperty()
    rss_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(RssBox, self).__init__(**kwargs)
        Clock.schedule_once(self.show_more, 0)

    def show_more(self, *args):
        for feed in self.feeds[:5]:
            self.feeds.remove(feed)
            feed['published'] = datetime.strptime(feed['published'], '%Y-%m-%dT%H:%M:%S+00:00')
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

            self.rss_grid.add_widget(Label(text=text, font_size=20, text_size=(self.width/2, None)))
            self.rss_grid.add_widget(AsyncImage(source=feed['media_content'][0]['url'], size_hint_y=None, height=150))

            if not self.feeds:
                self.remove_widget(self.show_more_button)


class NewsScreen(Screen):
    pass


class DuoNews(Screen):
    pass


class MyScreenManager(ScreenManager):

    def next_screen(self):
        football = True if self.get_screen('menu').football_subscription.state == "down" else False
        hockey = True if self.get_screen('menu').hockey_subscription.state == "down" else False

        if hockey and football:
            football_feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')
            hockey_feeds = feedparser.parse('https://www.sport.ru/rssfeeds/hockey.rss')
            duobox = BoxLayout(orientation="vertical")
            duobox.add_widget(RssBox(feeds=football_feeds['entries'], title="Фубол"))
            duobox.add_widget(RssBox(feeds=hockey_feeds['entries'], title="Хокей"))
            self.get_screen('duo').add_widget(duobox)
            self.current = "duo"

        else:
            if football:
                feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')
                title = "Футбол"
            if hockey:
                feeds = feedparser.parse('https://www.sport.ru/rssfeeds/hockey.rss')
                title = "Хокей"

            rssbox = RssBox(feeds=feeds['entries'], title=title)
            self.get_screen('news').add_widget(rssbox)
            self.current = 'news'


# sm = ScreenManager()
# sm.add_widget(MenuScreen)


class RSSApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    RSSApp().run()
