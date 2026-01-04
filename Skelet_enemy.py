import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
from constants import FaceDirection


class Skelet(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.speed = 200
        self.health = 100

        idle_path = 'images/pers/enemy/skelet/Skeleton_Warrior/Idle.png'
        IDLE_COLUMNS = 7
        sprite_sheet_idle = arcade.SpriteSheet(idle_path)
        self.idle_textures_right = sprite_sheet_idle.get_texture_grid(
            size=(128, 128),
            columns=IDLE_COLUMNS,
            count=IDLE_COLUMNS
        )
        self.idle_textures_left = [tex.flip_horizontally() for tex in self.idle_textures_right]

        self.current_texture_index = 0
        self.animation_timer = 0

        self.state = 'idle'
        self.is_walking = False

        self.face_direction = FaceDirection.RIGHT
        self.attack_direction = FaceDirection.RIGHT

        self.texture = self.idle_textures_right[0]

        self.walk_delay = 0.1
        self.idle_delay = 0.2
        self.atc_1_delay = 0.1
        self.atc_2_delay = 0.1

        self.center_x = random.randint(0, WIDTH)
        self.center_y = HEIGHT // 2

    def update_animation(self, delta_time: float):
        self.animation_timer += delta_time

        if self.state == 'idle':
            if self.animation_timer >= self.idle_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.idle_textures_right)
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.idle_textures_right[self.current_texture_index]
                else:
                    self.texture = self.idle_textures_left[self.current_texture_index]

    def update(self, delta_time, player_x, player_y):
        dx = player_x - self.center_x
        dy = player_y - self.center_y

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor
