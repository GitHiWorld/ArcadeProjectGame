import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
from constants import FaceDirection, SCALE

class Hero(arcade.Sprite):
    def __init__(self, map_name):
        super().__init__()

        self.map_name = map_name

        self.scale = 1.0
        if self.map_name != 'images/backgrounds/map_start_artemii.tmx':
            self.speed = 300
        else:
            self.speed = 180
        self.dodge_speed = 600
        self.health = 100

        self.is_dodging = False
        self.dodge_timer = 0
        self.dodge_duration = 0.3
        self.dodge_cooldown = 0
        self.dodge_cooldown_max = 1.0
        self.dodge_direction = None

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
        self.run_textures_right = sprite_sheet_run.get_texture_grid(
            size=(128, 128),
            columns=RUN_COLUMNS,
            count=RUN_COLUMNS
        )
        self.run_textures_left = [tex.flip_horizontally() for tex in self.run_textures_right]

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

        dodge_path = 'images/pers/Knight_1/Jump.png'
        JUMP_COLUMNS = 6
        sprite_sheet_dodge = arcade.SpriteSheet(dodge_path)
        all_dodge_textures = sprite_sheet_dodge.get_texture_grid(
            size=(128, 128),
            columns=JUMP_COLUMNS,
            count=JUMP_COLUMNS
        )
        DODGE_FRAME_INDEX = 0
        self.dodge_texture_right = all_dodge_textures[DODGE_FRAME_INDEX]
        self.dodge_texture_left = self.dodge_texture_right.flip_horizontally()

        walk_path = 'images/pers/Knight_1/Walk.png'
        WALK_COLUMNS = 8
        sprite_sheet_walk = arcade.SpriteSheet(walk_path)
        self.walk_textures_right = sprite_sheet_walk.get_texture_grid(
            size=(128, 128),
            columns=WALK_COLUMNS,
            count=WALK_COLUMNS
        )
        self.walk_textures_left = [i.flip_horizontally() for i in self.walk_textures_right]

        self.current_texture_index = 0
        self.animation_timer = 0

        self.walk_delay = 0.1
        self.idle_delay = 0.2
        self.atc_1_delay = 0.1
        self.atc_2_delay = 0.1
        self.dodge_delay = 0.05

        self.state = 'idle'
        self.is_walking = False

        self.attack_cooldown = 0.5
        self.attack_timer = 0
        self.can_attack = True
        self.attack = 'atc_1'

        self.face_direction = FaceDirection.RIGHT
        self.attack_direction = FaceDirection.RIGHT

        self.texture = self.idle_textures_right[0]

        self.center_x = 100 * SCALE
        self.center_y = HEIGHT * 1.8

    def set_attack_direction(self, mouse_x):
        if mouse_x >= self.center_x:
            self.attack_direction = FaceDirection.RIGHT
        else:
            self.attack_direction = FaceDirection.LEFT

    def update_animation(self, delta_time: float):
        self.animation_timer += delta_time

        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= delta_time

        if self.state == 'walk':
            if self.animation_timer >= self.walk_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.walk_textures_right)
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures_right[self.current_texture_index]
                else:
                    self.texture = self.walk_textures_left[self.current_texture_index]

        if self.state == 'run':
            if self.animation_timer >= self.walk_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.run_textures_right)
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.run_textures_right[self.current_texture_index]
                else:
                    self.texture = self.run_textures_left[self.current_texture_index]

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

        elif self.state == 'atc_2':
            if self.animation_timer >= self.atc_2_delay:
                self.animation_timer = 0
                if self.current_texture_index == len(self.atc_2_texture_right) - 1:
                    self.state = 'idle'
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)
                    if self.attack_direction == FaceDirection.RIGHT:
                        self.texture = self.atc_2_texture_right[self.current_texture_index]
                    else:
                        self.texture = self.atc_2_texture_left[self.current_texture_index]

        elif self.state == 'dodge':
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.dodge_texture_right
            else:
                self.texture = self.dodge_texture_left

            self.dodge_timer -= delta_time
            if self.dodge_timer <= 0:
                self.is_dodging = False
                self.state = 'idle'
                self.current_texture_index = 0
                self.animation_timer = 0

    def dodge(self, direction=None):
        if not self.is_dodging and self.dodge_cooldown <= 0 and self.map_name != 'images/backgrounds/map_start_artemii.tmx':
            self.state = 'dodge'
            self.is_dodging = True
            self.dodge_timer = self.dodge_duration
            self.dodge_cooldown = self.dodge_cooldown_max

            if direction is None:
                self.dodge_direction = self.face_direction
            else:
                self.dodge_direction = direction

            if self.dodge_direction != self.face_direction:
                if self.dodge_direction == FaceDirection.RIGHT:
                    self.texture = self.dodge_texture_right
                else:
                    self.texture = self.dodge_texture_left

    def update(self, delta_time, keys_pressed):
        if not self.can_attack:
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_cooldown:
                self.can_attack = True
                self.attack_timer = 0

        dx, dy = 0, 0

        if arcade.key.SPACE in keys_pressed and self.map_name != 'images/backgrounds/map_start_artemii.tmx':
            if not self.is_dodging and self.dodge_cooldown <= 0:
                self.dodge()

        if self.is_dodging:
            current_speed = self.dodge_speed
            if self.dodge_direction == FaceDirection.LEFT:
                dx -= current_speed * delta_time
            elif self.dodge_direction == FaceDirection.RIGHT:
                dx += current_speed * delta_time
        else:
            current_speed = self.speed
            if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
                dx -= current_speed * delta_time
                if not self.is_dodging:
                    self.face_direction = FaceDirection.LEFT
            if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
                dx += current_speed * delta_time
                if not self.is_dodging:
                    self.face_direction = FaceDirection.RIGHT

        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += current_speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= current_speed * delta_time

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

        if not self.is_dodging and self.state not in ['atc_1', 'atc_2']:
            self.is_walking = bool(dx or dy)
            if self.is_walking and self.map_name != 'images/backgrounds/map_start_artemii.tmx':
                self.state = 'run'
            elif self.is_walking and self.map_name == 'images/backgrounds/map_start_artemii.tmx':
                self.state = 'walk'
            else:
                self.state = 'idle'

    def try_attack(self, mouse_x):
        if self.can_attack and self.map_name != 'images/backgrounds/map_start_artemii.tmx':
            self.can_attack = False
            self.attack_timer = 0

            self.set_attack_direction(mouse_x)

            self.face_direction = self.attack_direction

            if self.attack == 'atc_1':
                self.state = 'atc_1'
                self.attack = 'atc_2'

                if self.attack_direction == FaceDirection.RIGHT:
                    self.texture = self.atc_1_texture_right[0]
                else:
                    self.texture = self.atc_1_texture_left[0]

            elif self.attack == 'atc_2':
                self.state = 'atc_2'
                self.attack = 'atc_1'

                if self.attack_direction == FaceDirection.RIGHT:
                    self.texture = self.atc_2_texture_right[0]
                else:
                    self.texture = self.atc_2_texture_left[0]

            self.current_texture_index = 0
            self.animation_timer = 0



            return True
        else:
            return False



