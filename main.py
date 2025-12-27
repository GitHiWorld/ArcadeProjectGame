import time
import arcade
import math
import random
from StartMenu import Start_menu
from constants import WIDTH, HEIGHT, TITLE

def main():
    # game = Start_menu(WIDTH, HEIGHT, TITLE)
    window = arcade.Window(fullscreen=True, title=TITLE)
    view = Start_menu()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
