import sys
import os

# ========== ПАТЧ ДЛЯ PYINSTALLER + ARCADE ==========
if getattr(sys, 'frozen', False):
    # Мы в собранном приложении PyInstaller
    meipass = getattr(sys, '_MEIPASS', os.path.abspath("."))

    # Создаем необходимые директории
    arcade_temp_dir = os.path.join(meipass, 'arcade')
    version_file = os.path.join(arcade_temp_dir, 'VERSION')

    # Создаем директорию если не существует
    os.makedirs(arcade_temp_dir, exist_ok=True)

    # Создаем фиктивный VERSION файл
    if not os.path.exists(version_file):
        try:
            version = "2.6.17"  # Укажите вашу версию arcade
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version)
        except Exception as e:
            pass
# ========== КОНЕЦ ПАТЧА ==========

# ========== ПАТЧ ДЛЯ ВСЕХ РЕСУРСОВ ==========
import arcade

# Сохраняем оригинальные функции
_original_load_texture = arcade.load_texture
_original_load_sound = arcade.load_sound
_original_SpriteSheet = arcade.SpriteSheet
_original_load_tilemap = arcade.load_tilemap


def _resource_path(path):
    """Преобразует путь для PyInstaller"""
    if not path:
        return path

    # Если путь уже абсолютный, возвращаем как есть
    if os.path.isabs(path):
        return path

    # Пробуем найти файл в нескольких местах
    possible_paths = []

    # 1. В _MEIPASS (для PyInstaller)
    if hasattr(sys, '_MEIPASS'):
        possible_paths.append(os.path.join(sys._MEIPASS, path))
        # Также пробуем с нормализованными слешами
        possible_paths.append(os.path.join(sys._MEIPASS, path.replace('/', '\\')))
        possible_paths.append(os.path.join(sys._MEIPASS, path.replace('\\', '/')))

    # 2. В текущей директории (для разработки)
    possible_paths.append(os.path.join(os.getcwd(), path))
    possible_paths.append(os.path.join(os.getcwd(), path.replace('/', '\\')))
    possible_paths.append(os.path.join(os.getcwd(), path.replace('\\', '/')))

    # 3. Относительно этой директории
    possible_paths.append(path)
    possible_paths.append(path.replace('/', '\\'))
    possible_paths.append(path.replace('\\', '/'))

    # 4. В папке с EXE файлом
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        possible_paths.append(os.path.join(exe_dir, path))
        possible_paths.append(os.path.join(exe_dir, path.replace('/', '\\')))
        possible_paths.append(os.path.join(exe_dir, path.replace('\\', '/')))

    # Ищем первый существующий путь
    for possible_path in possible_paths:
        try:
            if os.path.exists(possible_path):
                return possible_path
        except:
            continue

    # Если ничего не нашли, возвращаем исходный путь
    return path


# Функция для логирования
def _log_resource_load(func_name, original_path, fixed_path):
    if original_path != fixed_path:
        pass  # Можно добавить логирование если нужно


# Патчим arcade.load_texture
def patched_load_texture(file_path, *args, **kwargs):
    fixed_path = _resource_path(file_path)
    _log_resource_load('load_texture', file_path, fixed_path)
    return _original_load_texture(fixed_path, *args, **kwargs)


# Патчим arcade.load_sound
def patched_load_sound(file_path, *args, **kwargs):
    fixed_path = _resource_path(file_path)
    _log_resource_load('load_sound', file_path, fixed_path)
    return _original_load_sound(fixed_path, *args, **kwargs)


# Патчим arcade.SpriteSheet
def patched_SpriteSheet(file_path, *args, **kwargs):
    fixed_path = _resource_path(file_path)
    _log_resource_load('SpriteSheet', file_path, fixed_path)
    return _original_SpriteSheet(fixed_path, *args, **kwargs)


# Патчим arcade.load_tilemap
def patched_load_tilemap(file_path, *args, **kwargs):
    fixed_path = _resource_path(file_path)
    _log_resource_load('load_tilemap', file_path, fixed_path)
    return _original_load_tilemap(fixed_path, *args, **kwargs)


# Применяем патчи
arcade.load_texture = patched_load_texture
arcade.load_sound = patched_load_sound
arcade.SpriteSheet = patched_SpriteSheet
arcade.load_tilemap = patched_load_tilemap

# Патчим arcade.Sound если существует
if hasattr(arcade, 'Sound'):
    _original_Sound = arcade.Sound
    arcade.Sound = lambda file_path, *args, **kwargs: _original_Sound(_resource_path(file_path), *args, **kwargs)

# Патчим создание arcade.Sprite для обработки путей
_original_Sprite_init = arcade.Sprite.__init__


def patched_Sprite_init(self, filename=None, scale=1, **kwargs):
    if filename:
        fixed_filename = _resource_path(filename)
        _original_Sprite_init(self, fixed_filename, scale, **kwargs)
    else:
        _original_Sprite_init(self, filename, scale, **kwargs)


arcade.Sprite.__init__ = patched_Sprite_init

# Также патчим другие возможные функции загрузки
try:
    # Патчим arcade.load_font если используется
    if hasattr(arcade, 'load_font'):
        _original_load_font = arcade.load_font
        arcade.load_font = lambda font_path: _original_load_font(_resource_path(font_path))
except:
    pass

print("✅ Патч для PyInstaller активирован")
# ========== КОНЕЦ ПАТЧА ==========

# Теперь можно импортировать остальные модули
import arcade
from StartMenu import Start_menu
from constants import TITLE


def main():
    window = arcade.Window(fullscreen=True, title=TITLE)
    view = Start_menu()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()