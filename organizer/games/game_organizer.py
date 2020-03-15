import os
import shutil

from organizer.parser.game_list_parser import GameListParser
from organizer.tools.exception_tools import ExceptionPrinter


class GameOrganizer:

    @staticmethod
    def move_game_files(list_of_games, gamelist_folder):

        parser = GameListParser(gamelist_folder)
        parser.parse()

        for game in list_of_games:
            organizer = GameOrganizer(game)
            organizer.register_parser(parser)
            organizer.__move_game_file()
            organizer.__update_game_node()

        parser.write_document()

    def register_parser(self, parser):
        self.parser = parser

    def __init__(self, game):
        self.game = game
        self.parser = None

    def get_game_node(self):
        if self.parser is not None:
            game_name = self.game.get_filename()
            return self.parser.get_game_node_from_game_file(game_name)

        return None

    def __update_game_node(self):
        node = self.get_game_node()
        node.find(GameListParser.PATH_KEY).text = self.__compute_new_game_location()

    def __move_game_file(self):

        current_path, target_root, target_path = self.__get_paths()

        if current_path is not target_path and os.path.isfile(current_path):

            try:

                if not os.path.isdir(target_root): os.makedirs(target_root)
                shutil.move(current_path, target_path)

            except Exception as something_happened:
                ExceptionPrinter.print_exception(something_happened)

    def __get_paths(self):
        current_path = self.game.get_current_path()
        file_name = os.path.basename(os.path.normpath(current_path))

        target_root = os.path.normpath(os.path.join(self.game.get_root_path(), self.game.get_genre()))
        target_path = os.path.normpath(os.path.join(target_root, file_name))

        return current_path, target_root, target_path

    def __compute_new_game_location(self):

        unix_relative_path = []

        if self.parser is not None:

            _, _, target_path = self.__get_paths()

            root = self.parser.get_root()

            relative_path = os.path.relpath(target_path, root)
            unix_relative_path = './' + relative_path.replace(os.path.sep, '/')

        return unix_relative_path




