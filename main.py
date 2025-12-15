import arcade
import math
import random

WIDTH = 1300
HEIGHT = 900
TITLE = 'Wyvern: The Path to the Crown of Heaven'


class Start_menu(arcade.Window):
    def __init__(self, width, height, title):
        size = arcade.get_display_size()
        if isinstance(size, tuple):
            self.w = size[0]
            self.h = size[1]
        super().__init__(width, height, title, fullscreen=True)
        self.texture = arcade.load_texture('images/backgrounds/start_menu.jpg')

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h))


def main():
    game = Start_menu(WIDTH, HEIGHT, TITLE)
    arcade.run()


if __name__ == "__main__":
    main()