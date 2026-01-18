import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
from constants import FaceDirection, SCALE


class Boss(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.base_speed = 250
        self.speed = self.base_speed * SCALE
        self.health = 1000

        self.scale = 1.8 * SCALE

        self.atc_range = 80 * SCALE
        self.vision_range = 700 * SCALE

        self.last_damage_time = 0
        self.is_dead = False

        self.center_x = 0
        self.center_y = 0

        idle_path = 'images/pers/enemy/skelet/Skeleton_Archer/Idle.png'
        IDLE_COLUMNS = 7
        sprite_sheet_idle = arcade.SpriteSheet(idle_path)
        self.idle_textures_right = sprite_sheet_idle.get_texture_grid(
            size=(128, 128),
            columns=IDLE_COLUMNS,
            count=IDLE_COLUMNS
        )
        self.idle_textures_left = [tex.flip_horizontally() for tex in self.idle_textures_right]


        walk_path = 'images/pers/enemy/skelet/Skeleton_Archer/Walk.png'
        WALK_COLUMNS = 8
        sprite_sheet_walk = arcade.SpriteSheet(walk_path)
        self.walk_textures_right = sprite_sheet_walk.get_texture_grid(
            size=(128, 128),
            columns=WALK_COLUMNS,
            count=WALK_COLUMNS
        )
        self.walk_textures_left = [tex.flip_horizontally() for tex in self.walk_textures_right]

        hurt_path = 'images/pers/enemy/skelet/Skeleton_Archer/Hurt.png'
        HURT_COLUMNS = 2
        sprite_sheet_hurt = arcade.SpriteSheet(hurt_path)
        self.hurt_textures_right = sprite_sheet_hurt.get_texture_grid(
            size=(128, 128),
            columns=HURT_COLUMNS,
            count=HURT_COLUMNS
        )
        self.hurt_textures_left = [tex.flip_horizontally() for tex in self.hurt_textures_right]

        dead_path = 'images/pers/enemy/skelet/Skeleton_Archer/Dead.png'
        DEAD_COLUMNS = 5
        sprite_sheet_dead = arcade.SpriteSheet(dead_path)
        self.dead_textures_right = sprite_sheet_dead.get_texture_grid(
            size=(128, 128),
            columns=DEAD_COLUMNS,
            count=DEAD_COLUMNS
        )
        self.dead_textures_left = [tex.flip_horizontally() for tex in self.dead_textures_right]

        attack_1_path = 'images/pers/enemy/skelet/Skeleton_Archer/Attack_1.png'
        ATTACK_1_COLUMNS = 5  # Укажи правильное количество колонок
        sprite_sheet_attack_1 = arcade.SpriteSheet(attack_1_path)
        self.attack_1_textures_right = sprite_sheet_attack_1.get_texture_grid(
            size=(128, 128),
            columns=ATTACK_1_COLUMNS,
            count=ATTACK_1_COLUMNS
        )
        self.attack_1_textures_left = [tex.flip_horizontally() for tex in self.attack_1_textures_right]

        attack_2_path = 'images/pers/enemy/skelet/Skeleton_Archer/Attack_2.png'
        ATTACK_2_COLUMNS = 4
        sprite_sheet_attack_2 = arcade.SpriteSheet(attack_2_path)
        self.attack_2_textures_right = sprite_sheet_attack_2.get_texture_grid(
            size=(128, 128),
            columns=ATTACK_2_COLUMNS,
            count=ATTACK_2_COLUMNS
        )
        self.attack_2_textures_left = [tex.flip_horizontally() for tex in self.attack_2_textures_right]

        shot_1_path = 'images/pers/enemy/skelet/Skeleton_Archer/Shot_1.png'
        SHOT_1_COLUMNS = 5
        sprite_sheet_shot_1 = arcade.SpriteSheet(shot_1_path)
        self.shot_1_textures_right = sprite_sheet_shot_1.get_texture_grid(
            size=(128, 128),
            columns=SHOT_1_COLUMNS,
            count=SHOT_1_COLUMNS
        )
        self.shoot_1_textures_left = [tex.flip_horizontally() for tex in self.shot_1_textures_right]

        self.texture = self.idle_textures_right[0]

        self.current_texture_index = 0
        self.animation_timer = 0
        self.state = 'idle'
        self.face_direction = FaceDirection.RIGHT

        self.idle_delay = 0.15
        self.walk_delay = 0.1
        self.attack_1_delay = 0.12
        self.attack_2_delay = 0.12
        self.shoot_1_delay = 0.15
        self.hurt_delay = 0.1
        self.dead_delay = 0.2

    def update_animation(self, delta_time, player_x):
        self.animation_timer += delta_time

        if self.state == 'idle':
            if self.animation_timer >= self.idle_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.idle_textures_right)
                if player_x >= self.center_x:
                    self.texture = self.idle_textures_right[self.current_texture_index]
                    self.face_direction = FaceDirection.RIGHT
                else:
                    self.texture = self.idle_textures_left[self.current_texture_index]
                    self.face_direction = FaceDirection.LEFT

        elif self.state == 'walk':
            if self.animation_timer >= self.walk_delay:
                self.animation_timer = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(self.walk_textures_right)
                if player_x >= self.center_x:
                    self.texture = self.walk_textures_right[self.current_texture_index]
                    self.face_direction = FaceDirection.RIGHT
                else:
                    self.texture = self.walk_textures_left[self.current_texture_index]
                    self.face_direction = FaceDirection.LEFT

        elif self.state == 'hurt':
            if self.animation_timer >= self.hurt_delay:
                self.animation_timer = 0
                if self.current_texture_index == len(self.hurt_textures_right) - 1:
                    self.state = 'idle'
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)
                    if player_x >= self.center_x:
                        self.texture = self.hurt_textures_right[self.current_texture_index]
                        self.face_direction = FaceDirection.RIGHT
                    else:
                        self.texture = self.hurt_textures_left[self.current_texture_index]
                        self.face_direction = FaceDirection.LEFT

        elif self.state == 'dead':
            if self.animation_timer >= self.dead_delay:
                self.animation_timer = 0
                if self.current_texture_index < len(self.dead_textures_right) - 1:
                    self.current_texture_index += 1
                    if player_x >= self.center_x:
                        self.texture = self.dead_textures_right[self.current_texture_index]
                    else:
                        self.texture = self.dead_textures_left[self.current_texture_index]
                else:
                    self.is_dead = True

        elif self.state == 'attack_1':
            if self.animation_timer >= self.attack_1_delay:
                self.animation_timer = 0
                if self.current_texture_index == len(self.attack_1_textures_right) - 1:
                    self.state = 'idle'
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)
                    if player_x >= self.center_x:
                        self.texture = self.attack_1_textures_right[self.current_texture_index]
                        self.face_direction = FaceDirection.RIGHT
                    else:
                        self.texture = self.attack_1_textures_left[self.current_texture_index]
                        self.face_direction = FaceDirection.LEFT

        elif self.state == 'attack_2':
            if self.animation_timer >= self.attack_2_delay:
                self.animation_timer = 0
                if self.current_texture_index == len(self.attack_2_textures_right) - 1:
                    self.state = 'idle'  # Возвращаемся в состояние покоя после атаки
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)
                    if player_x >= self.center_x:
                        self.texture = self.attack_2_textures_right[self.current_texture_index]
                        self.face_direction = FaceDirection.RIGHT
                    else:
                        self.texture = self.attack_2_textures_left[self.current_texture_index]
                        self.face_direction = FaceDirection.LEFT

        elif self.state == 'shot_1':
            if self.animation_timer >= self.shoot_1_delay:
                self.animation_timer = 0
                if self.current_texture_index == len(self.shot_1_textures_right) - 1:
                    self.state = 'idle'
                    self.current_texture_index = 0
                else:
                    self.current_texture_index = (self.current_texture_index + 1)
                    if player_x >= self.center_x:
                        self.texture = self.shot_1_textures_right[self.current_texture_index]
                        self.face_direction = FaceDirection.RIGHT
                    else:
                        self.texture = self.shoot_1_textures_left[self.current_texture_index]
                        self.face_direction = FaceDirection.LEFT

    def update(self, delta_time, player_x, player_y):
        if self.state != 'hurt' and self.state != 'dead':
            dx = player_x - self.center_x
            dy = player_y - self.center_y

            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= self.atc_range:
                if self.state not in ['attack_1', 'attack_2']:
                    attack_type = random.choice(['attack_1', 'attack_2'])
                    self.state = attack_type
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

                if self.state not in ['shot_1', 'attack_1', 'attack_2'] and random.random() < 0.01:
                    self.state = 'shot_1'
                    self.current_texture_index = 0
                    self.animation_timer = 0
                else:
                    self.state = 'walk'
            else:
                self.state = 'idle'

    def take_damage(self, amount, player_x):
        if self.state == 'dead' or self.is_dead:
            return False

        current_time = time.time()
        if current_time - self.last_damage_time < 0.1:
            return False

        self.last_damage_time = current_time

        self.health -= amount
        if self.health <= 0:
            self.state = 'dead'
            self.health = 0
            self.is_dead = False
            self.current_texture_index = 0
            self.animation_timer = 0
            if player_x >= self.center_x:
                self.texture = self.dead_textures_right[0]
                self.face_direction = FaceDirection.RIGHT
            else:
                self.texture = self.dead_textures_left[0]
                self.face_direction = FaceDirection.LEFT
            return True
        else:
            self.state = 'hurt'
            self.current_texture_index = 0
            self.animation_timer = 0
            self.face_direction = FaceDirection.RIGHT if player_x >= self.center_x else FaceDirection.LEFT
            return True