import arcade
size = arcade.get_display_size()
WIDTH = size[0]
HEIGHT = size[1]
TITLE = 'Wyvern: The Path to the Crown of Heaven'

def cursor(self):
    self.cursor = arcade.Sprite('images/cursors/pixel_cursors/Tiles/tile_0202.png', scale=1.2)
    self.cursor.center_x = 0
    self.cursor.center_y = 0
    # self.cursor_w = self.cursor.width
    # self.cursor_h = self.cursor.height
    # self.cursor_scale = 1.2
    self.cursors_list = arcade.SpriteList()
    self.cursors_list.append(self.cursor)