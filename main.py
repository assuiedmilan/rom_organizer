import os
import argparse

from organizer.games.game import Game
from organizer.games.game_organizer import GameOrganizer
from organizer.parser.game_list_parser import GameListParser

class MainParser:

    def __init__(self):
        arguments = self.__parse_arguments()

        self.root_folder = arguments.root_folder
        self.is_rom_folder = arguments.is_rom_folder.lower() == 'true'

    def execute(self):
        if self.is_rom_folder:
            self.__parse_folder(self.root_folder)
        else:
            list_of_folders_to_parse = [f.path for f in os.scandir(self.root_folder) if f.is_dir()]

            for folder in list_of_folders_to_parse:
                self.__parse_folder(folder)

    @staticmethod
    def __parse_arguments():
        argument_parser = argparse.ArgumentParser(description='Process roms organizer options')
        argument_parser.add_argument('root_folder', help="Folder in which the parser will start looking for gamelist.xml files")
        argument_parser.add_argument('--is_rom_folder', dest='is_rom_folder', default=True, help='If set to false, the parser will look into each subfolder of the root folder for gamelist.xml. Each subfolder will be considered as an independent gaming platform')

        return argument_parser.parse_args()

    @staticmethod
    def __parse_folder(folder):
        try:
            parser = GameListParser(folder)
            game_list = Game.factory(parser.get_parsed_games())

            game_organizer = GameOrganizer()
            game_organizer.move_game_files(game_list)
        except Exception as something_happened:
            print(something_happened)
        finally:
            pass

if __name__ == "__main__":

    main_parser = MainParser()
    main_parser.execute()


