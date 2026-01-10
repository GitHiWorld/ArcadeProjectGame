import time
import arcade
import math
import random
import json
import os
from GameWindow import GameWindow
from constants import WIDTH, HEIGHT, cursor, SCALE, load_settings
from SettingsView import SettingsView


class Start_menu(arcade.View):
    def __init__(self):
        super().__init__()

        self.pressed_button = None
        self.sound = None

        # Используем глобальные размеры
        self.w = WIDTH
        self.h = HEIGHT

        self.texture = arcade.load_texture('images/backgrounds/start_mennu.png')

        self.background_sound = arcade.load_sound('sounds/Flappy Dragon - Wispernalia.mp3')

        button_scale = 0.5 * SCALE
        if WIDTH == 3840:
            button_scale = 1.0

        self.play = arcade.Sprite('images/sprites/play.png', scale=button_scale)
        self.settings = arcade.Sprite('images/sprites/settings.png', scale=button_scale)
        self.exit_game = arcade.Sprite('images/sprites/exit.png', scale=button_scale)

        self.update_button_positions()

        self.button_list = arcade.SpriteList()
        self.button_list.append(self.play)
        self.button_list.append(self.settings)
        self.button_list.append(self.exit_game)

        self.particles = []
        self.particle()

        font_size = int(24 * SCALE)
        if WIDTH == 3840:
            font_size = 48

        self.text_main = arcade.Text(
            'Wyvern: The Path to the Crown of Heaven',
            self.w // 2,
            self.h * 0.8,
            (255, 241, 210),
            font_size=font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x='center',
            anchor_y='top'
        )

        cursor(self)

        self.particle_list = arcade.shape_list.ShapeElementList()

    def start_game(self):
        game_view = GameWindow(self)
        self.window.show_view(game_view)

    def on_hide_view(self):
        if hasattr(self, 'sound') and self.sound:
            try:
                self.sound.pause()
            except:
                pass

    def setup(self):
        pass

    def particle(self):
        for i in range(250):
            self.particles.append({
                'x': random.uniform(0, self.w),
                'y': random.uniform(0, self.h),
                'size': random.uniform(2, 8) * SCALE,
                'speed': random.uniform(10.5, 16.5),
                'color': random.choice([
                    (255, 192, 203, random.randint(0, 100)),
                    (255, 182, 193, random.randint(0, 120)),
                    (255, 160, 122, random.randint(120, 200)),
                    (255, 183, 197, random.randint(0, 100)),
                    (240, 230, 140, random.randint(60, 200))
                ]),
                'side_speed': random.uniform(-8, 8),
                'rotation': random.uniform(0, 360),
                'rot_speed': random.uniform(-16, 16)
            })

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.w = width
        self.h = height
        self.update_button_positions()
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

        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h)
        )

        self.text_main.draw()

        self.button_list.draw()

        for i in self.particles:
            arcade.draw_rect_filled(
                arcade.XYWH(i['x'], i['y'], i['size'], i['size']),
                i['color'],
                i['rotation']
            )

        if hasattr(self, 'cursors_list'):
            self.cursors_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        clicked_sprites = arcade.get_sprites_at_point((x, y), self.button_list)

        if not clicked_sprites:
            return

        clicked = clicked_sprites[-1]
        self.pressed_button = clicked

        base_scale = 0.5 * SCALE
        if WIDTH == 3840:
            base_scale = 1.0

        clicked.scale = base_scale * 0.9

        clicked_sprite = clicked_sprites[-1]

        if clicked_sprite == self.play:
            self.start_game()
        elif clicked_sprite == self.settings:
            settings_view = SettingsView(self)
            self.window.show_view(settings_view)
        elif clicked_sprite == self.exit_game:
            arcade.exit()

    def on_mouse_release(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if hasattr(self, 'pressed_button') and self.pressed_button is not None:
            base_scale = 0.5 * SCALE
            if WIDTH == 3840:
                base_scale = 1.0
            self.pressed_button.scale = base_scale
            self.pressed_button = None

    def on_mouse_motion(self, x, y, dx, dy):
        base_scale = 0.5 * SCALE
        hover_scale = base_scale * 1.1

        if WIDTH == 3840:
            base_scale = 1.0
            hover_scale = 1.2

        for btn in [self.play, self.settings, self.exit_game]:
            btn.scale = base_scale

        check = arcade.get_sprites_at_point((x, y), self.button_list)
        if check:
            checkin = check[-1]
            checkin.scale = hover_scale

        if hasattr(self, 'cursor'):
            self.cursor.center_x = x
            self.cursor.center_y = y

    def update_button_positions(self):
        center_x = self.w // 2
        button_spacing = 100 * SCALE

        self.play.center_x = center_x
        self.play.center_y = int(self.h * 0.6)

        self.settings.center_x = center_x
        self.settings.center_y = int(self.h * 0.6 - button_spacing)

        self.exit_game.center_x = center_x
        self.exit_game.center_y = int(self.h * 0.6 - button_spacing * 2)

    def on_show_view(self):
        if hasattr(self, 'sound') and self.sound:
            try:
                self.sound.delete()
            except:
                pass

        settings = load_settings()
        volume = settings.get("volume", 70) / 100.0
        sound_enabled = settings.get("sound_enabled", True)

        if sound_enabled:
            self.sound = arcade.play_sound(
                self.background_sound,
                loop=True,
                volume=volume
            )
        else:
            self.sound = None

        # Обновляем позиции
        self.on_resize(WIDTH, HEIGHT)