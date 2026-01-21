@echo off
chcp 65001 > nul
echo ===============================================
echo    СБОРКА ARCADEGAME С ИСПРАВЛЕНИЕМ VERSION
echo ===============================================

echo Удаляем старые сборки...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo.
echo Создаем временный VERSION файл...
echo 2.6.17 > _temp_version.txt

echo.
echo Запускаем сборку...

pyinstaller --onefile ^
  --name "ArcadeGame" ^
  --clean ^
  --noconfirm ^
  --windowed ^
  --add-data "fonts;fonts" ^
  --add-data "images;backgrounds" ^
  --add-data "sounds;sounds" ^
  --add-data "game_settings.json;." ^
  --add-data "_temp_version.txt;arcade/VERSION" ^
  --add-data "*.py;." ^
  --hidden-import arcade ^
  --hidden-import pygame ^
  --hidden-import pygame._view ^
  --hidden-import pygame.mixer ^
  --hidden-import pygame.mixer.music ^
  --hidden-import importlib.metadata ^
  --hidden-import importlib.resources ^
  main.py

echo.
echo Удаляем временные файлы...
del _temp_version.txt 2>nul

echo.
echo ===============================================
echo    СБОРКА ЗАВЕРШЕНА!
echo    Запустите файл: dist\ArcadeGame.exe
echo ===============================================
echo.
pause