import os
import argparse

from organizer.games.game import Game
from organizer.games.game_organizer import GameOrganizer
from organizer.parser.game_list_parser import GameListParser
from organizer.parser.genre_aliases_generator import GenreAliasesGenerator


class MainParser:

    def __init__(self):
        arguments = self.__parse_arguments()

        self.folders = []

        self.find_folders(arguments.root_folder)
        self.is_rom_folder = 1 == len(self.folders)
        self.generate_genres = arguments.generate_genres.lower() == 'true'

    def find_folders(self, from_root):

        self.folders = []

        for root, dirs, names in os.walk(from_root):
            if GameListParser.GAMELIST_FILE in names:
                self.folders.append(root)

    def execute(self):
        if not self.generate_genres:
            self.__process_parsing()
        else:
            self.__process_genres()

    def __process_genres(self):
        for folder in self.folders:
            try:
                parser = GenreAliasesGenerator(folder, self.is_rom_folder)
                parser.create_genre_association_entry()
            except Exception as something_happened:
                print(something_happened)
            finally:
                pass

    def __process_parsing(self):
        for folder in self.folders:
            self.__parse_folder(folder)

    @staticmethod
    def __parse_arguments():
        argument_parser = argparse.ArgumentParser(description='Process roms organizer options')
        argument_parser.add_argument('root_folder', help="Folder in which the parser will start looking for gamelist.xml files")
        argument_parser.add_argument('--generate_genres', dest='generate_genres', default=False, help='If set to true, no sorting will occur, but genre associations will be created')

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
