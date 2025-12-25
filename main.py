import time
import arcade
import math
import random
from StartMenu import Start_menu, WIDTH, HEIGHT, TITLE

def main():
    game = Start_menu(WIDTH, HEIGHT, TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
