import arcade
from constants import WIDTH, HEIGHT, cursor, SCALE



class SettingsView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.w = WIDTH
        self.h = HEIGHT

        if WIDTH == 3840:
            self.back_button = arcade.Sprite('images/sprites/back_button.png', scale=1)
            self.sound_on = arcade.Sprite('images/sprites/sound_on.png', scale=1)
            self.sound_off = arcade.Sprite('images/sprites/sound_off.png', scale=1)
        else:
            self.back_button = arcade.Sprite('images/sprites/back_button.png', scale=0.5)
            self.sound_on = arcade.Sprite('images/sprites/sound_on.png', scale=0.5)
            self.sound_off = arcade.Sprite('images/sprites/sound_off.png', scale=0.5)

        arcade.load_font('fonts/Comic Sans MS Pixel/Comic Sans MS Pixel.ttf')
        self.title = arcade.Text("Настройки", WIDTH // 2, HEIGHT * 0.8,
                                 arcade.color.WHITE,
                                 font_size=50 * SCALE,
                                 font_name="Comic Sans MS pixel rus eng",
                                 anchor_x='center')

        self.sound_text = arcade.Text("Звук:", WIDTH // 2 - 150 * SCALE, HEIGHT * 0.6,
                                      arcade.color.WHITE,
                                      font_size=30 * SCALE,
                                      font_name="Comic Sans MS pixel rus eng")

        self.back_text = arcade.Text("Назад", WIDTH // 2, HEIGHT * 0.3,
                                     arcade.color.WHITE,
                                     font_size=30 * SCALE,
                                     font_name="Comic Sans MS pixel rus eng",
                                     anchor_x='center')

        self.button_list = arcade.SpriteList()
        self.button_list.append(self.back_button)
        self.button_list.append(self.sound_on)
        self.button_list.append(self.sound_off)

        self.text_list = arcade.SpriteList()

        self.update_button_positions()

        self.sound_enabled = True
        self.show_sound_button()

        cursor(self)
        self.pressed_button = None

    def update_button_positions(self):
        self.back_button.center_x = self.width // 2
        self.back_button.center_y = self.height * 0.3

        self.sound_on.center_x = self.width // 2 + 100 * SCALE
        self.sound_off.center_x = self.width // 2 + 100 * SCALE
        self.sound_on.center_y = self.height * 0.6
        self.sound_off.center_y = self.height * 0.6

        # Обновляем позиции текста
        self.sound_text.x = self.width // 2 - 150 * SCALE
        self.sound_text.y = self.height * 0.6
        self.back_text.x = self.width // 2
        self.back_text.y = self.height * 0.3
        self.title.x = self.width // 2
        self.title.y = self.height * 0.8

    def show_sound_button(self):
        self.sound_on.visible = self.sound_enabled
        self.sound_off.visible = not self.sound_enabled

    def on_draw(self):
        self.clear()

        arcade.draw_rect_filled(arcade.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT),
                                (0, 0, 0, 200))

        self.title.draw()
        self.sound_text.draw()
        self.back_text.draw()

        self.button_list.draw()

        self.cursors_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        clicked_sprites = arcade.get_sprites_at_point((x, y), self.button_list)

        if not clicked_sprites:
            return

        clicked = clicked_sprites[-1]
        self.pressed_button = clicked

        if clicked == self.back_button:
            self.window.show_view(self.menu_view)
        elif clicked == self.sound_on:
            self.sound_enabled = False
            # Отключаем звук в главном меню
            if hasattr(self.menu_view, 'sound') and self.menu_view.sound:
                self.menu_view.sound.pause()
            self.show_sound_button()
        elif clicked == self.sound_off:
            self.sound_enabled = True
            # Включаем звук в главном меню
            if hasattr(self.menu_view, 'sound') and self.menu_view.sound:
                self.menu_view.sound.play(loop=True, volume=0.5)
            self.show_sound_button()

    def on_mouse_release(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if hasattr(self, 'pressed_button') and self.pressed_button is not None:
            self.pressed_button = None

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.button_list:
            check = arcade.get_sprites_at_point((x, y), self.button_list)
            if check and btn in check:
                if btn == self.back_button:
                    btn.color = arcade.color.LIGHT_BLUE
                elif btn == self.sound_on:
                    btn.color = arcade.color.LIGHT_GREEN
                elif btn == self.sound_off:
                    btn.color = arcade.color.LIGHT_SALMON
            else:
                if btn == self.back_button:
                    btn.color = arcade.color.BLUE
                elif btn == self.sound_on:
                    btn.color = arcade.color.GREEN
                elif btn == self.sound_off:
                    btn.color = arcade.color.RED

        self.cursor.center_x = x
        self.cursor.center_y = y

    def on_show_view(self):
        cursor(self)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.w = width
        self.h = height
        self.update_button_positions()