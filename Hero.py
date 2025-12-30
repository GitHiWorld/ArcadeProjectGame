import time
import arcade
import math
import random
from constants import WIDTH, HEIGHT, cursor, DEAD_ZONE_H, DEAD_ZONE_W, CAMERA_LERP
from PauseView import PauseView
import enum

# Делаем класс для направления взгляда персонажа,
# это позволит не запутаться в чиселках и сделать код более читаемым
class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 1.0
        self.speed = 300
        self.health = 100

        self.idle_player = arcade.load_texture(f'images/pers/Knight_1/Idle.png')
        self.texture = self.idle_player
        self.run_player = arcade.load_texture('images/pers/Knight_1/Run.png')

        self.walk_textures = []
        for i in range():
            texture = arcade.load_texture(self.run_player, x=i * 128, y=0, width=128, height=128)
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр
        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2

    def update_animation(self, delta_time):
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()

        else:
            # Если не идём, то просто показываем текстуру покоя
            # и поворачиваем её в зависимости от направления взгляда
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_player
            else:
                self.texture = self.idle_player.flip_horizontally()

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
        # Поворачиваем персонажа в зависимости от направления движения
        # Если никуда не идём, то не меняем направление взгляда
        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT

        # Проверка на движение
        self.is_walking = dx or dy