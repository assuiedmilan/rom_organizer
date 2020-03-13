import collections
import os
import re
from lxml import etree


class GameListParser(object):
    GAMELIST_FILE = 'gamelist.xml'

    GAME_ID = "id"
    GAME_KEY = "game"
    GENRE_KEY = "genre"

    PATH_KEY = "path"
    ROOT_KEY = "root"
    NAME_KEY = "name"
    NO_TEXT = "Undefined_text"

    game_map = collections.OrderedDict()

    def __init__(self, gamelist_path):
        self.root = gamelist_path
        self.gamelist = os.path.join(gamelist_path, self.GAMELIST_FILE)
        self.parsed_gamelist = None
        self.__parse()

    def get_parsed_games(self):
        return self.game_map

    def reparse(self):
        self.__parse()

    def get_all_games(self):
        return self.parsed_gamelist.findall(self.GAME_KEY)

    def get_game_id(self, game):
        return game.get(self.GAME_ID)

    def get_game_genre(self, game):
        match_any_slashes_or_space = re.compile(r'(?:\s+|\\+|/+)')
        match_any_carret = re.compile(r'-+')

        genre = self.__process_game_child_value(game, self.GENRE_KEY)

        genre = re.sub(match_any_slashes_or_space, '-', genre)
        genre = re.sub(match_any_carret, '-', genre)

        return genre if genre is not self.NO_TEXT else "Unclassified"

    def get_game_path(self, game):
        return self.__process_game_child_value(game, self.PATH_KEY)

    def get_game_name(self, game):
        return self.__process_game_child_value(game, self.NAME_KEY)

    def is_game_valid(self, game):
        return self.get_game_id(game) is not None and self.get_game_id(game) is not "0"

    def __parse(self):
        parser = etree.XMLParser(remove_blank_text=True)
        self.parsed_gamelist = etree.parse(self.gamelist, parser)

        self.__process_all_games()

    def __process_all_games(self):
        for game in self.get_all_games():
            self.__process_game_nodes(game)

    def __process_game_nodes(self, game):
        if self.is_game_valid(game):
            details = {self.GENRE_KEY: self.get_game_genre(game),
                       self.PATH_KEY: self.get_game_path(game),
                       self.ROOT_KEY: self.root}

            self.game_map[self.get_game_name(game)] = details

    def __process_game_child_value(self, game, key):
        game_child = game.find(key)

        if game_child is None or game_child.text is None:
            return self.NO_TEXT
        else:
            return game_child.text

    def __str__(self):
        text_output = []

        for game_id, game in self.game_map.items():
            text_output.append("Game " + game_id + " has properties:")
            for key, value in game.items():
                if value is None:
                    text_output.append("ERROR Undefined value for " + key)
                else:
                    text_output.append(key + ": " + value)
            text_output.append("\n")

        return "\n".join(text_output)
