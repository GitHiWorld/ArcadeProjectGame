import arcade
import math
import random

from pyglet.event import EVENT_HANDLE_STATE

WIDTH = 5120
HEIGHT = 2580
TITLE = 'Wyvern: The Path to the Crown of Heaven'


class Start_menu(arcade.Window):
    def __init__(self):
        size = arcade.get_display_size()

        if isinstance(size, tuple):
            self.w = size[0]
            self.h = size[1]

        super().__init__(self.w, self.h, TITLE, fullscreen=True)

        self.texture = arcade.load_texture('images/backgrounds/start_menu.jpg')
        arcade.load_font('fonts/Comic Sans MS Pixel/Comic Sans MS Pixel.ttf')
        self.background_sound = arcade.load_sound('sounds/Flappy Dragon - Wispernalia.mp3')

        self.set_mouse_visible(False)
        # self.painter_cur = arcade.Sprite('images/cursors/modest-dark/Windows/pointer.cur')
#        self.link_cur = arcade.Sprite('images/cursors/modest-dark/Windows/link.cur')
        self.painter_cur = arcade.load_texture('images/cursors/modest-dark/Windows/pointer.cur')
        self.cursor_w = self.painter_cur.width
        self.cursor_h = self.painter_cur.height
        self.cursor_x = self.w // 2
        self.cursor_y = self.h // 2

        arcade.play_sound(self.background_sound, loop=True, volume=0.1)

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
                'rotation': random.uniform(0,360),
                'rot_speed': random.uniform(-10, 10)
            }
            )

        self.text_main = arcade.Text('Wyvern: The Path to the Crown of Heaven', self.w // 2, self.h * 0.8, arcade.color.APRICOT,
                         font_size=46, font_name="Comic Sans MS pixel rus eng", anchor_x='center', anchor_y='top')
    def on_setup(self):
        pass

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
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h))
        # arcade.draw_texture_rect(self.texture_title, arcade.XYWH(self.w // 2, self.h - 30, self.w // 1.1, self.h // 3.2))

        self.text_main.draw()

        for i in self.parcticles:
            arcade.draw_rect_filled(arcade.rect.XYWH(i['x'], i['y'], i['size'], i['size']), i['color'], i['rotation'])

        arcade.draw_texture_rect(self.painter_cur, arcade.rect.XYWH(self.cursor_x, self.cursor_y, self.cursor_w, self.cursor_h))

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_x = x
        self.cursor_y = y



def main():
    game = Start_menu()
    arcade.run()


if __name__ == "__main__":
    main()