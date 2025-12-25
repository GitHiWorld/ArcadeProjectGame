import time
import arcade
import math
import random


class GameWindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rect_filled(arcade.XYWH(150,150, 150, 150), color=(255, 0, 0))
