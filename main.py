import arcade
from StartMenu import Start_menu
from constants import TITLE

def main():
    window = arcade.Window(fullscreen=True, title=TITLE)
    start_menu = Start_menu()
    window.show_view(start_menu)
    arcade.run()

if __name__ == "__main__":
    main()