import arcade

# Константы
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 620
SCREEN_TITLE = "Balls"
CELL_SIZE = 40
INDENT = 10  # Отступ от края окна

# Цвета шариков (по кругу)
COLORS = [
    arcade.color.RED,
    arcade.color.GREEN,
    arcade.color.BLUE,
    arcade.color.YELLOW,
    arcade.color.VIOLET
]


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title):
        super().__init__(screen_width, screen_height, screen_title)

        self.rows = (screen_height - 2 * INDENT) // CELL_SIZE
        self.cols = (screen_width - 2 * INDENT) // CELL_SIZE

        self.radius = CELL_SIZE // 2 - 2

    def setup(self):
        # Создаём пустую сетку нужного размера
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def on_draw(self):
        self.clear()
        # Рисуем сетку, цвет arcade.color.GRAY
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * CELL_SIZE + CELL_SIZE // 2 + INDENT
                y = row * CELL_SIZE + CELL_SIZE // 2 + INDENT

                # Для красоты рисуем границы, чтобы всё не сливалось
                arcade.draw_rect_outline(arcade.rect.XYWH(x, y,
                                                          CELL_SIZE,
                                                          CELL_SIZE),
                                         arcade.color.GRAY, 1)
        # Рисуем шарики, если они есть
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * CELL_SIZE + CELL_SIZE // 2 + INDENT
                y = row * CELL_SIZE + CELL_SIZE // 2 + INDENT
                if self.grid[row][col]:
                    ind = self.grid[row][col] - 1
                    arcade.draw_circle_filled(x, y, self.radius, COLORS[ind])

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мыши"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Преобразуем экранные координаты в индексы сетки
            col = int((x - INDENT) // CELL_SIZE)
            row = int((y - INDENT) // CELL_SIZE)
            # Проверяем границы
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.grid[row][col] %= len(COLORS)
                self.grid[row][col] += 1


def setup_game(width=820, height=620, title="Balls"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()