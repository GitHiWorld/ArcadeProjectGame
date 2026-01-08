import time
import arcade
import math
import random
from pyglet.graphics import Batch
from constants import WIDTH, HEIGHT, cursor
from SettingsView import SettingsView


class PauseView(arcade.View):
    def __init__(self, game_view, menu_view):
        super().__init__()
        self.game_view = game_view
        self.menu_view = menu_view

        self.w = WIDTH

        if WIDTH == 3840:
            self.play = arcade.Sprite('images/sprites/play.png', scale=1)
            self.settings = arcade.Sprite('images/sprites/settings.png', scale=1)
            self.exit_game = arcade.Sprite('images/sprites/exit.png', scale=1)
            self.main_menu = arcade.Sprite('images/sprites/main_menu.png', scale=0.51)

        if WIDTH != 3840:
            self.play = arcade.Sprite('images/sprites/play.png', scale=0.5)
            self.settings = arcade.Sprite('images/sprites/settings.png', scale=0.5)
            self.exit_game = arcade.Sprite('images/sprites/exit.png', scale=0.5)
            self.main_menu = arcade.Sprite('images/sprites/main_menu.png', scale=0.255)

        self.update_button_positions()

        self.button_list = arcade.SpriteList()

        self.button_list.append(self.play)
        self.button_list.append(self.settings)
        self.button_list.append(self.exit_game)
        self.button_list.append(self.main_menu)

        cursor(self)

        self.pressed_button = None

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_rect_filled(arcade.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT), (0, 0, 0, 150))
        self.button_list.draw()
        self.cursors_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)

    def on_show_view(self):
        cursor(self)

    def update_button_positions(self):
        center_x = self.width // 2
        self.play.center_y = int(self.height * 0.7)
        self.main_menu.center_y = int(self.height * 0.6)
        self.settings.center_y = int(self.height * 0.5)
        self.exit_game.center_y = int(self.height * 0.4)

        self.play.center_x = center_x
        self.settings.center_x = center_x
        self.exit_game.center_x = center_x
        self.main_menu.center_x = center_x

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        clicked_sprites = arcade.get_sprites_at_point((x, y), self.button_list)

        if not clicked_sprites:
            return

        clicked = clicked_sprites[-1]
        self.pressed_button = clicked
        if self.w != 3840:
            if clicked != self.main_menu:
                clicked.scale = 0.45
            else:
                clicked.scale = 0.23

            if button == arcade.MOUSE_BUTTON_LEFT:
                clicked_buttons = arcade.get_sprites_at_point((x, y), self.button_list)
                if clicked_buttons:
                    clicked_sprite = clicked_buttons[-1]

                    if clicked_sprite == self.play:
                        self.window.show_view(self.game_view)
                    if clicked_sprite == self.settings:
                        pass
                    if clicked_sprite == self.exit_game:
                        arcade.exit()
                    if clicked_sprite == self.main_menu:
                        self.window.show_view(self.menu_view)

        else:
            if clicked != self.main_menu:
                clicked.scale = 0.7
            else:
                clicked.scale = 0.46

            if button == arcade.MOUSE_BUTTON_LEFT:
                clicked_buttons = arcade.get_sprites_at_point((x, y), self.button_list)
                if clicked_buttons:
                    clicked_sprite = clicked_buttons[-1]

                    if clicked_sprite == self.play:
                        self.window.show_view(self.game_view)

                    if clicked_sprite == self.settings:
                        settings_view = SettingsView(self.menu_view)
                        self.window.show_view(settings_view)

                    if clicked_sprite == self.exit_game:
                        arcade.exit()
                    if clicked_sprite == self.main_menu:
                        self.window.show_view(self.menu_view)
    def on_mouse_release(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if hasattr(self, 'pressed_button') and self.pressed_button is not None and self.w != 3840:
            if self.pressed_button != self.main_menu:
                self.pressed_button.scale = 0.55
            else:
                self.pressed_button.scale = 0.285
            self.pressed_button = None
        elif hasattr(self, 'pressed_button') and self.pressed_button is not None and self.w == 3840:
            if self.pressed_button != self.main_menu:
                self.pressed_button.scale = 1.2
            else:
                self.pressed_button.scale = 0.57
            self.pressed_button = None

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.button_list:
            if self.w != 3840:
                if btn != self.main_menu:
                    btn.scale = 0.5
                else:
                    btn.scale = 0.255

                check = arcade.get_sprites_at_point((x, y), self.button_list)
                if check:
                    checkin = check[-1]
                    if checkin != self.main_menu:
                        checkin.scale = 0.55
                    else:
                        checkin.scale = 0.285

            if self.w == 3840:
                if btn != self.main_menu:
                    btn.scale = 1
                else:
                    btn.scale = 0.51

                check = arcade.get_sprites_at_point((x, y), self.button_list)
                if check:
                    checkin = check[-1]
                    if checkin != self.main_menu:
                        checkin.scale = 1.2
                    else:
                        checkin.scale = 0.57

        self.cursor.center_x = x
        self.cursor.center_y = y