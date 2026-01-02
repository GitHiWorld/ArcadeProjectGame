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

        self.mouse_x = 0
        self.mouse_y = 0

        idle_path = 'images/pers/Knight_1/Idle.png'
        IDLE_COLUMNS = 4
        sprite_sheet_idle = arcade.SpriteSheet(idle_path)
        self.idle_textures_right = sprite_sheet_idle.get_texture_grid(
            size=(128, 128),
            columns=IDLE_COLUMNS,
            count=IDLE_COLUMNS
        )
        self.idle_textures_left = [i.flip_horizontally() for i in self.idle_textures_right]

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

        atc_2_path = 'images/pers/Knight_1/Attack 2.png'
        ATC_2_COLUMNS = 4
        sprite_sheet_atc_2 = arcade.SpriteSheet(atc_2_path)
        self.atc_2_texture_right = sprite_sheet_atc_2.get_texture_grid(
            size=(128, 128),
            columns=ATC_2_COLUMNS,
            count=ATC_2_COLUMNS
        )
        self.atc_2_texture_left = [i.flip_horizontally() for i in self.atc_2_texture_right]

        self.current_texture_index = 0
        self.animation_timer = 0

        self.walk_delay = 0.1
        self.idle_delay = 0.2
        self.atc_1_delay = 0.1

        self.state = 'idle'
        self.is_walking = False

        self.attack_cooldown = 0.6
        self.attack_timer = 0
        self.can_attack = True

        self.face_direction = FaceDirection.RIGHT
        self.attack_direction = FaceDirection.RIGHT

        self.texture = self.idle_textures_right[0]

        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2

    def set_attack_direction(self, mouse_x):
        if mouse_x >= self.center_x:
            self.attack_direction = FaceDirection.RIGHT
        else:
            self.attack_direction = FaceDirection.LEFT

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
                if self.current_texture_index == len(self.atc_1_texture_right) - 1:
                    self.state = 'idle'
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)
                    if self.attack_direction == FaceDirection.RIGHT:
                        self.texture = self.atc_1_texture_right[self.current_texture_index]
                    else:
                        self.texture = self.atc_1_texture_left[self.current_texture_index]

    def update(self, delta_time, keys_pressed):
        if not self.can_attack:
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_cooldown:
                self.can_attack = True
                self.attack_timer = 0

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

    def try_attack(self, mouse_x):
        if self.can_attack:
            self.can_attack = False
            self.attack_timer = 0

            self.set_attack_direction(mouse_x)

            self.face_direction = self.attack_direction

            self.state = 'atc_1'
            self.current_texture_index = 0
            self.animation_timer = 0

            if self.attack_direction == FaceDirection.RIGHT:
                self.texture = self.atc_1_texture_right[0]
            else:
                self.texture = self.atc_1_texture_left[0]

            return True
        else:
            return False



