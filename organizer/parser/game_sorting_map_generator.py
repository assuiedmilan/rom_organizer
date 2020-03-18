import collections

from organizer.parser.game_list_parser import GameListParser
from organizer.parser.genre_aliases_generator import GenreAliasesGenerator


class GameSortingMapGenerator(object):

    def __init__(self, gamelist_path, is_single_folder):
        self.gamelist_path = gamelist_path
        self.game_parser = GameListParser(gamelist_path)
        self.genre_aliases_generator = GenreAliasesGenerator(gamelist_path, is_single_folder)
        self.game_map = collections.OrderedDict()

    def get_parsed_games(self):
        if 0 == len(self.game_map.items()):
            self.process_game_map()

        return self.game_map

    def process_game_map(self):

        print("Processing game map for " + self.gamelist_path)
        for file_name in self.game_parser.get_all_files():

            game = self.game_parser.get_game_node_from_game_file(file_name)

            if game is not None:
                self.__process_games_details(game)

        print("Done processing game map for " + self.gamelist_path)

    def __process_games_details(self, game):

        details = {self.game_parser.GENRE_KEY: self.__compute_game_genre(game),
                   self.game_parser.PATH_KEY: self.game_parser.get_game_path(game),
                   self.game_parser.ROOT_KEY: self.gamelist_path}

        self.game_map[self.game_parser.get_game_name(game)] = details

    def __compute_game_genre(self, game):

        if self.genre_aliases_generator.document_exists():
            return self.genre_aliases_generator.get_game_genre_alias(game)

        return self.game_parser.get_game_genre(game)
