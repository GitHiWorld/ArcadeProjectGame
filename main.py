import arcade
import math
import random

WIDTH = 1
HEIGHT = 1
TITLE = 'Wyvern: The Path to the Crown of Heaven'


class Start_menu(arcade.Window):
    def __init__(self, width, height, title):
        size = arcade.get_display_size()

        if isinstance(size, tuple):
            self.w = size[0]
            print(size[0])
            self.h = size[1]
            print(size[1])

        super().__init__(self.w, self.h, title, fullscreen=False, resizable=True)

        self.texture = arcade.load_texture('images/backgrounds/start_menu.jpg')
        arcade.load_font('fonts/Comic Sans MS Pixel/Comic Sans MS Pixel.ttf')
        self.background_sound = arcade.load_sound('sounds/Flappy Dragon - Wispernalia.mp3')

        arcade.play_sound(self.background_sound, loop=True, volume=0.6)

        self.parcticles = []
        for i in range(350):
            self.parcticles.append({
                'x': random.uniform(0, self.w),
                'y': random.uniform(0, self.h),
                'size': random.uniform(2, 8),
                'speed': random.uniform(5.5, 10.5),
                'color': random.choice([
                    (255, 192, 203, random.randint(0, 120)),  # Розовый (лепестки сакуры)
                    (255, 182, 193, random.randint(0, 200)),  # Светло-розовый
                    (255, 160, 122, random.randint(60, 200)),  # Светло-коралловый
                    (255, 218, 185, random.randint(60, 200)),  # Персиковый
                    (240, 230, 140, random.randint(60, 200))
                ]),
                'side_speed': random.uniform(-4, 4),
                'rotation': random.uniform(0, 360),
                'rot_speed': random.uniform(-10, 10)
            }
            )

        self.text_main = arcade.Text('Wyvern: The Path to the Crown of Heaven', self.w // 2, self.h * 0.8,
                                     arcade.color.APRICOT,
                                     font_size=46, font_name="Comic Sans MS pixel rus eng", anchor_x='center',
                                     anchor_y='top')

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.w = width
        self.h = height

        # Обновляем позицию текста
        self.text_main.x = self.w // 2
        self.text_main.y = self.h * 0.8

    def on_update(self, delta_time):
        for i in self.parcticles:
            i['y'] -= i['speed'] * delta_time
            i['x'] += i['side_speed'] * delta_time
            i['rotation'] += i['rot_speed'] * delta_time

            if i['y'] <= 0:
                i['y'] = self.h + 10
            if i['x'] <= -10:
                i['x'] = self.w + 10
            elif i['x'] >= self.w + 10:
                i['x'] = -10

    def on_draw(self):
        arcade.draw_texture_rect(self.texture,
                                 arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h))

        self.text_main.draw()

        for i in self.parcticles:
            arcade.draw_rect_filled(arcade.XYWH(i['x'], i['y'], i['size'], i['size']), i['color'], i['rotation'])


def main():
    game = Start_menu(WIDTH, HEIGHT, TITLE)
    arcade.run()


if __name__ == "__main__":
    main()