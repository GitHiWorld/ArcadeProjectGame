import arcade
import enum

arcade.load_font('fonts/Comic Sans MS Pixel/Comic Sans MS Pixel.ttf')
size = arcade.get_display_size()
WIDTH = size[0]
HEIGHT = size[1]
TITLE = 'Wyvern: The Path to the Crown of Heaven'
DEAD_ZONE_W = int(WIDTH * 0.35)
DEAD_ZONE_H = int(HEIGHT * 0.45)
CAMERA_LERP = 0.1
TILE_SCALING = 1
BASE_WIDTH = 1920
SCALE = WIDTH / BASE_WIDTH


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


def cursor(self):
    self.cursor = arcade.Sprite('images/cursors/pixel_cursors/Tiles/tile_0202.png', scale=1.2)
    self.cursor.center_x = self.window._mouse_x if hasattr(self.window, '_mouse_x') else self.w // 2
    self.cursor.center_y = self.window._mouse_y if hasattr(self.window, '_mouse_y') else self.h // 2
    self.cursors_list = arcade.SpriteList()
    self.cursors_list.append(self.cursor)
    self.window.set_mouse_visible(False)