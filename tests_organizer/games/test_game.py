import os
import pytest

from organizer.games.game import Game

ROOT_PATH = os.path.join('home', 'pi', 'roms')

GENRE = 'genre'
ROOT = 'root'
PATH = 'path'
SUBFOLDER = 'subfolder'
FILENAME = 'filename'

VALID_SUBFOLDER = 'toto'
VALID_GENRE = 'Action'
VALID_FILENAME = 'tata.zip'

TEST_PARAMETERS = [
    pytest.param( pytest.lazy_fixture('game'), pytest.lazy_fixture('valid_expected')),
    pytest.param( pytest.lazy_fixture('game'), pytest.lazy_fixture('invalid_expected'), marks=pytest.mark.xfail )
]

@pytest.fixture( params= [{GENRE: VALID_GENRE, ROOT: ROOT_PATH, SUBFOLDER: VALID_SUBFOLDER, FILENAME: VALID_FILENAME}] )
def game(request):
    values = request.param
    return Game(values.get(GENRE), os.path.join(values.get(SUBFOLDER), values.get(FILENAME)), values.get(ROOT))

@pytest.fixture( params= [{GENRE: VALID_GENRE, ROOT: ROOT_PATH, PATH: os.path.join(ROOT_PATH, VALID_SUBFOLDER, VALID_FILENAME), FILENAME: VALID_FILENAME}] )
def valid_expected(request):
    return request.param

@pytest.fixture( params= [{GENRE: 'Strategy', ROOT: ROOT_PATH, PATH: os.path.join(ROOT_PATH, 'tutu', VALID_FILENAME), FILENAME: 'titi.zip'}] )
def invalid_expected(request):
    return request.param

def game_test_parameters():
    from _pytest.mark import MarkGenerator
    generator = MarkGenerator()
    return generator.parametrize('test_input, expected', TEST_PARAMETERS)

@game_test_parameters()
def test_get_genre(test_input, expected):
    assert test_input.get_genre() == expected.get(GENRE)

@game_test_parameters()
def test_get_root_path(test_input, expected):
    assert test_input.get_root_path() == expected.get(ROOT)

@game_test_parameters()
def test_get_current_path(test_input, expected):
    assert test_input.get_current_path() == expected.get(PATH)

@game_test_parameters()
def test_get_filename(test_input, expected):
    assert test_input.get_filename() == expected.get(FILENAME)

def test_factory():
    game_details = [
        {'genre': 'Action', 'path': 'toto\tata.zip', 'root': ROOT_PATH},
        {'genre': 'Strategy', 'path': 'toto\tata.zip', 'root': ROOT_PATH},
        {'genre': 'Platform', 'path': 'toto\tata.zip', 'root': ROOT_PATH}
    ]

    games_list = Game.factory(game_details)

    assert len(games_list) == len(game_details)

    for item in games_list:
        assert isinstance(item, Game)