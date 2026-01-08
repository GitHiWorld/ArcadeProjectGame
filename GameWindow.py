import arcade
import math
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP, SCALE
from PauseView import PauseView
from Hero import Hero
from Skelet_enemy import Skelet


class GameWindow(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.main_menu = menu_view

        self.map_1_sound = arcade.load_sound('sounds/map_1_sound.mp3', streaming=True)
        self.sound_map1 = None
        self.sound_pos = 0

        map_name = 'images/backgrounds/map_start_artemii.tmx'

        self.w = WIDTH
        self.h = HEIGHT

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.player_list = arcade.SpriteList()
        self.player = Hero(map_name)
        self.player_list.append(self.player)

        self.enemy_list = arcade.SpriteList()

        self.skeleton_list = arcade.SpriteList()
        self.skelet_1 = Skelet()
        self.skeleton_list.append(self.skelet_1)
        # self.enemy_list.append(self.skeleton_list)

        cursor(self)

        self.keys_pressed = set()

        arcade.set_background_color(arcade.color.BLACK)

        # ДИНАМИЧЕСКОЕ МАСШТАБИРОВАНИЕ КАРТЫ

        # Рассчитываем масштаб карты на основе разрешения экрана
        # Базовый масштаб для 1920x1080 = 2.5
        # Для 4K (3840x2160) масштаб будет 5.0
        base_tile_scale = 2.5
        dynamic_scale = base_tile_scale * SCALE

        self.tile_map = arcade.load_tilemap(map_name, scaling=dynamic_scale)
        tile_map = self.tile_map

        self.embient_list = tile_map.sprite_lists['окружение']
        self.walls_list = tile_map.sprite_lists['walls']
        self.water_list = tile_map.sprite_lists['water']
        self.floor_list = tile_map.sprite_lists['floor']

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.walls_list
        )


    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.floor_list.draw()
        self.water_list.draw()
        self.walls_list.draw()
        self.embient_list.draw()
        self.skeleton_list.draw()
        self.player_list.draw()

        self.gui_camera.use()
        self.cursors_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
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

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time, self.keys_pressed)
        self.player_list.update_animation(delta_time)

        self.skeleton_list.update(delta_time, self.player.center_x, self.player.center_y)
        self.skeleton_list.update_animation(delta_time, self.player.center_x)

        if self.player.state in ['atc_1', 'atc_2']:
            skeleton_hit_list = arcade.check_for_collision_with_list(self.player, self.skeleton_list)

            # Наносим урон только в середине анимации (чтобы избежать множественных попаданий)
            if self.player.current_texture_index in [2, 3] and skeleton_hit_list:
                for skeleton in skeleton_hit_list:
                    skeleton.health -= 25

        for skeleton in self.skeleton_list:
            if skeleton.health <= 0:
                skeleton.remove_from_sprite_lists()

        map_width_pixels = self.tile_map.width * self.tile_map.tile_width * (2.5 * SCALE)
        map_height_pixels = self.tile_map.height * self.tile_map.tile_height * (2.5 * SCALE)

        if self.player.center_x - self.w // 2 <= 0:
            target_x = self.w // 2
        elif self.player.center_x + self.w // 2 >= map_width_pixels:
            target_x = map_width_pixels - self.w // 2
        else:
            target_x = self.player.center_x

        if self.player.center_y - self.h // 2 <= 0:
            target_y = self.h // 2
        elif self.player.center_y + self.w // 2 >= map_height_pixels:
            target_y = map_height_pixels - self.h // 2
        else:
            target_y = self.player.center_y

        position = (
            target_x,
            target_y
        )

        self.world_camera.position = arcade.math.lerp_2d(self.world_camera.position,
                                                         position,
                                                         0.03,
                                                         )

    def on_hide_view(self):
        if self.sound_map1:
            self.sound_pos = self.map_1_sound.get_stream_position(self.sound_map1)
            self.sound_map1.pause()
        self.cursors_list = arcade.SpriteList()

    def on_show_view(self):
        cursor(self)
        self.sound_map1 = arcade.play_sound(self.map_1_sound, volume=0.5, loop=True)
        if self.sound_pos > 0:
            self.sound_map1.seek(self.sound_pos)
        self.keys_pressed = set()