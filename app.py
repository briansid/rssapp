from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.clock import Clock
import feedparser
from kivy.uix.image import AsyncImage

class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass
    # def __init__(self, **kwargs):
    #     super(SecondScreen, self).__init__(**kwargs)
    #     # Clock.schedule_once(self.init_ui, 3)
    #     self.test()

    # def test(self):
    #     print(self.ids.grid)

    # pass
    # def on_enter(self, *args):
    #     grid = self.ids.grid
    #     print(dir(grid))

    # def some(self):
    #     pass
        # tasks = ['football' for i in range(10)]
        # for task in tasks:
        #     grid.add_widget(Label(text=task[1]))


class MyGrid(GridLayout):
    feeds = feedparser.parse('https://www.sport.ru/rssfeeds/football.rss')
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        # hockey = self.ids['_hockey']
        # print(hockey.state)
        # if hockey.state == 'down':
        for feed in self.feeds['entries']:
            self.add_widget(Label(text=feed['title']))
            self.add_widget(AsyncImage(source=feed['media_content'][0]['url']))



class MyScreenManager(ScreenManager):
    pass


class PMApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    PMApp().run()
