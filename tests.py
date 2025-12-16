import os
import arcade

# Проверьте путь
font_path = 'fonts/Comic Sans MS Pixel/Comic Sans MS Pixel.ttf'
print(f"Файл шрифта существует: {os.path.exists(font_path)}")
print(f"Полный путь: {os.path.abspath(font_path)}")