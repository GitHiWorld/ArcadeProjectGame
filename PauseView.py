import arcade
from constants import WIDTH, HEIGHT, cursor, SCALE
from SettingsView import SettingsView


class PauseView(arcade.View):
    def __init__(self, game_view, menu_view):
        super().__init__()
        self.game_view = game_view
        self.menu_view = menu_view

        self.w = WIDTH

        button_scale = 0.5 * SCALE
        if WIDTH == 3840:
            button_scale = 1.0

        main_menu_scale = 0.255 * SCALE
        if WIDTH == 3840:
            main_menu_scale = 0.51

        self.play = arcade.Sprite('images/sprites/play.png', scale=button_scale)
        self.settings = arcade.Sprite('images/sprites/settings.png', scale=button_scale)
        self.exit_game = arcade.Sprite('images/sprites/exit.png', scale=button_scale)
        self.main_menu = arcade.Sprite('images/sprites/main_menu.png', scale=main_menu_scale)

        self.update_button_positions()

        self.button_list = arcade.SpriteList()

        self.button_list.append(self.play)
        self.button_list.append(self.settings)
        self.button_list.append(self.exit_game)
        self.button_list.append(self.main_menu)

        cursor(self)

        self.pressed_button = None

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_rect_filled(arcade.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT), (0, 0, 0, 150))
        self.button_list.draw()
        self.cursors_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)

    def on_show_view(self):
        cursor(self)

    def update_button_positions(self):
        center_x = self.width // 2
        button_spacing = 80 * SCALE

        self.play.center_y = int(self.height * 0.7)
        self.main_menu.center_y = int(self.height * 0.7 - button_spacing)
        self.settings.center_y = int(self.height * 0.7 - button_spacing * 2)
        self.exit_game.center_y = int(self.height * 0.7 - button_spacing * 3)

        self.play.center_x = center_x
        self.settings.center_x = center_x
        self.exit_game.center_x = center_x
        self.main_menu.center_x = center_x

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        clicked_sprites = arcade.get_sprites_at_point((x, y), self.button_list)

        if not clicked_sprites:
            return

        clicked = clicked_sprites[-1]
        self.pressed_button = clicked

        if clicked == self.play:
            self.window.show_view(self.game_view)
        elif clicked == self.settings:
            settings_view = SettingsView(self)
            self.window.show_view(settings_view)
        elif clicked == self.exit_game:
            arcade.exit()
        elif clicked == self.main_menu:
            self.window.show_view(self.menu_view)

    def on_mouse_release(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if hasattr(self, 'pressed_button') and self.pressed_button is not None:
            self.pressed_button = None

    def on_mouse_motion(self, x, y, dx, dy):
        base_scale = 0.5 * SCALE
        hover_scale = base_scale * 1.1
        main_menu_base = 0.255 * SCALE
        main_menu_hover = main_menu_base * 1.1

        if WIDTH == 3840:
            base_scale = 1.0
            hover_scale = 1.2
            main_menu_base = 0.51
            main_menu_hover = 0.57

        for btn in self.button_list:
            if btn == self.main_menu:
                btn.scale = main_menu_base
            else:
                btn.scale = base_scale

        check = arcade.get_sprites_at_point((x, y), self.button_list)
        if check:
            checkin = check[-1]
            if checkin == self.main_menu:
                checkin.scale = main_menu_hover
            else:
                checkin.scale = hover_scale

        if hasattr(self, 'cursor'):
            self.cursor.center_x = x
            self.cursor.center_y = y