import arcade
import math
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
from Hero import Hero
from Skelet_enemy import Skelet

class GameWindow(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.main_menu = menu_view

        self.w = WIDTH
        self.h = HEIGHT

        self.world_width = 2000
        self.world_height = 2000

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.player_list = arcade.SpriteList()
        self.player = Hero()
        self.player_list.append(self.player)

        self.enemy_list = arcade.SpriteList()

        self.skeleton_list = arcade.SpriteList()
        self.skelet_1 = Skelet()
        self.skeleton_list.append(self.skelet_1)
        # self.enemy_list.append(self.skeleton_list)

        cursor(self)

        self.keys_pressed = set()

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
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
            mouse_world_x = camera_x - (WIDTH // 2) + x
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
        self.player_list.update(delta_time, self.keys_pressed)
        self.player_list.update_animation(delta_time)

        self.skeleton_list.update(delta_time, self.player.center_x, self.player.center_y)
        self.skeleton_list.update_animation(delta_time, self.player.center_x)

        # skeleton_hit_list = arcade.check_for_collision_with_list(self.player, self.skeleton_list)

        # if skeleton_hit_list and self.player.state in ['atc_1', 'atc_2']:
        #     if self.player.current_texture_index == 1:
        #         for i in skeleton_hit_list:
        #             i.health -= 50

        if self.player.state in ['atc_1', 'atc_2']:
            skeleton_hit_list = arcade.check_for_collision_with_list(self.player, self.skeleton_list)

            # Наносим урон только в середине анимации (чтобы избежать множественных попаданий)
            if self.player.current_texture_index in [2, 3] and skeleton_hit_list:
                for skeleton in skeleton_hit_list:
                    skeleton.health -= 25

        for skeleton in self.skeleton_list:
            if skeleton.health <= 0:
                skeleton.remove_from_sprite_lists()

        position = (
            self.player.center_x,
            self.player.center_y
        )


        self.world_camera.position = arcade.math.lerp_2d(self.world_camera.position,
            position,
            0.03,
        )

    def on_hide_view(self):
        self.cursors_list = arcade.SpriteList()

    def on_show_view(self):
        cursor(self)
        self.keys_pressed = set()