import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
from constants import FaceDirection, SCALE


class Skelet(arcade.Sprite):
    def __init__(self, speed_multiplier=1.0):
        super().__init__()

        self.base_speed = 150
        self.speed = self.base_speed * speed_multiplier
        self.health = 100

        screen_ratio = WIDTH / 1920
        self.scale = 1.0 * screen_ratio

        self.atc_range = 50 * screen_ratio
        self.vision_range = 500 * screen_ratio


        idle_path = 'images/pers/enemy/skelet/Skeleton_Warrior/Idle.png'
        IDLE_COLUMNS = 7
        sprite_sheet_idle = arcade.SpriteSheet(idle_path)
        self.idle_textures_right = sprite_sheet_idle.get_texture_grid(
            size=(128, 128),
            columns=IDLE_COLUMNS,
            count=IDLE_COLUMNS
        )
        self.idle_textures_left = [tex.flip_horizontally() for tex in self.idle_textures_right]

        run_path = 'images/pers/enemy/skelet/Skeleton_Warrior/Walk.png'
        RUN_COLUMNS = 7
        sprite_sheet_run = arcade.SpriteSheet(run_path)
        self.walk_textures_right = sprite_sheet_run.get_texture_grid(
            size=(128, 128),
            columns=RUN_COLUMNS,
            count=RUN_COLUMNS
        )
        self.walk_textures_left = [tex.flip_horizontally() for tex in self.walk_textures_right]

        atc_1_path = 'images/pers/enemy/skelet/Skeleton_Warrior/Attack_1.png'
        ATC_1_COLUMNS = 5
        sprite_sheet_atc_1 = arcade.SpriteSheet(atc_1_path)
        self.atc_1_texture_right = sprite_sheet_atc_1.get_texture_grid(
            size=(128, 128),
            columns=ATC_1_COLUMNS,
            count=ATC_1_COLUMNS
        )
        self.atc_1_texture_left = [tex.flip_horizontally() for tex in self.atc_1_texture_right]

        hurt_path = 'images/pers/enemy/skelet/Skeleton_Warrior/Hurt.png'
        HURT_COLUMNS = 2
        sprite_sheet_hurt = arcade.SpriteSheet(hurt_path)
        self.hurt_texture_right = sprite_sheet_hurt.get_texture_grid(
            size=(128, 128),
            columns=HURT_COLUMNS,
            count=HURT_COLUMNS
        )
        self.hurt_texture_left = [i.flip_horizontally() for i in self.hurt_texture_right]

        dead_path = 'images/pers/enemy/skelet/Skeleton_Warrior/Dead.png'
        DEAD_COLUMNS = 4
        sprite_sheet_dead = arcade.SpriteSheet(dead_path)
        self.dead_texture_right = sprite_sheet_dead.get_texture_grid(
            size=(128, 128),
            columns=DEAD_COLUMNS,
            count=DEAD_COLUMNS
        )
        self.dead_texture_left = [i.flip_horizontally() for i in self.dead_texture_right]

        self.current_texture_index = 0
        self.animation_timer = 0

        self.state = 'idle'
        self.is_walking = False

        self.face_direction = FaceDirection.RIGHT
        self.attack_direction = FaceDirection.RIGHT

        self.texture = self.idle_textures_right[0]

        self.walk_delay = 0.1
        self.idle_delay = 0.16
        self.atc_1_delay = 0.14
        self.atc_2_delay = 0.1
        self.hurt_delay = 0.1
        self.dead_delay = 0.18

        self.atc_range = 50
        self.vision_range = 500

        self.center_x = random.randint(10, WIDTH)
        self.center_y = HEIGHT * 1.8

        self.is_dead = False

    def update_animation(self, delta_time, player_x):
        self.animation_timer += delta_time

        if self.state == 'run':
            if self.animation_timer >= self.walk_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.walk_textures_right)
                if player_x >= self.center_x:
                    self.texture = self.walk_textures_right[self.current_texture_index]
                else:
                    self.texture = self.walk_textures_left[self.current_texture_index]

        elif self.state == 'idle':
            if self.animation_timer >= self.idle_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.idle_textures_right)
                if player_x >= self.center_x:
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
                    if player_x >= self.center_x:
                        self.texture = self.atc_1_texture_right[self.current_texture_index]
                    else:
                        self.texture = self.atc_1_texture_left[self.current_texture_index]

        elif self.state == 'hurt':
            if self.animation_timer >= self.hurt_delay:
                self.animation_timer = 0
                # self.current_texture_index = (self.current_texture_index + 1) % len(self.hurt_texture_right)
                if self.current_texture_index == len(self.hurt_texture_right) - 1:
                    self.state = 'idle'
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)
                    if player_x >= self.center_x:
                        self.texture = self.hurt_texture_right[self.current_texture_index]
                    else:
                        self.texture = self.hurt_texture_left[self.current_texture_index]

        elif self.state == 'dead':
            if self.animation_timer >= self.dead_delay:
                self.animation_timer = 0

                if self.current_texture_index == len(self.dead_texture_right) - 1:
                    self.is_dead = True
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)

                    if player_x >= self.center_x:
                        self.texture = self.dead_texture_right[self.current_texture_index]
                    else:
                        self.texture = self.dead_texture_left[self.current_texture_index]

    def update(self, delta_time, player_x, player_y):
        if self.state != 'hurt' and self.state != 'dead':
            dx = player_x - self.center_x
            dy = player_y - self.center_y

            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= self.atc_range:
                if self.state != 'atc_1':
                    self.state = 'atc_1'
                    self.current_texture_index = 0
                    self.animation_timer = 0
            elif distance <= self.vision_range:
                if distance > 0:
                    dx_normalized = dx / distance
                    dy_normalized = dy / distance
                else:
                    dx_normalized = 0
                    dy_normalized = 0

                self.center_x += dx_normalized * self.speed * delta_time
                self.center_y += dy_normalized * self.speed * delta_time

                if dx_normalized > 0.1:
                    self.face_direction = FaceDirection.RIGHT
                elif dx_normalized < -0.1:
                    self.face_direction = FaceDirection.LEFT
                self.state = 'run'
            else:
                self.state = 'idle'

    def take_damage(self, amount, player_x):
        if self.state == 'hurt':
            return False

        self.health -= amount
        if self.health <= 0:
            self.state = 'dead'
        else:
            self.state = 'hurt'
        self.current_texture_index = 0
        self.animation_timer = 0

        self.face_direction = FaceDirection.RIGHT if player_x >= self.center_x else FaceDirection.LEFT
        return True

