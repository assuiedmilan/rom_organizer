import lxml.etree
import mock
import pytest

from organizer.parser.game_list_parser import GameListParser
from tests_organizer.common import gamelist
from tests_organizer.common.gamelist import EXPECTED_DATA
from tests_organizer.common.mocks import PARSED_DOCUMENT

GAMELIST_ROOT_VALUES = ['GAMES']

@pytest.fixture(params = GAMELIST_ROOT_VALUES)
def root_values(request):
    yield request.param

@pytest.fixture()
def basic_parser(root_values):
    with mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse') as parser:
        parser.return_value = PARSED_DOCUMENT
        yield GameListParser(root_values)

@pytest.fixture()
def ready_parser(basic_parser):
    with mock.patch('organizer.parser.game_list_parser.GameListParser.validate') as validation:
        with mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse') as parser:
            parser.return_value = PARSED_DOCUMENT
            validation.return_value = True
            basic_parser.parse()
            yield basic_parser

def ready_parser_parameters():
    from _pytest.mark import MarkGenerator
    generator = MarkGenerator()
    parser_fixture = pytest.lazy_fixture('ready_parser')
    roots_fixture = pytest.lazy_fixture('root_values')
    return generator.parametrize('parser, root_value', [(parser_fixture, roots_fixture)] )

def test_validate(basic_parser):
    with pytest.raises(KeyError)  as execution_info:
        basic_parser.validate()
        assert "No game file located at" in str(execution_info.value)

def test_parse_fails_when_game_file_is_missing(basic_parser):
    with pytest.raises(KeyError)  as execution_info:
        basic_parser.parse()
        assert "No game file located at" in str(execution_info.value)

def test_parse_with_validation_passing(ready_parser):
    ready_parser.parse()

@ready_parser_parameters()
def test_get_root(parser, root_value):
    assert (parser.get_root() == root_value)

def test_get_all_games(ready_parser):
    all_games = ready_parser.get_all_games()
    assert (len(all_games) == len(EXPECTED_DATA))

def test_get_game_name(ready_parser):
    all_games = ready_parser.get_all_games()
    games_values = [ready_parser.get_game_name(game) for game in all_games]

    assert (games_values == gamelist.expected_names)

def test_get_game_genre(ready_parser):
    all_games = ready_parser.get_all_games()
    games_values = [ready_parser.get_game_genre(game) for game in all_games]

    assert (games_values == gamelist.expected_genres)

def test_get_game_path(ready_parser):
    all_games = ready_parser.get_all_games()
    games_values = [ready_parser.get_game_path(game) for game in all_games]

    assert (games_values == gamelist.expected_paths)

def test_get_game_node(ready_parser):

    for name in gamelist.expected_files:
        node = ready_parser.get_game_node_from_game_file(name)
        assert(node is not None and isinstance(node, lxml.etree._Element))
