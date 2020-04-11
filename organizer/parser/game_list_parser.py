import os
import re

from organizer.tools.xml_files_operations import XmlFilesOperations


class GameListParser(object):

    GAMELIST_FILE = 'gamelist.xml'

    GAME_ID = "id"
    GAME_KEY = "game"
    GENRE_KEY = "genre"

    PATH_KEY = "path"
    ROOT_KEY = "root"
    NAME_KEY = "name"
    NO_TEXT = "Undefined_text"
    NO_GENRE = "Unclassified"

    __EXCLUDE_FOLDERS = ['media']

    def __init__(self, gamelist_path):
        self.root = gamelist_path
        self.gamelist = os.path.join(gamelist_path, self.GAMELIST_FILE)
        self.parsed_gamelist = None
        self.files_to_parse = []

    def parse(self):
        self.parsed_gamelist = XmlFilesOperations.parse(self.gamelist)
        self.validate()

    def write_document(self):
        self.validate()
        XmlFilesOperations.write(self.parsed_gamelist, self.gamelist)

    def validate(self):
        for game in self.get_all_games():
            game_path = os.path.join(self.root, self.get_game_path(game))

            if not os.path.isfile(game_path):
                raise KeyError("No game file located at %s", game_path)

    def get_root(self):
        return self.root

    def get_all_files(self):
        if not self.files_to_parse:
            self.__process_all_files_to_parse()

        return self.files_to_parse

    def get_all_games(self):
        if self.parsed_gamelist is None:
            self.parse()

        return self.parsed_gamelist.findall(self.GAME_KEY)

    def get_game_genre(self, game):
        match_any_slashes_or_space = re.compile(r'(?:\s+|\\+|/+)')
        match_any_carret = re.compile(r'-+')

        genre = self.__process_game_child_value(game, self.GENRE_KEY)

        genre = re.sub(match_any_slashes_or_space, '-', genre)
        genre = re.sub(match_any_carret, '-', genre)

        return genre if genre is not self.NO_TEXT else self.NO_GENRE

    def get_game_path(self, game):
        return self.__process_game_child_value(game, self.PATH_KEY)

    def get_game_name(self, game):
        return self.__process_game_child_value(game, self.NAME_KEY)

    def get_game_node_from_game_file(self, name):

        game_node = None

        for game in self.get_all_games():
            path = self.get_game_path(game)
            _, file_name = os.path.split(path)

            if file_name == name:
                game_node = game

        return game_node

    def __process_all_files_to_parse(self):

        self.files_to_parse = []

        for root, dirs, names in os.walk(self.root):

            path_contains_excluded_folder = any(value in root for value in self.__EXCLUDE_FOLDERS)

            if not path_contains_excluded_folder:

                for name in names:
                    self.files_to_parse.append(name)

    def __process_game_child_value(self, game, key):
        game_child = game.find(key)

        if game_child is None or game_child.text is None:
            return self.NO_TEXT
        else:
            return game_child.text
