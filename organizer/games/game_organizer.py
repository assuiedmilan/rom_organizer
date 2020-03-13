import os
import shutil


class GameOrganizer:

    def __init__(self):
        pass

    def move_game_files(self, list_of_games):

        for game in list_of_games:
            self.__move_game_file(game)

    @staticmethod
    def __move_game_file(game):

        current_path = game.get_current_path()
        file_name = os.path.basename(os.path.normpath(current_path))
        target_root = os.path.normpath(os.path.join(game.get_root_path(), game.get_genre()))
        target_path = os.path.normpath(os.path.join(target_root, file_name))

        if current_path is not target_path and os.path.isfile(current_path):

            try:
                if not os.path.isdir(target_root): os.makedirs(target_root)
                shutil.move(current_path, target_path)
            except Exception as something_happened:
                print("Failed to move file\n  from " + current_path + "\n  to " + target_path)
                print(something_happened)



