import os

from lxml import etree

from organizer.parser.game_list_parser import GameListParser


class GenreAliasesGenerator(object):
    GENRE_ASSOCIATION_FILE = 'genre_associations.xml'
    GENRE_ASSOCIATION_NODE = "genre_associations"
    GENRE_ALIAS_KEY = "alias"

    def __init__(self, gamelist_path, is_single_folder):

        self.document_root = None

        if is_single_folder:
            self.document_path = os.path.join(gamelist_path, self.GENRE_ASSOCIATION_FILE)
        else:
            self.document_path = os.path.join(gamelist_path, '..', self.GENRE_ASSOCIATION_FILE)

        self.game_parser = GameListParser(gamelist_path)
        self.open_document()

    def create_genre_association_entry(self):
        self.__add_genre_association_node()
        self.__process_genre_aliases()
        self.write_document()

    def open_document(self):

        if os.path.isfile(self.document_path):
            parser = etree.XMLParser(remove_blank_text=True)
            self.document_root = etree.parse(self.document_path, parser).getroot()
        else:
            self.document_root = etree.Element('root')

    def write_document(self):
        document = etree.ElementTree(self.document_root)
        document.write(self.document_path, pretty_print=True)

    def _get_genre_alias_from_genre(self, genre):

        genre_alias = None

        genre_association_node = self.__get_game_association_node()

        if genre_association_node is not None:

            for node in genre_association_node.getchildren():
                if node.get(self.game_parser.GENRE_KEY) == genre:
                    genre_alias = node.get(self.GENRE_ALIAS_KEY)
                    break

        return genre_alias

    def __get_game_genre_alias(self, game):
        genre = self.game_parser.get_game_genre(game)
        return self._get_genre_alias_from_genre(genre)

    def __get_game_association_node(self):
        return self.document_root.find(self.GENRE_ASSOCIATION_NODE)

    def __process_genre_aliases(self):

        for game in self.game_parser.get_all_games():
            if self.game_parser.is_game_valid(game):
                self.__add_genre_node(self.game_parser.get_game_genre(game))

        self.__sort_genre_aliases()

    def __sort_genre_aliases(self):
        genre_association_node = self.__get_game_association_node()

        if genre_association_node is not None:
            all_genres = genre_association_node.getchildren()
            all_genres.sort(key=lambda x: x.attrib[self.game_parser.GENRE_KEY].lower())

            genre_association_node[:] = all_genres

    def __genre_alias_already_exists(self, genre):
        return self._get_genre_alias_from_genre(genre) is not None

    def __add_genre_association_node(self):

        genre_association_node = self.__get_game_association_node()

        if genre_association_node is None:

            genre_association_node = etree.Element(self.GENRE_ASSOCIATION_NODE)
            genre_association_node.set("text", "Defines aliases between games genres for folders organization")
            self.document_root.insert(1, genre_association_node)

    def __add_genre_node(self, genre):
        genre_association_node = self.__get_game_association_node()

        if genre_association_node is not None and not self.__genre_alias_already_exists(genre):
            genre_node = etree.Element(self.game_parser.GENRE_KEY)
            genre_node.set(self.game_parser.GENRE_KEY, genre)
            genre_node.set(self.GENRE_ALIAS_KEY, genre)

            genre_association_node.append(genre_node)