import arcade
import math
import time
import random
from constants import WIDTH, HEIGHT, cursor, SCALE, load_settings
from PauseView import PauseView
from Hero import Hero
from Skelet_enemy import Skelet
from LoseView import LoseView


class GameWindow(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.main_menu = menu_view

        self.map_1_sound = arcade.load_sound('sounds/map_1_sound.mp3', streaming=True)
        self.sound_map1 = None
        self.sound_pos = 0

        self.w = WIDTH
        self.h = HEIGHT

        self.map_name = 'images/backgrounds/map_start_artemii.tmx'

        self.world_camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.player_list = arcade.SpriteList()
        self.player = Hero(self.map_name)
        self.player_list.append(self.player)

        self.level_message = ""
        self.level_message_timer = 0
        self.show_level_message = False

        self.level_message_text = arcade.Text(
            "",
            self.window.width // 2,
            self.window.height // 2 + 100 * SCALE,
            (255, 50, 50, 255),
            font_size=int(48 * SCALE),
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        self.enemy_list = arcade.SpriteList()
        self.skeleton_list = arcade.SpriteList()

        cursor(self)

        self.keys_pressed = set()

        self.subtitles = [
            "...Предисловие...",
            "Отец: Давным давно, сын мой, эти земли были подвластны тёмной магии...",
            "Наши предки были доблестными воинами и магами, они сражались с тьмой на протяжении долгих десятилетий...",
            'И вот, когда тьма дала слабину, наши предки запечатали её в древнем артефакте: Короне небес...',
            'Но сейчас, после столь долгого времени силы тьмы, набрав мощь, вырвались на свободу...',
            'Я уже слишком стар чтобы бороться с ними, но ты, сын мой, должен остановить их...',
            'И, наконец, положить же конец страданиям и насилию в этих краях...',
            'Иди же в Замок Тёмных и повергни их раз и на всегда...',
            '...Удачи, о сын мой...'
        ]
        self.current_subtitle = 0
        self.displayed_text = ""
        self.full_text = ""
        self.typing_index = 0
        self.typing_timer = 0
        self.typing_speed = 0.055
        self.show_subtitles = True

        subtitle_font_size = int(24 * SCALE)
        if WIDTH == 3840:
            subtitle_font_size = 48

        self.subtitle_text = arcade.Text(
            "",
            110,
            100,
            (255, 241, 210),
            font_size=subtitle_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="left",
            anchor_y="center",
            align="left",
            width=self.window.width - 150
        )

        self.hint_text = arcade.Text(
            "Нажмите E",
            self.window.width // 2,
            30,
            (0, 0, 0, 180),
            font_size=int(20 * SCALE),
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center"
        )

        if self.subtitles:
            self.full_text = self.subtitles[0]

        self.load_map()

    def what_level(self, map_name):
        if map_name == 'images/backgrounds/map_start_artemii.tmx':
            return 1
        elif map_name == 'images/backgrounds/lvl2/dungeon_lvl2_test.tmx':
            return 2

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.floor_list.draw()
        self.walls_list.draw()
        self.other_list.draw()
        self.skeleton_list.draw()
        self.other_2_list.draw()
        self.player_list.draw()
        self.embient_list.draw()

        if self.what_level(self.map_name) != 1:
            self.draw_enemy_health_bars()

        if self.what_level(self.map_name) != 1:
            self.draw_player_health_bar()

        self.gui_camera.use()
        if self.what_level(self.map_name) != 1:
            self.draw_player_health()

        if self.what_level(self.map_name) == 1:
            self.draw_subtitles()

        if self.show_level_message:
            arcade.draw_rect_filled(
                arcade.XYWH(
                    self.window.width // 2,
                    self.level_message_text.y,
                    self.window.width - 100,
                    80 * SCALE
                ),
                (0, 0, 0, 150)
            )
            self.level_message_text.draw()

        self.cursors_list.draw()

    def update_subtitles(self, delta_time):
        if not self.show_subtitles or self.typing_index >= len(self.full_text):
            return

        self.typing_timer += delta_time
        if self.typing_timer >= self.typing_speed:
            self.typing_timer = 0
            self.displayed_text += self.full_text[self.typing_index]
            self.typing_index += 1
            self.subtitle_text.text = self.displayed_text

    def draw_subtitles(self):
        if not self.show_subtitles:
            return

        arcade.draw_rect_filled(
            arcade.XYWH(
                self.window.width // 2,
                100,
                self.window.width - 100,
                80 * SCALE
            ),
            (0, 0, 0, 180)
        )

        self.subtitle_text.draw()

        if self.typing_index >= len(self.full_text):
            blink = int(time.time() * 2) % 2
            if blink:
                self.hint_text.draw()

    def next_subtitle(self):
        self.current_subtitle += 1
        if self.current_subtitle < len(self.subtitles):
            self.full_text = self.subtitles[self.current_subtitle]
            self.displayed_text = ""
            self.typing_index = 0
            self.subtitle_text.text = ""
            return True
        else:
            self.show_subtitles = False
            return False

    def on_mouse_motion(self, x, y, dx, dy):
        if hasattr(self, 'cursor'):
            self.cursor.center_x = x
            self.cursor.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            camera_x = self.world_camera.position[0]
            mouse_world_x = camera_x - (self.w // 2) + x
            self.player.try_attack(mouse_world_x)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self, self.main_menu)
            self.window.show_view(pause_view)

        if key == arcade.key.E and self.show_subtitles:
            if self.typing_index < len(self.full_text):
                self.displayed_text = self.full_text
                self.typing_index = len(self.full_text)
                self.subtitle_text.text = self.full_text
            else:
                if not self.next_subtitle():
                    self.show_subtitles = False

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_update(self, delta_time):
        if self.player.is_dead:
            lose_view = LoseView(self)
            self.window.show_view(lose_view)
            return

        if self.show_level_message:
            self.level_message_timer -= delta_time
            if self.level_message_timer <= 0:
                self.show_level_message = False

        map_width_pixels = self.tile_map.width * self.tile_map.tile_width * (2.5 * SCALE)
        map_height_pixels = self.tile_map.height * self.tile_map.tile_height * (2.5 * SCALE)

        self.physics_engine.update()
        self.player_list.update(delta_time, self.keys_pressed)
        self.player_list.update_animation(delta_time)

        self.skeleton_list.update(delta_time, self.player.center_x, self.player.center_y)
        self.skeleton_list.update_animation(delta_time, self.player.center_x)

        next_collison = arcade.check_for_collision_with_list(self.player, self.next_list)

        if self.what_level(self.map_name) == 1:
            self.update_subtitles(delta_time)
            if next_collison and not self.show_subtitles or 0 == 0:
                self.level_message = "Уничтожь всех стражей тьмы"
                self.level_message_text.text = self.level_message
                self.show_level_message = True
                self.level_message_timer = 5.0
                self.map_name = 'images/backgrounds/lvl2/dungeon_lvl2_ready.tmx'
                self.load_map()
                self.player_list.remove(self.player)
                self.player = Hero(self.map_name)
                self.player_list.append(self.player)
                map_height_pixels = self.tile_map.height * self.tile_map.tile_height * (2.5 * SCALE)
                self.player.center_y = map_height_pixels // 2
                self.physics_engine = arcade.PhysicsEngineSimple(
                    self.player, (self.walls_list, self.other_list)
                )

        heal_colision = arcade.check_for_collision_with_list(self.player, self.heal_list)
        if heal_colision:
            self.player.health = 100

        skeleton_hit_list = arcade.check_for_collision_with_list(self.player, self.skeleton_list)

        if self.player.state in ['atc_1', 'atc_2']:
            if self.player.current_texture_index in [2] and skeleton_hit_list:
                for skeleton in skeleton_hit_list:
                    skeleton.take_damage(random.randint(15, 25), self.player.center_x)

        for skeleton in self.skeleton_list:
            if skeleton.is_dead:
                skeleton.remove_from_sprite_lists()
            if skeleton.state == 'atc_1' and skeleton.current_texture_index == 2:
                self.player.take_damage(random.randint(5, 15), skeleton.center_x)

        if self.player.center_x - self.w // 2 <= 0:
            target_x = self.w // 2
        elif self.player.center_x + self.w // 2 >= map_width_pixels:
            target_x = map_width_pixels - self.w // 2
        else:
            target_x = self.player.center_x

        if self.player.center_y - self.h // 2 <= 0:
            target_y = self.h // 2
        elif self.player.center_y + self.h // 2 >= map_height_pixels:
            target_y = map_height_pixels - self.h // 2
        else:
            target_y = self.player.center_y

        position = (target_x, target_y)

        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            0.03
        )

    def draw_player_health(self):
        hp_ratio = max(0, self.player.health) / 100.0

        x = self.w - 320 * SCALE
        y = self.h - 90 * SCALE
        bar_width = 280 * SCALE
        bar_height = 40 * SCALE

        arcade.draw_lbwh_rectangle_outline(
            left=x,
            bottom=y,
            width=bar_width,
            height=bar_height,
            color=arcade.color.WHITE,
            border_width=5
        )

        arcade.draw_lbwh_rectangle_filled(
            left=x + 5,
            bottom=y + 5,
            width=bar_width - 10,
            height=bar_height - 10,
            color=arcade.color.BLACK
        )

        fill_width = (bar_width - 10) * hp_ratio
        fill_color = arcade.color.GREEN if hp_ratio > 0.5 else arcade.color.ORANGE if hp_ratio > 0.25 else arcade.color.RED
        arcade.draw_lbwh_rectangle_filled(
            left=x + 5,
            bottom=y + 5,
            width=fill_width,
            height=bar_height - 10,
            color=fill_color
        )

        arcade.draw_text(
            f"HP: {int(self.player.health)} / 100",
            x + bar_width / 2,
            y + bar_height / 2,
            arcade.color.WHITE,
            font_size=int(28 * SCALE),
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def draw_player_health_bar(self):
        if not self.player.is_dead and self.player.health > 0:
            hp_ratio = max(0, self.player.health) / 100.0

            left = self.player.center_x - 35 * SCALE
            bottom = self.player.center_y + 40 * SCALE
            bar_width = 70 * SCALE
            bar_height = 14 * SCALE

            arcade.draw_lbwh_rectangle_outline(
                left=left,
                bottom=bottom,
                width=bar_width,
                height=bar_height,
                color=arcade.color.WHITE_SMOKE,
                border_width=int(2 * SCALE)
            )

            arcade.draw_lbwh_rectangle_filled(
                left=left + 2 * SCALE,
                bottom=bottom + 2 * SCALE,
                width=bar_width - 4 * SCALE,
                height=bar_height - 4 * SCALE,
                color=arcade.color.DARK_GRAY
            )

            fill_width = (bar_width - 4 * SCALE) * hp_ratio
            fill_color = (
                arcade.color.LIME_GREEN if hp_ratio > 0.6 else
                arcade.color.ORANGE if hp_ratio > 0.3 else
                arcade.color.RED
            )
            arcade.draw_lbwh_rectangle_filled(
                left=left + 2 * SCALE,
                bottom=bottom + 2 * SCALE,
                width=fill_width,
                height=bar_height - 4 * SCALE,
                color=fill_color
            )

    def draw_enemy_health_bars(self):
        for skeleton in self.skeleton_list:
            if not skeleton.is_dead and skeleton.health > 0:
                hp_ratio = max(0, skeleton.health) / 100.0

                left = skeleton.center_x - 35 * SCALE
                bottom = skeleton.center_y + 70 * SCALE
                bar_width = 70 * SCALE
                bar_height = 14 * SCALE

                arcade.draw_lbwh_rectangle_outline(
                    left=left,
                    bottom=bottom,
                    width=bar_width,
                    height=bar_height,
                    color=arcade.color.WHITE_SMOKE,
                    border_width=int(2 * SCALE)
                )

                arcade.draw_lbwh_rectangle_filled(
                    left=left + 2 * SCALE,
                    bottom=bottom + 2 * SCALE,
                    width=bar_width - 4 * SCALE,
                    height=bar_height - 4 * SCALE,
                    color=arcade.color.DARK_GRAY
                )

                fill_width = (bar_width - 4 * SCALE) * hp_ratio
                fill_color = (
                    arcade.color.LIME_GREEN if hp_ratio > 0.6 else
                    arcade.color.ORANGE if hp_ratio > 0.3 else
                    arcade.color.RED
                )
                arcade.draw_lbwh_rectangle_filled(
                    left=left + 2 * SCALE,
                    bottom=bottom + 2 * SCALE,
                    width=fill_width,
                    height=bar_height - 4 * SCALE,
                    color=fill_color
                )

    def on_hide_view(self):
        if self.sound_map1:
            try:
                self.sound_pos = self.map_1_sound.get_stream_position(self.sound_map1)
            except:
                self.sound_pos = 0

            try:
                self.sound_map1.pause()
            except:
                pass

        if hasattr(self, 'cursors_list'):
            self.cursors_list.clear()

    def on_show_view(self):
        cursor(self)

        if hasattr(self, 'sound_map1') and self.sound_map1:
            try:
                self.sound_map1.delete()
            except:
                pass

        settings = load_settings()
        volume = settings.get("volume", 70) / 100.0
        sound_enabled = settings.get("sound_enabled", True)

        if sound_enabled:
            self.sound_map1 = arcade.play_sound(
                self.map_1_sound,
                volume=volume,
                loop=True
            )

            if hasattr(self, 'sound_pos') and self.sound_pos > 0:
                try:
                    self.sound_map1.seek(self.sound_pos)
                except:
                    pass
        else:
            self.sound_map1 = None

        self.keys_pressed = set()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.w = width
        self.h = height

    def load_map(self):
        base_tile_scale = 2.5
        dynamic_scale = base_tile_scale * SCALE

        self.tile_map = arcade.load_tilemap(self.map_name, scaling=dynamic_scale)
        tile_map = self.tile_map

        if self.what_level(self.map_name) == 1:
            self.next_list = tile_map.sprite_lists['next']
        else:
            self.other_2_list = tile_map.sprite_lists['other+']
            self.heal_list = tile_map.sprite_lists['heal']

        self.skeleton_list.clear()

        if 'skelets' in tile_map.sprite_lists:
            spawn_tiles = tile_map.sprite_lists['skelets']
            for tile in spawn_tiles:
                skeleton = Skelet()
                skeleton.center_x = tile.center_x
                skeleton.center_y = tile.center_y
                self.skeleton_list.append(skeleton)

        self.embient_list = tile_map.sprite_lists['embient']
        self.other_list = tile_map.sprite_lists['other']
        self.walls_list = tile_map.sprite_lists['walls']
        self.floor_list = tile_map.sprite_lists['floor']

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, (self.walls_list, self.other_list)
        )