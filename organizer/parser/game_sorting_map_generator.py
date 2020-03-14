import collections

from organizer.parser.game_list_parser import GameListParser
from organizer.parser.genre_aliases_generator import GenreAliasesGenerator


class GameSortingMapGenerator(object):

    def __init__(self, gamelist_path, is_single_folder):
        self.gamelist_path = gamelist_path
        self.game_parser = GameListParser(gamelist_path)
        self.genre_aliases_generator = GenreAliasesGenerator(gamelist_path, is_single_folder)
        self.game_map = collections.OrderedDict()

        #self.__process_game_map()

    def get_parsed_games(self):
        return self.game_map

    def __process_game_map(self):

        for game in self.game_parser.get_all_games():
            self.__process_games_details(game)

    def __process_games_details(self, game):

        if self.game_parser.is_game_valid(game):
            details = {self.game_parser.GENRE_KEY: self.__compute_game_genre(game),
                       self.game_parser.PATH_KEY: self.game_parser.get_game_path(game),
                       self.game_parser.ROOT_KEY: self.gamelist_path}

            self.game_map[self.game_parser.get_game_name(game)] = details

    def __compute_game_genre(self, game):

        if self.genre_aliases_generator.document_exists():
            return self.genre_aliases_generator.get_game_genre_alias(game)

        return self.game_parser.get_game_genre(game)
