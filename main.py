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
        # self.texture_title = arcade.load_texture('images/backgrounds/title.jpg')
        arcade.load_font('fonts/Comic Sans MS Pixel/Comic Sans MS Pixel.ttf')

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h))
        # arcade.draw_texture_rect(self.texture_title, arcade.XYWH(self.w // 2, self.h - 30, self.w // 1.1, self.h // 3.2))
        arcade.draw_text('Wyvern: The Path to the Crown of Heaven', self.w // 7, self.h - 50, arcade.color.NAVAJO_WHITE,
                         font_size=38, font_name='Comic Sans MS Pixel')


def main():
    game = Start_menu(WIDTH, HEIGHT, TITLE)
    arcade.run()


if __name__ == "__main__":
    main()