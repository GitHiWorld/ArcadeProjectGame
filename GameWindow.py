import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor
from PauseView import PauseView


class GameWindow(arcade.View):
    def __init__(self):
        super().__init__()

        self.w = WIDTH
        self.h = HEIGHT

        self.player = arcade.SpriteCircle(20, arcade.color.BLUE)
        self.player.center_x = self.w // 2
        self.player.center_y = self.h // 2
        self.player_speed = 170
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        cursor(self)

        self.keys_pressed = set()

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        # arcade.start_render()
        # arcade.draw_rect_filled(arcade.XYWH(self.w // 2, self.h // 2, self.w, self.h), color=(255, 0, 0))
        self.player_list.draw()
        self.cursors_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.center_x = x
        self.cursor.center_y = y

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


    def on_update(self, delta_time):
        dx, dy = 0, 0
        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            dx -= self.player_speed * delta_time
        if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            dx += self.player_speed * delta_time
        if arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed:
            dy += self.player_speed * delta_time
        if arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed:
            dy -= self.player_speed * delta_time


        # Нормализация диагонального движения
        if dx != 0 and dy != 0:
            factor = 0.7071  # ≈ 1/√2
            dx *= factor
            dy *= factor

        self.player.center_x += dx
        self.player.center_y += dy

    def on_hide_view(self):
        self.cursors_list = arcade.SpriteList()

    def on_show_view(self):
        cursor(self)
        self.keys_pressed = set()

