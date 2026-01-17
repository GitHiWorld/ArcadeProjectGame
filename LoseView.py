import arcade
import math
import time
import random
from constants import WIDTH, HEIGHT, cursor, SCALE, load_settings
from PauseView import PauseView
from Hero import Hero
from Skelet_enemy import Skelet


class LoseView(arcade.View):
    def __init__(self, game_window):
        super().__init__()
        self.game_window = game_window

        self.w = WIDTH
        self.h = HEIGHT

        # Создаем UI элементы
        self.create_ui_elements()

        self.hovered_button = None
        self.pressed_button = None

        cursor(self)

    def create_ui_elements(self):
        # Диалоговое окно
        dialog_width = min(500 * SCALE, self.w - 100)
        dialog_height = 300 * SCALE
        self.dialog_left = self.w // 2 - dialog_width // 2
        self.dialog_bottom = self.h // 2 - dialog_height // 2

        title_font_size = int(36 * SCALE)
        text_font_size = int(28 * SCALE)
        button_font_size = int(24 * SCALE)

        # Текст "Вы погибли"
        self.title_text = arcade.Text(
            "ВЫ ПОГИБЛИ",
            self.w // 2,
            self.dialog_bottom + dialog_height - 60 * SCALE,
            arcade.color.RED,
            font_size=title_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Сообщение
        self.message_text = arcade.Text(
            "Выберите действие:",
            self.w // 2,
            self.dialog_bottom + dialog_height - 120 * SCALE,
            arcade.color.WHITE,
            font_size=text_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center"
        )

        # Кнопки
        buttons_y = self.dialog_bottom + dialog_height - 200 * SCALE
        button_width = 200 * SCALE
        button_height = 50 * SCALE
        button_spacing = 30 * SCALE

        # Кнопка "Возродиться"
        self.respawn_button_x = self.w // 2 - button_width - button_spacing // 2
        self.respawn_button_y = buttons_y

        self.respawn_text = arcade.Text(
            "ВОЗРОДИТЬСЯ",
            self.respawn_button_x + button_width // 2,
            self.respawn_button_y,
            arcade.color.WHITE,
            font_size=button_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Кнопка "Выйти в меню"
        self.menu_button_x = self.w // 2 + button_spacing // 2
        self.menu_button_y = buttons_y

        self.menu_text = arcade.Text(
            "ВЫЙТИ В МЕНЮ",
            self.menu_button_x + button_width // 2,
            self.menu_button_y,
            arcade.color.WHITE,
            font_size=button_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Размеры кнопок для проверки наведения
        self.button_width = button_width
        self.button_height = button_height

    def on_draw(self):
        # Сначала рисуем игру на заднем плане (затемненную)
        self.clear()

        # Используем камеру игры для отрисовки
        self.game_window.world_camera.use()
        self.game_window.floor_list.draw()
        self.game_window.other_list.draw()
        self.game_window.walls_list.draw()
        self.game_window.embient_list.draw()
        self.game_window.skeleton_list.draw()

        # Рисуем игрока (возможно в анимации смерти)
        self.game_window.player_list.draw()

        # Затемняем экран
        self.game_window.gui_camera.use()
        arcade.draw_rect_filled(arcade.XYWH(
            self.w // 2, self.h // 2,
            self.w, self.h),
            (0, 0, 0, 150)  # Полупрозрачный черный
        )

        # Рисуем диалоговое окно
        dialog_width = min(500 * SCALE, self.w - 100)
        dialog_height = 300 * SCALE

        # Фон диалогового окна
        arcade.draw_rect_filled(arcade.XYWH(
            self.w // 2, self.h // 2,
            dialog_width, dialog_height),
            (40, 40, 50, 240)
        )

        # Обводка диалогового окна
        arcade.draw_rect_outline(arcade.XYWH(
            self.w // 2, self.h // 2,
            dialog_width, dialog_height),
            (100, 100, 120, 255),
            2 * SCALE
        )

        # Верхняя часть диалогового окна
        arcade.draw_rect_filled(arcade.XYWH(
            self.w // 2,
            self.h // 2 + dialog_height // 2 - 40 * SCALE,
            dialog_width,
            80 * SCALE),
            (60, 60, 80, 255)
        )

        # Тексты
        self.title_text.draw()
        self.message_text.draw()

        # Кнопка "Возродиться"
        respawn_color = (60, 180, 80) if self.hovered_button == "respawn" else (40, 140, 60)
        if self.pressed_button == "respawn":
            respawn_color = (30, 120, 40)

        arcade.draw_rect_filled(arcade.XYWH(
            self.respawn_button_x + self.button_width // 2,
            self.respawn_button_y,
            self.button_width, self.button_height),
            respawn_color
        )

        arcade.draw_rect_outline(arcade.XYWH(
            self.respawn_button_x + self.button_width // 2,
            self.respawn_button_y,
            self.button_width, self.button_height),
            (255, 255, 255, 255), 2 * SCALE
        )

        self.respawn_text.draw()

        # Кнопка "Выйти в меню"
        menu_color = (180, 60, 60) if self.hovered_button == "menu" else (140, 40, 40)
        if self.pressed_button == "menu":
            menu_color = (120, 30, 30)

        arcade.draw_rect_filled(arcade.XYWH(
            self.menu_button_x + self.button_width // 2,
            self.menu_button_y,
            self.button_width, self.button_height),
            menu_color
        )

        arcade.draw_rect_outline(arcade.XYWH(
            self.menu_button_x + self.button_width // 2,
            self.menu_button_y,
            self.button_width, self.button_height),
            (255, 255, 255, 255), 2 * SCALE
        )

        self.menu_text.draw()

        # Курсор
        self.cursors_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Проверяем нажатие на кнопку "Возродиться"
        respawn_left = self.respawn_button_x
        respawn_right = self.respawn_button_x + self.button_width
        respawn_bottom = self.respawn_button_y - self.button_height // 2
        respawn_top = self.respawn_button_y + self.button_height // 2

        if (respawn_left <= x <= respawn_right and
                respawn_bottom <= y <= respawn_top):
            self.pressed_button = "respawn"
            return

        # Проверяем нажатие на кнопку "Выйти в меню"
        menu_left = self.menu_button_x
        menu_right = self.menu_button_x + self.button_width
        menu_bottom = self.menu_button_y - self.button_height // 2
        menu_top = self.menu_button_y + self.button_height // 2

        if (menu_left <= x <= menu_right and
                menu_bottom <= y <= menu_top):
            self.pressed_button = "menu"
            return

    def on_mouse_release(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Проверяем отпускание кнопки "Возродиться"
        respawn_left = self.respawn_button_x
        respawn_right = self.respawn_button_x + self.button_width
        respawn_bottom = self.respawn_button_y - self.button_height // 2
        respawn_top = self.respawn_button_y + self.button_height // 2

        if (respawn_left <= x <= respawn_right and
                respawn_bottom <= y <= respawn_top and
                self.pressed_button == "respawn"):
            # Возрождаем игрока
            self.respawn_player()
            return

        # Проверяем отпускание кнопки "Выйти в меню"
        menu_left = self.menu_button_x
        menu_right = self.menu_button_x + self.button_width
        menu_bottom = self.menu_button_y - self.button_height // 2
        menu_top = self.menu_button_y + self.button_height // 2

        if (menu_left <= x <= menu_right and
                menu_bottom <= y <= menu_top and
                self.pressed_button == "menu"):
            # Возвращаемся в главное меню
            from StartMenu import Start_menu
            menu_view = Start_menu()
            self.window.show_view(menu_view)
            return

        self.pressed_button = None

    def on_mouse_motion(self, x, y, dx, dy):
        # Проверяем наведение на кнопки
        self.hovered_button = None

        # Проверка кнопки "Возродиться"
        respawn_left = self.respawn_button_x
        respawn_right = self.respawn_button_x + self.button_width
        respawn_bottom = self.respawn_button_y - self.button_height // 2
        respawn_top = self.respawn_button_y + self.button_height // 2

        if (respawn_left <= x <= respawn_right and
                respawn_bottom <= y <= respawn_top):
            self.hovered_button = "respawn"

        # Проверка кнопки "Выйти в меню"
        menu_left = self.menu_button_x
        menu_right = self.menu_button_x + self.button_width
        menu_bottom = self.menu_button_y - self.button_height // 2
        menu_top = self.menu_button_y + self.button_height // 2

        if (menu_left <= x <= menu_right and
                menu_bottom <= y <= menu_top):
            self.hovered_button = "menu"

        # Обновляем позицию курсора
        if hasattr(self, 'cursor'):
            self.cursor.center_x = x
            self.cursor.center_y = y

    def respawn_player(self):
        """Возрождает игрока"""
        player = self.game_window.player

        # Восстанавливаем здоровье
        player.health = 100

        # Сбрасываем состояние смерти
        player.is_dead = False
        player.state = 'idle'
        player.current_texture_index = 0
        player.animation_timer = 0

        # Устанавливаем начальные координаты в зависимости от уровня
        if self.game_window.what_level(self.game_window.map_name) == 1:
            # Для первого уровня
            player.center_x = 100 * SCALE
            player.center_y = HEIGHT * 1.8
        else:
            # Для второго уровня
            map_height_pixels = self.game_window.tile_map.height * self.game_window.tile_map.tile_height * (2.5 * SCALE)
            player.center_x = 100 * SCALE
            player.center_y = map_height_pixels // 2

        # Если игрок был удален из списка, добавляем обратно
        if player not in self.game_window.player_list:
            self.game_window.player_list.append(player)

        self.game_window.attack_hit_skeletons.clear()

        # Возвращаемся в игровое окно
        self.window.show_view(self.game_window)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # При нажатии ESC предлагаем выйти в меню
            self.pressed_button = "menu"
            from StartMenu import Start_menu
            menu_view = Start_menu()
            self.window.show_view(menu_view)

    def on_show_view(self):
        cursor(self)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.w = width
        self.h = height
        self.create_ui_elements()