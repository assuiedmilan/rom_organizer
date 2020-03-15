import os

from organizer.parser.game_list_parser import GameListParser


class Game:

    @staticmethod
    def factory(parsed_games):
        games_list = []

        for game_name, game_details in parsed_games.items():
            games_list.append(
                Game(game_name,
                     game_details.get(GameListParser.GENRE_KEY),
                     game_details.get(GameListParser.PATH_KEY),
                     game_details.get(GameListParser.ROOT_KEY)))

        return games_list

    def __init__(self, name, genre, relative_path, root_path):
        self.name = name
        self.genre = genre
        self.relative_path = relative_path
        self.root_path = root_path

    def get_name(self):
        return self.name

    def get_filename(self):
        return os.path.split(self.get_current_path())[1]

    def get_genre(self):
        return self.genre

    def get_current_path(self):
        return os.path.normpath(os.path.join(self.root_path, self.relative_path))

    def get_root_path(self):
        return self.root_path