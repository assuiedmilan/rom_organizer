import os
import shutil

from organizer.tools.exception_tools import ExceptionPrinter


class GameOrganizer:

    def __init__(self, game):
        self.game = game

    @classmethod
    def move_game_files(cls, list_of_games):

        for game in list_of_games:
            organizer = GameOrganizer(game)

            organizer.__move_game_file()


    def __move_game_file(self):

        current_path, target_root, target_path = self.get_paths()

        if current_path is not target_path and os.path.isfile(current_path):

            try:

                if not os.path.isdir(target_root): os.makedirs(target_root)
                shutil.move(current_path, target_path)

            except Exception as something_happened:
                ExceptionPrinter.print_exception(something_happened)

    def get_paths(self):
        current_path = self.game.get_current_path()
        file_name = os.path.basename(os.path.normpath(current_path))
        target_root = os.path.normpath(os.path.join(self.game.get_root_path(), self.game.get_genre()))
        target_path = os.path.normpath(os.path.join(target_root, file_name))

        return current_path, target_root, target_path

    def compute_new_game_location(self):

        current_path, _, target_path = self.get_paths()

        original_folder = os.path.split(current_path)[0]
        relative_path = os.path.relpath(target_path, original_folder)
        unix_relative_path = './' + relative_path.replace(os.path.sep, '/')

        return os.path.normpath(os.path.join(original_folder, unix_relative_path))




