import arcade
import json
import os
from constants import WIDTH, HEIGHT, cursor, SCALE, load_settings, save_settings


class SettingsView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.w = WIDTH
        self.h = HEIGHT

        self.settings = load_settings()
        self.volume = self.settings["volume"]
        self.sound_enabled = self.settings["sound_enabled"]

        self.create_ui_elements()

        self.active_slider = None
        self.slider_being_dragged = False
        self.hovered_button = None

        cursor(self)

    def create_ui_elements(self):
        # Диалоговое окно
        dialog_width = min(600 * SCALE, self.w - 100)
        dialog_height = 400 * SCALE
        self.dialog_left = self.w // 2 - dialog_width // 2
        self.dialog_bottom = self.h // 2 - dialog_height // 2

        title_font_size = int(36 * SCALE)
        text_font_size = int(28 * SCALE)
        value_font_size = int(24 * SCALE)

        self.title_text = arcade.Text(
            "НАСТРОЙКИ",
            self.w // 2,
            self.dialog_bottom + dialog_height - 50 * SCALE,
            arcade.color.GOLD,
            font_size=title_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        sound_section_y = self.dialog_bottom + dialog_height - 120 * SCALE

        self.volume_label_text = arcade.Text(
            "Громкость:",
            self.dialog_left + 30 * SCALE,
            sound_section_y,
            arcade.color.WHITE,
            font_size=text_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_y="center"
        )

        slider_width = 300 * SCALE
        slider_height = 15 * SCALE
        self.slider_x = self.dialog_left + dialog_width - 150 * SCALE
        self.slider_y = sound_section_y
        self.slider_width = slider_width
        self.slider_height = slider_height

        self.slider_min_x = self.slider_x - slider_width // 2
        self.slider_max_x = self.slider_x + slider_width // 2

        self.slider_knob_x = self.slider_min_x + (self.volume / 100.0) * slider_width
        self.slider_knob_radius = 12 * SCALE

        self.volume_value_text = arcade.Text(
            f"{self.volume}%",
            self.slider_max_x + 50 * SCALE,
            sound_section_y,
            arcade.color.WHITE,
            font_size=value_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center"
        )

        sound_toggle_y = sound_section_y - 80 * SCALE

        self.sound_label_text = arcade.Text(
            "Звук:",
            self.dialog_left + 30 * SCALE,
            sound_toggle_y,
            arcade.color.WHITE,
            font_size=text_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_y="center"
        )

        self.toggle_x = self.slider_x
        self.toggle_y = sound_toggle_y
        self.toggle_width = 60 * SCALE
        self.toggle_height = 30 * SCALE

        buttons_y = self.dialog_bottom + 80 * SCALE

        button_width = 180 * SCALE
        button_height = 50 * SCALE
        self.apply_button_x = self.w // 2 - button_width - 20 * SCALE
        self.apply_button_y = buttons_y

        self.apply_text = arcade.Text(
            "ПРИМЕНИТЬ",
            self.apply_button_x + button_width // 2,
            self.apply_button_y,
            arcade.color.WHITE,
            font_size=value_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        self.cancel_button_x = self.w // 2 + 20 * SCALE
        self.cancel_button_y = buttons_y

        self.cancel_text = arcade.Text(
            "ОТМЕНА",
            self.cancel_button_x + button_width // 2,
            self.cancel_button_y,
            arcade.color.WHITE,
            font_size=value_font_size,
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def on_draw(self):
        self.clear()

        arcade.draw_lrbt_rectangle_filled(
            0, self.w, 0, self.h,
            (0, 0, 0, 180)
        )

        dialog_width = min(600 * SCALE, self.w - 100)
        dialog_height = 400 * SCALE
        dialog_left = self.w // 2 - dialog_width // 2
        dialog_bottom = self.h // 2 - dialog_height // 2

        arcade.draw_lbwh_rectangle_filled(
            dialog_left,
            dialog_bottom,
            dialog_width,
            dialog_height,
            (40, 40, 50, 240)
        )

        arcade.draw_lbwh_rectangle_outline(
            dialog_left,
            dialog_bottom,
            dialog_width,
            dialog_height,
            (100, 100, 120, 255),
            2 * SCALE
        )

        arcade.draw_lbwh_rectangle_filled(
            dialog_left,
            dialog_bottom + dialog_height - 80 * SCALE,
            dialog_width,
            80 * SCALE,
            (60, 60, 80, 255)
        )

        self.title_text.draw()

        self.volume_label_text.draw()

        arcade.draw_lbwh_rectangle_filled(
            self.slider_min_x,
            self.slider_y - self.slider_height // 2,
            self.slider_width, self.slider_height,
            (80, 80, 100, 255)
        )

        fill_width = (self.slider_knob_x - self.slider_min_x)
        if fill_width > 0:
            arcade.draw_lbwh_rectangle_filled(
                self.slider_min_x,
                self.slider_y - self.slider_height // 2,
                fill_width, self.slider_height,
                (100, 180, 255, 255)
            )

        knob_color = (120, 200, 255) if self.active_slider == "volume" else (80, 160, 220)
        arcade.draw_circle_filled(
            self.slider_knob_x, self.slider_y,
            self.slider_knob_radius,
            knob_color
        )
        arcade.draw_circle_outline(
            self.slider_knob_x, self.slider_y,
            self.slider_knob_radius,
            arcade.color.WHITE, 2 * SCALE
        )

        self.volume_value_text.text = f"{self.volume}%"
        self.volume_value_text.draw()

        self.sound_label_text.draw()

        toggle_color = (60, 200, 80) if self.sound_enabled else (200, 60, 60)
        arcade.draw_lbwh_rectangle_filled(
            self.toggle_x - self.toggle_width // 2,
            self.toggle_y - self.toggle_height // 2,
            self.toggle_width, self.toggle_height,
            toggle_color
        )

        button_offset = self.toggle_width // 4 if self.sound_enabled else -self.toggle_width // 4
        arcade.draw_circle_filled(
            self.toggle_x + button_offset,
            self.toggle_y,
            self.toggle_height // 2 - 2 * SCALE,
            (240, 240, 240, 255)
        )

        state_text = "ВКЛ" if self.sound_enabled else "ВЫКЛ"
        state_color = arcade.color.WHITE
        arcade.draw_text(
            state_text,
            self.toggle_x,
            self.toggle_y,
            state_color,
            font_size=int(18 * SCALE),
            font_name="Comic Sans MS pixel rus eng",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        button_width = 180 * SCALE
        button_height = 50 * SCALE

        apply_color = (60, 180, 80) if self.hovered_button == "apply" else (40, 140, 60)
        arcade.draw_lbwh_rectangle_filled(
            self.apply_button_x,
            self.apply_button_y - button_height // 2,
            button_width, button_height,
            apply_color
        )
        arcade.draw_lbwh_rectangle_outline(
            self.apply_button_x,
            self.apply_button_y - button_height // 2,
            button_width, button_height,
            (255, 255, 255, 255), 2 * SCALE
        )
        self.apply_text.draw()

        cancel_color = (180, 60, 60) if self.hovered_button == "cancel" else (140, 40, 40)
        arcade.draw_lbwh_rectangle_filled(
            self.cancel_button_x,
            self.cancel_button_y - button_height // 2,
            button_width, button_height,
            cancel_color
        )
        arcade.draw_lbwh_rectangle_outline(
            self.cancel_button_x,
            self.cancel_button_y - button_height // 2,
            button_width, button_height,
            (255, 255, 255, 255), 2 * SCALE
        )
        self.cancel_text.draw()

        self.cursors_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        distance_to_knob = abs(x - self.slider_knob_x)
        if distance_to_knob <= self.slider_knob_radius * 1.5:
            self.active_slider = "volume"
            self.slider_being_dragged = True
            return

        if (self.slider_min_x <= x <= self.slider_max_x and
                self.slider_y - self.slider_height * 2 <= y <= self.slider_y + self.slider_height * 2):
            self.active_slider = "volume"
            self.slider_being_dragged = True
            self.update_slider_value(x)
            return

        toggle_left = self.toggle_x - self.toggle_width // 2
        toggle_right = self.toggle_x + self.toggle_width // 2
        toggle_bottom = self.toggle_y - self.toggle_height // 2
        toggle_top = self.toggle_y + self.toggle_height // 2

        if (toggle_left <= x <= toggle_right and toggle_bottom <= y <= toggle_top):
            self.sound_enabled = not self.sound_enabled
            return

        button_width = 180 * SCALE
        button_height = 50 * SCALE

        apply_left = self.apply_button_x
        apply_right = self.apply_button_x + button_width
        apply_bottom = self.apply_button_y - button_height // 2
        apply_top = self.apply_button_y + button_height // 2

        if (apply_left <= x <= apply_right and apply_bottom <= y <= apply_top):
            self.settings["volume"] = self.volume
            self.settings["sound_enabled"] = self.sound_enabled

            if save_settings(self.settings):
                self.window.show_view(self.menu_view)
            return

        cancel_left = self.cancel_button_x
        cancel_right = self.cancel_button_x + button_width
        cancel_bottom = self.cancel_button_y - button_height // 2
        cancel_top = self.cancel_button_y + button_height // 2

        if (cancel_left <= x <= cancel_right and cancel_bottom <= y <= cancel_top):
            self.settings = load_settings()
            self.volume = self.settings["volume"]
            self.sound_enabled = self.settings["sound_enabled"]
            self.create_ui_elements()
            self.window.show_view(self.menu_view)
            return

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.active_slider = None
            self.slider_being_dragged = False
            self.hovered_button = None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.slider_being_dragged and self.active_slider == "volume":
            self.update_slider_value(x)

        self.hovered_button = None
        button_width = 180 * SCALE
        button_height = 50 * SCALE

        apply_left = self.apply_button_x
        apply_right = self.apply_button_x + button_width
        apply_bottom = self.apply_button_y - button_height // 2
        apply_top = self.apply_button_y + button_height // 2

        if (apply_left <= x <= apply_right and apply_bottom <= y <= apply_top):
            self.hovered_button = "apply"

        cancel_left = self.cancel_button_x
        cancel_right = self.cancel_button_x + button_width
        cancel_bottom = self.cancel_button_y - button_height // 2
        cancel_top = self.cancel_button_y + button_height // 2

        if (cancel_left <= x <= cancel_right and cancel_bottom <= y <= cancel_top):
            self.hovered_button = "cancel"

        self.cursor.center_x = x
        self.cursor.center_y = y

    def update_slider_value(self, mouse_x):
        knob_x = max(self.slider_min_x, min(mouse_x, self.slider_max_x))

        self.volume = int(((knob_x - self.slider_min_x) / self.slider_width) * 100)
        self.slider_knob_x = knob_x

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.settings = load_settings()
            self.volume = self.settings["volume"]
            self.sound_enabled = self.settings["sound_enabled"]
            self.create_ui_elements()
            self.window.show_view(self.menu_view)

    def on_show_view(self):
        cursor(self)
        self.settings = load_settings()
        self.volume = self.settings["volume"]
        self.sound_enabled = self.settings["sound_enabled"]
        self.create_ui_elements()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.w = width
        self.h = height
        self.create_ui_elements()