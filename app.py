from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout


class StartPage(AnchorLayout):
    def subscription(self, *args):
        hockey_subscription = self.ids['football_subscription']
        print(dir(hockey_subscription))


class PMApp(App):
    def build(self):
        return StartPage()


if __name__ == '__main__':
    PMApp().run()