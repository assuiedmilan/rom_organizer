import os
import re
import traceback

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

    def __init__(self, gamelist_path):
        self.root = gamelist_path
        self.gamelist = os.path.join(gamelist_path, self.GAMELIST_FILE)
        self.parsed_gamelist = None
        self.files_to_parse = []
        self.__process_all_files_to_parse()

        print("In root " + self.root)
        print(self.files_to_parse)
        print("\n\n\n")
        #self.__parse()

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

    def __process_all_files_to_parse(self):
        for root, dirs, names in os.walk(self.root):
            for name in names:
                self.files_to_parse.append(name)

    # noinspection PyBroadException
    def __parse(self):
        parser = etree.XMLParser(remove_blank_text=True)

        try:
            self.parsed_gamelist = etree.parse(self.gamelist, parser)
        except Exception as e:
            print("Error parsing " + self.gamelist)
            print(e.message)
            traceback.print_exc()
            raise e

    def __process_game_child_value(self, game, key):
        game_child = game.find(key)

        if game_child is None or game_child.text is None:
            return self.NO_TEXT
        else:
            return game_child.text
