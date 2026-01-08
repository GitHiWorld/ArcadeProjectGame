import time
import arcade
import math
import random
from GameWindow import GameWindow
from constants import WIDTH, HEIGHT, cursor
from pyglet.graphics import Batch
from SettingsView import SettingsView
from SettingsView import SettingsView


class Start_menu(arcade.View):
    def __init__(self):
        super().__init__()

        screen_extension4k = 16

        self.pressed_button = None

        size = arcade.get_display_size()
        if isinstance(size, tuple):
            self.w = size[0]
            self.h = size[1]

        self.texture = arcade.load_texture('images/backgrounds/start_mennu.png')
        # arcade.load_font('fonts/Comic Sans MS Pixel/Comic Sans MS Pixel.ttf')
        self.background_sound = arcade.load_sound('sounds/Flappy Dragon - Wispernalia.mp3')

        if self.w == 3840:
            self.play = arcade.Sprite('images/sprites/play.png', scale=1)
            self.settings = arcade.Sprite('images/sprites/settings.png', scale=1)
            self.exit_game = arcade.Sprite('images/sprites/exit.png', scale=1)

        if self.w != 3840:
            self.play = arcade.Sprite('images/sprites/play.png', scale=0.5)
            self.settings = arcade.Sprite('images/sprites/settings.png', scale=0.5)
            self.exit_game = arcade.Sprite('images/sprites/exit.png', scale=0.5)

        self.update_button_positions()

        self.button_list = arcade.SpriteList()

        self.button_list.append(self.play)
        self.button_list.append(self.settings)
        self.button_list.append(self.exit_game)

        # self.sound = arcade.play_sound(self.background_sound, loop=True, volume=0.5)

        self.particles = []
        self.particle()

        self.text_main = arcade.Text('Wyvern: The Path to the Crown of Heaven', self.w // 2, self.h * 0.8,
                                     (255, 241, 210),
                                     font_size=23.5 * (self.w / 1366) , font_name="Comic Sans MS pixel rus eng", anchor_x='center',
                                     anchor_y='top')
        if self.w == 3840:
            self.text_main = arcade.Text('Wyvern: The Path to the Crown of Heaven', self.w // 2, self.h * 0.8,
                                     (255, 241, 210),
                                     font_size=screen_extension4k * (self.w / 1366) , font_name="Comic Sans MS pixel rus eng", anchor_x='center',
                                     anchor_y='top')

        self.window.set_mouse_visible(False)

        cursor(self)

        self.particle_list = arcade.shape_list.ShapeElementList()

    def start_game(self):
        game_view = GameWindow(self)
        self.window.show_view(game_view)

    def on_hide_view(self):
        if self.sound:
            self.sound.pause()

    def setup(self):
        pass

    def particle(self):
        for i in range(250):
            self.particles.append({
                'x': random.uniform(0, self.w),
                'y': random.uniform(0, self.h),
                'size': random.uniform(2, 8),
                'speed': random.uniform(10.5, 16.5),
                'color': random.choice([
                    (255, 192, 203, random.randint(0, 100)),  # Розовый (лепестки сакуры)
                    (255, 182, 193, random.randint(0, 120)),  # Светло-розовый
                    (255, 160, 122, random.randint(120, 200)),  # Светло-коралловый
                    # (255, 218, 185, random.randint(60, 200)),  # Персиковый
                    (255,183,197, random.randint(0, 100)),
                    (255, 183, 197, random.randint(0, 160)),
                    (240, 230, 140, random.randint(60, 200))
                ]),
                'side_speed': random.uniform(-8, 8),
                'rotation': random.uniform(0, 360),
                'rot_speed': random.uniform(-16, 16)
            })

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.update_button_positions()
        self.w = width
        self.h = height

        self.text_main.x = self.w // 2
        self.text_main.y = self.h * 0.8

    def on_update(self, delta_time):
        for i in self.particles:
            i['y'] -= i['speed'] * delta_time
            i['x'] += i['side_speed'] * delta_time
            i['rotation'] += i['rot_speed'] * delta_time

            if i['y'] <= 0:
                i['y'] = self.h + 10
            if i['x'] <= -10:
                i['x'] = self.w + 10
            elif i['x'] >= self.w + 10:
                i['x'] = -10


    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.texture,
                                 arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h))

        self.text_main.draw()
        self.button_list.draw()

        for i in self.particles:
            arcade.draw_rect_filled(arcade.XYWH(i['x'], i['y'], i['size'], i['size']), i['color'], i['rotation'])

        self.cursors_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        clicked_sprites = arcade.get_sprites_at_point((x, y), self.button_list)

        if not clicked_sprites:
            return

        clicked = clicked_sprites[-1]
        self.pressed_button = clicked
        if self.w != 3840:
            clicked.scale = 0.45

            if button == arcade.MOUSE_BUTTON_LEFT:
                clicked_buttons = arcade.get_sprites_at_point((x, y), self.button_list)
                if clicked_buttons:
                    clicked_sprite = clicked_buttons[-1]

                    if clicked_sprite == self.play:
                        self.start_game()
                    if clicked_sprite == self.settings:
                        settings_view = SettingsView(self)
                        self.window.show_view(settings_view)
                    if clicked_sprite == self.exit_game:
                        arcade.exit()
        else:
            clicked.scale = 0.7

            if button == arcade.MOUSE_BUTTON_LEFT:
                clicked_buttons = arcade.get_sprites_at_point((x, y), self.button_list)
                if clicked_buttons:
                    clicked_sprite = clicked_buttons[-1]

                    if clicked_sprite == self.play:
                        self.start_game()

                    if clicked_sprite == self.settings:
                        pass

                    if clicked_sprite == self.exit_game:
                        arcade.exit()

    def on_mouse_release(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if hasattr(self, 'pressed_button') and self.pressed_button is not None and self.w != 3840:
            self.pressed_button.scale = 0.55
            self.pressed_button = None
        elif hasattr(self, 'pressed_button') and self.pressed_button is not None and self.w == 3840:
            self.pressed_button.scale = 0.8
            self.pressed_button = None

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in [self.play, self.settings, self.exit_game]:
            if self.w != 3840:
                btn.scale = 0.5

                check = arcade.get_sprites_at_point((x, y), self.button_list)
                if check:
                    checkin = check[-1]
                    checkin.scale = 0.55

            if self.w == 3840:
                btn.scale = 1

                check = arcade.get_sprites_at_point((x, y), self.button_list)
                if check:
                    checkin = check[-1]
                    checkin.scale = 1.2

        self.cursor.center_x = x
        self.cursor.center_y = y

    def update_button_positions(self):
        center_x = self.width // 2
        self.play.center_y = int(self.height * 0.6)
        self.settings.center_y = int(self.height * 0.5)
        self.exit_game.center_y = int(self.height * 0.4)

        self.play.center_x = center_x
        self.settings.center_x = center_x
        self.exit_game.center_x = center_x

    def on_show_view(self):
        self.__init__()
        self.sound = arcade.play_sound(self.background_sound, loop=True, volume=0.5)
        self.on_resize(WIDTH, HEIGHT)
