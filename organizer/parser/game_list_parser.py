import collections
import os
import re
from lxml import etree


class GameListParser:
    GAMELIST_FILE = 'gamelist.xml'

    GENRE_ASSOCIATION_NODE = "genre_associations"

    GAME_ID = "id"
    GAME_KEY = "game"
    GENRE_KEY = "genre"
    GENRE_ALIAS_KEY = "alias"
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

    def create_genre_association_entry(self):

        genre_association_node = self.__get_game_association_node()

        if genre_association_node is None:

            genre_association_node = etree.Element(self.GENRE_ASSOCIATION_NODE)
            genre_association_node.set("text", "Defines aliases between games genres for folders organization")
            self.parsed_gamelist.getroot().insert(1, genre_association_node)

        self.__process_genre_aliases()

        self.parsed_gamelist.write(self.gamelist, pretty_print=True)

    def __parse(self):
        parser = etree.XMLParser(remove_blank_text=True)
        self.parsed_gamelist = etree.parse(self.gamelist, parser)

        self.__process_all_games()

    def __get_all_games(self):
        return self.parsed_gamelist.findall(self.GAME_KEY)

    def __get_game_id(self, game):
        return game.get(self.GAME_ID)

    def __game_is_valid(self, game):
        return self.__get_game_id(game) is not None and self.__get_game_id(game) is not "0"

    def __get_game_genre(self, game):
        match_any_slashes_or_space = re.compile(r'(?:\s+|\\+|/+)')
        match_any_carret = re.compile(r'-+')

        genre = self.__process_game_child_value(game, self.GENRE_KEY)

        genre = re.sub(match_any_slashes_or_space, '-', genre)
        genre = re.sub(match_any_carret, '-', genre)

        return genre if genre is not self.NO_TEXT else "Unclassified"

    def __get_game_path(self, game):
        return self.__process_game_child_value(game, self.PATH_KEY)

    def __get_game_name(self, game):
        return self.__process_game_child_value(game, self.NAME_KEY)

    def __get_game_association_node(self):
        return self.parsed_gamelist.find(self.GENRE_ASSOCIATION_NODE)

    def __process_all_games(self):
        for game in self.__get_all_games():
            self.__process_game_nodes(game)

    def __process_game_nodes(self, game):
        if self.__game_is_valid(game):
            details = {self.GENRE_KEY: self.__get_game_genre(game),
                       self.PATH_KEY: self.__get_game_path(game),
                       self.ROOT_KEY: self.root}

            self.game_map[self.__get_game_name(game)] = details

    def __process_game_child_value(self, game, key):
        game_child = game.find(key)

        if game_child is None or game_child.text is None:
            return self.NO_TEXT
        else:
            return game_child.text

    def __process_genre_aliases(self):

        for game in self.__get_all_games():
            if self.__game_is_valid(game):
                self.__add_genre_node(self.__get_game_genre(game))

        self.__sort_genre_aliases()

    def __sort_genre_aliases(self):
        genre_association_node = self.__get_game_association_node()

        if genre_association_node is not None:
            all_genres = genre_association_node.getchildren()
            all_genres.sort(key=lambda x: x.attrib[self.GENRE_KEY].lower())

            genre_association_node[:] = all_genres

    def __genre_alias_already_exists(self, genre):

        genre_alias_already_exist = False
        genre_association_node = self.__get_game_association_node()

        if genre_association_node is not None:

            for node in genre_association_node.getchildren():
                if node.get(self.GENRE_KEY) == genre:
                    genre_alias_already_exist = True
                    break

        return genre_alias_already_exist

    def __add_genre_node(self, genre):
        genre_association_node = self.__get_game_association_node()

        if genre_association_node is not None and not self.__genre_alias_already_exists(genre):
            genre_node = etree.Element(self.GENRE_KEY)
            genre_node.set(self.GENRE_KEY, genre)
            genre_node.set(self.GENRE_ALIAS_KEY, genre)

            genre_association_node.append(genre_node)

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



