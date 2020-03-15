import os
import argparse

from organizer.games.game import Game
from organizer.games.game_organizer import GameOrganizer
from organizer.parser.game_list_parser import GameListParser
from organizer.parser.game_sorting_map_generator import GameSortingMapGenerator
from organizer.parser.genre_aliases_generator import GenreAliasesGenerator
from organizer.tools.exception_tools import ExceptionPrinter


class MainParser(object):

    @staticmethod
    def __clean(folder):
        for root, dirs, names in os.walk(folder):
            for directory in dirs:
                to_delete = os.path.join(root, directory)
                if 0 == len(os.listdir(to_delete)):
                    os.rmdir(to_delete)

    @staticmethod
    def __parse_arguments():
        argument_parser = argparse.ArgumentParser(description='Process roms organizer options')

        argument_parser.add_argument('root_folder',
                                     help="Folder in which the parser will start looking for gamelist.xml files"
                                     )

        argument_parser.add_argument('--generate_genres',
                                     dest='generate_genres',
                                     type=bool,
                                     default=False,
                                     help='If set to true, no sorting will occur, but genre associations will be created'
                                     )

        argument_parser.add_argument('--aliases_priority_list',
                                     dest='aliases_priority_list',
                                     type=str,
                                     default="",
                                     help='If filled, genre will be replaced by an alias in the order they appear on this list during genres generation.'
                                          ' Example: "platform,action" will transform action-platform into platform and action-strategy into action')

        return argument_parser.parse_args()


    def __init__(self):
        arguments = self.__parse_arguments()

        self.folders = []

        self.find_folders(arguments.root_folder)
        self.argument_folder_is_single_rom_folder = 1 == len(self.folders)
        self.generate_genres = arguments.generate_genres
        self.aliases_priority_list = [str(item) for item in arguments.aliases_priority_list.split(',')]

    def find_folders(self, from_root):

        self.folders = []

        for root, dirs, names in os.walk(from_root):
            if GameListParser.GAMELIST_FILE in names:
                self.folders.append(root)

    def execute(self):
        if not self.generate_genres:
            self.__process_sorting()
        else:
            self.__process_genres()

    def __process_genres(self):
        for folder in self.folders:
            self.__process_genres_for_folder(folder)

    def __process_sorting(self):
        for folder in self.folders:
            self.__process_sorting_for_folder(folder)
            self.__clean(folder)

    def __process_genres_for_folder(self, folder):

        try:

            parser = GenreAliasesGenerator(folder, self.argument_folder_is_single_rom_folder,
                                           self.aliases_priority_list)
            parser.create_genre_association_entry()

        except Exception as something_happened:
            ExceptionPrinter.print_exception(something_happened)

        finally:
            pass

    def __process_sorting_for_folder(self, folder):

        try:

            game_sorter = GameSortingMapGenerator(folder, self.argument_folder_is_single_rom_folder)
            game_list = Game.factory(game_sorter.get_parsed_games())

            GameOrganizer.move_game_files(game_list, folder)

        except Exception as something_happened:
            ExceptionPrinter.print_exception(something_happened)

        finally:
            pass

