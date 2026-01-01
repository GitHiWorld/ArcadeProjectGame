import arcade
from StartMenu import Start_menu
from GameWindow import GameWindow
from constants import TITLE

def main():
    window = arcade.Window(fullscreen=True, title=TITLE)
    # view = Start_menu()
    view = GameWindow(123)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()