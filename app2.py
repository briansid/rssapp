from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
import feedparser
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class MenuScreen(Screen):
    pass


class RssBox(BoxLayout):
    feeds = ListProperty()
    title = StringProperty()
    rss_grid = ObjectProperty()
    action_button = ObjectProperty()
    action_bar = ObjectProperty()

    def __init__(self, **kwargs):
        super(RssBox, self).__init__(**kwargs)
        Clock.schedule_once(self.show_more, 0)
        # Store a copy of all feeds for duo category
        self.all_feeds = self.feeds.copy()

    def show_more(self, *args):
        for feed in self.feeds[:5]:
            self.feeds.remove(feed)
            try:
                feed['published'] = datetime.strptime(feed['published'], '%Y-%m-%dT%H:%M:%S+00:00')
            except:
                pass
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

            self.rss_grid.add_widget(ClickableLabel(
                    text=text, link=feed['link'],
                    font_size=20, text_size=(self.width/2, None)
            ))

            try:
                image = feed['media_content'][0]['url']
            except:
                image = 'no_image.svg'

            self.rss_grid.add_widget(ClickableImage(
                source=image, link=feed['link'],
                size_hint_y=None, height=150
            ))

            if not self.feeds:
                self.remove_widget(self.action_button)


class NewsScreen(Screen):
    pass


class DuoNews(Screen):
    pass


class ShowMoreButton(Button):
    pass


class ShowAllNewsButton(Button):
    pass


class ClickableLabel(Label):
    link = StringProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(self.link)


class ClickableImage(AsyncImage):
    link = StringProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(self.link)


class MyScreenManager(ScreenManager):
    def add_news_screen(self, feeds, title):
        rssbox = RssBox(feeds=feeds, title=title)
        self.get_screen('news').add_widget(rssbox)
        self.current = 'news'

    def next_screen(self):
        football = True if self.get_screen('menu').football_subscription.state == "down" else False
        hockey = True if self.get_screen('menu').hockey_subscription.state == "down" else False

        if hockey and football:
            football_feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')
            hockey_feeds = feedparser.parse('https://www.sport.ru/rssfeeds/hockey.rss')
            duobox = BoxLayout(orientation="vertical")

            football_box = RssBox(feeds=football_feeds['entries'], title="Фубол")
            football_box.remove_widget(football_box.action_button)
            football_box.add_widget(ShowAllNewsButton(text="Все новости футбола"))
            duobox.add_widget(football_box)

            hockey_box = RssBox(feeds=hockey_feeds['entries'], title="Хокей")
            hockey_box.remove_widget(hockey_box.action_button)
            hockey_box.remove_widget(hockey_box.action_bar)
            hockey_box.add_widget(ShowAllNewsButton(text="Все новости хокея"))
            duobox.add_widget(hockey_box)

            self.get_screen('duo').add_widget(duobox)
            self.current = "duo"
        else:
            if football:
                feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')
                title = "Футбол"
            if hockey:
                feeds = feedparser.parse('https://www.sport.ru/rssfeeds/hockey.rss')
                title = "Хокей"

            self.add_news_screen(feeds['entries'], title)


# sm = ScreenManager()
# sm.add_widget(MenuScreen)


class RSSApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    RSSApp().run()
