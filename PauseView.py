import time
import arcade
import math
import random
from pyglet.graphics import Batch
from constants import WIDTH, HEIGHT, cursor


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.batch = Batch()
        self.pause_text = arcade.Text("Пауза", self.window.width / 2, self.window.height / 2,
                                      arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы продолжить", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        cursor(self)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_rect_filled(arcade.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT), (0, 0, 0, 150))
        self.batch.draw()
        self.cursors_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.center_x = x
        self.cursor.center_y = y

    def on_show_view(self):
        cursor(self)