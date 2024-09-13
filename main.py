import random
import os
import sys
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color




class CardHolder(FloatLayout):
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def __init__(self,n_cards=1,**kwargs):
        self.cols = 1
        self.padding = [10,10,10,10]
        super(CardHolder, self).__init__(**kwargs)
        offset_x = 0.4
        offset_y = 0.3
        for i in range(n_cards):
            card = Image(source=self.resource_path("cards/{}.png".format(random.randint(0, 52))),
                                                              size_hint=(0.5, 0.5))
            card.pos_hint = {"x": offset_x, "y": offset_y}
            self.add_widget(card)

            offset_x -= 0.1
            offset_y -= 0.07
            if offset_x <= 0.1:
                offset_x = 0.4

class MainWindow(GridLayout):
    #chList = []
    label_nCards = Label(text="1",size_hint_y=None, height=50)
    label_nPlayers = Label(text="1",size_hint_y=None, height=50)
    n_cards = 1
    n_players = 1
    layout = GridLayout(cols = 1)
    currLay = GridLayout(cols = 1)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)



        self.cols = 1

        gr = GridLayout(cols=2)
        sl1 = Slider(min=1, max=10, value=1, value_track=True, value_track_color=[1, 0, 0, 1],size_hint_y=None, height=100)
        sl2 = Slider(min=1, max=5, value=1, value_track=True, value_track_color=[1, 0, 0, 1],size_hint_y=None, height=100)
        sl1.bind(value=self.change_n_players)
        sl2.bind(value=self.change_n_cards)

        gr2 = GridLayout(cols=2,size_hint_y=None, height=20)
        gr3 = GridLayout(cols=2,size_hint_y=None, height=20)
        gr2.add_widget(Label(text="Number of Players: ",size_hint_y=None, height=50))
        gr2.add_widget(self.label_nPlayers)
        gr3.add_widget(Label(text="Number of Cards: ", size_hint_y=None, height=50))
        gr3.add_widget(self.label_nCards)

        gr.add_widget(gr2)
        gr.add_widget(gr3)
        gr.add_widget(sl1)
        gr.add_widget(sl2)

        self.add_widget(gr)

        self.layout = GridLayout(cols=1, size_hint_y=10)

        with self.canvas.before:
            Color(0.5, 1, 0.2, 0.2)  # RGBA - this is a light blue color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)


        self.add_widget(self.layout)

        btn = Button(text="NEW CARDS!", size_hint_y=None, height=150)
        btn.bind(on_press = self.on_new_button_press)
        self.add_widget(btn)




    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos



    def change_n_players(self, *args):
        self.label_nPlayers.text = str(int(args[1]))
        self.n_players = int(args[1])

    def change_n_cards(self, *args):
        self.label_nCards.text = str(int(args[1]))
        self.n_cards = int(args[1])

    def create_layout(self, instance = None):
        self.layout.remove_widget(self.currLay)

        self.currLay = GridLayout(cols=self.n_players)
        #self.chList.clear()

        for i in range(self.n_players):
            ch = CardHolder(n_cards=self.n_cards)
            self.currLay.add_widget(ch)
            #self.chList.append(ch)

        self.layout.add_widget(self.currLay)


    def on_new_button_press(self, instance = None):
        self.create_layout()


class CardCounter(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    CardCounter().run()