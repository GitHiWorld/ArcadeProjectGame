import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
import enum

class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1

class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 1.0
        self.speed = 300
        self.health = 100

        idle_path = 'images/pers/Knight_1/Idle.png'
        IDLE_COLUMNS = 4
        sprite_sheet_idle = arcade.SpriteSheet(idle_path)
        self.idle_textures_right = sprite_sheet_idle.get_texture_grid(
            size=(128, 128),
            columns=IDLE_COLUMNS,
            count=IDLE_COLUMNS
        )
        self.idle_textures_left = [tex.flip_horizontally() for tex in self.idle_textures_right]

        run_path = 'images/pers/Knight_1/Run.png'
        RUN_COLUMNS = 5
        sprite_sheet_run = arcade.SpriteSheet(run_path)
        self.walk_textures_right = sprite_sheet_run.get_texture_grid(
            size=(128, 128),
            columns=RUN_COLUMNS,
            count=RUN_COLUMNS
        )
        self.walk_textures_left = [tex.flip_horizontally() for tex in self.walk_textures_right]

        atc_1_path = 'images/pers/Knight_1/Attack 1.png'
        ATC_1_COLUMNS = 5
        sprite_sheet_atc_1 = arcade.SpriteSheet(atc_1_path)
        self.atc_1_texture_right = sprite_sheet_atc_1.get_texture_grid(
            size=(128, 128),
            columns=ATC_1_COLUMNS,
            count=ATC_1_COLUMNS
        )
        self.atc_1_texture_left = [tex.flip_horizontally() for tex in self.atc_1_texture_right]

        self.current_texture_index = 0
        self.animation_timer = 0

        self.walk_delay = 0.1
        self.idle_delay = 0.2
        self.atc_1_delay = 0.1

        self.state = 'idle'
        self.is_walking = False

        self.face_direction = FaceDirection.RIGHT

        self.texture = self.idle_textures_right[0]

        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2

    def update_animation(self, delta_time: float):
        self.animation_timer += delta_time

        if self.state == 'run':
            if self.animation_timer >= self.walk_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.walk_textures_right)
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures_right[self.current_texture_index]
                else:
                    self.texture = self.walk_textures_left[self.current_texture_index]
            else:
                self.state = 'idle'
        elif self.state == 'idle':
            if self.animation_timer >= self.idle_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.idle_textures_right)
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.idle_textures_right[self.current_texture_index]
                else:
                    self.texture = self.idle_textures_left[self.current_texture_index]
        elif self.state == 'atc_1':
            if self.animation_timer >= self.atc_1_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.atc_1_texture_right)
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.atc_1_texture_right[self.current_texture_index]
                else:
                    self.texture = self.atc_1_texture_left[self.current_texture_index]
                if self.current_texture_index == len(self.atc_1_texture_right) - 1:
                    # Анимация закончилась
                    self.state = 'idle'
                    self.current_texture_index = 0


    def update(self, delta_time, keys_pressed):
        dx, dy = 0, 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy

        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT

        self.is_walking = bool(dx or dy)
        if self.state != 'atc_1':
            if self.is_walking:
                self.state = 'run'
            else:
                self.state = 'idle'



