import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
from Hero import Hero


class GameWindow(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.main_menu = menu_view

        self.w = WIDTH
        self.h = HEIGHT

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        # self.player = arcade.SpriteCircle(20, arcade.color.BLUE)
        # self.player.center_x = self.w // 2
        # self.player.center_y = self.h // 2
        # self.player_speed = 180
        # self.player_list = arcade.SpriteList()
        # self.player_list.append(self.player)

        self.player_list = arcade.SpriteList()
        self.player = Hero()
        self.player_list.append(self.player)

        cursor(self)

        self.keys_pressed = set()

    def on_draw(self):
        self.clear()
        # arcade.start_render()
        # arcade.draw_rect_filled(arcade.XYWH(self.w // 2, self.h // 2, self.w, self.h), color=(255, 0, 0))
        self.world_camera.use()
        self.player_list.draw()

        self.gui_camera.use()
        self.cursors_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.center_x = x
        self.cursor.center_y = y

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
        self.player_list.update_animation()
        # dx, dy = 0, 0
        # if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
        #     dx -= self.player_speed * delta_time
        # if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
        #     dx += self.player_speed * delta_time
        # if arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed:
        #     dy += self.player_speed * delta_time
        # if arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed:
        #     dy -= self.player_speed * delta_time
        #
        #
        # # Нормализация диагонального движения
        # if dx != 0 and dy != 0:
        #     factor = 0.7071  # ≈ 1/√2
        #     dx *= factor
        #     dy *= factor
        #
        # self.player.center_x += dx
        # self.player.center_y += dy

        position = (
            self.player.center_x,
            self.player.center_y
        )


        self.world_camera.position = arcade.math.lerp_2d(self.world_camera.position,
            position,
            0.1,
        )

        # cam_x, cam_y = self.world_camera.position
        # dz_left = cam_x - DEAD_ZONE_W // 2
        # dz_right = cam_x + DEAD_ZONE_W // 2
        # dz_bottom = cam_y - DEAD_ZONE_H // 2
        # dz_top = cam_y + DEAD_ZONE_H // 2
        #
        # px, py = self.player.center_x, self.player.center_y
        # target_x, target_y = cam_x, cam_y
        #
        # if px < dz_left:
        #     target_x = px + DEAD_ZONE_W // 2
        # elif px > dz_right:
        #     target_x = px - DEAD_ZONE_W // 2
        # if py < dz_bottom:
        #     target_y = py + DEAD_ZONE_H // 2
        # elif py > dz_top:
        #     target_y = py - DEAD_ZONE_H // 2
        #
        # half_w = self.world_camera.viewport_width / 2
        # half_h = self.world_camera.viewport_height / 2
        # target_x = max(half_w, min(self.world_width - half_w, target_x))
        # target_y = max(half_h, min(self.world_height - half_h, target_y))
        #
        # smooth_x = (1 - CAMERA_LERP) * cam_x + CAMERA_LERP * target_x
        # smooth_y = (1 - CAMERA_LERP) * cam_y + CAMERA_LERP * target_y
        # self.cam_target = (smooth_x, smooth_y)
        #
        # self.world_camera.position = (self.cam_target[0], self.cam_target[1])

    def on_hide_view(self):
        self.cursors_list = arcade.SpriteList()

    def on_show_view(self):
        cursor(self)
        self.keys_pressed = set()

