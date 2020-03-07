import os
import sys

from organizer.games.game import Game
from organizer.games.game_organizer import GameOrganizer
from organizer.parser.game_list_parser import GameListParser

if __name__ == "__main__":

    root = sys.argv[1]

    list_of_folders_to_parse = [f.path for f in os.scandir(root) if f.is_dir()]

    for folder in list_of_folders_to_parse:

        try:
            parser = GameListParser(folder)
            game_list = Game.factory(parser.get_parsed_games())

            game_organizer = GameOrganizer()
            game_organizer.move_game_files(game_list)
        except Exception as something_happened:
            print(something_happened)
        finally:
            pass
