import os

import pytest

from organizer.games.game import Game

GENRE = 'Action'
SUBFOLDER = 'toto'
FILENAME = 'tata.zip'
REL_PATH = os.path.join(SUBFOLDER, FILENAME)
ROOT = os.path.join('home', 'pi', 'roms')

@pytest.fixture(
    params=[
        pytest.param({'values': {'genre': 'Action', 'root': os.path.join('home', 'pi', 'roms'), 'subfolder': 'toto', 'filename': 'tata.zip'}, 'expected': {'genre': 'Action', 'root': os.path.join('home', 'pi', 'roms'), 'path': os.path.join('home', 'pi', 'roms', 'toto', 'tata.zip'), 'filename': 'tata.zip'}}),
        pytest.param({'values': {'genre': 'Action', 'root': os.path.join('home', 'pi', 'roms'), 'subfolder': 'toto', 'filename': 'tata.zip'}, 'expected': {'genre': 'Strategy', 'root': os.path.join('home', 'pi', 'roms'), 'path': os.path.join('home', 'pi', 'roms', 'tutu', 'tata.zip'), 'filename': 'titi.zip'}}, marks=pytest.mark.xfail)
    ]
)
def game(request):
    values = request.param.get('values')
    expected = request.param.get('expected')
    return Game(values.get('genre'), os.path.join(values.get('subfolder'), values.get('filename')), values.get('root')), expected

def test_factory():
    game_details = [
        {'genre': 'Action', 'path': REL_PATH, 'root': ROOT},
        {'genre': 'Strategy', 'path': REL_PATH, 'root': ROOT},
        {'genre': 'Platform', 'path': REL_PATH, 'root': ROOT}
    ]

    games_list = Game.factory(game_details)

    assert len(games_list) == len(game_details)

    for item in games_list:
        assert isinstance(item, Game)

@pytest.mark.parametrize('test_input', [pytest.lazy_fixture('game')])
def test_get_genre(test_input):
    game, expected = test_input
    assert game.get_genre() == expected.get('genre')

@pytest.mark.parametrize('test_input', [pytest.lazy_fixture('game')])
def test_get_root_path(test_input):
    game, expected = test_input
    assert game.get_genre() == expected.get('root')

@pytest.mark.parametrize('test_input', [pytest.lazy_fixture('game')])
def test_get_current_path(test_input):
    game, expected = test_input
    assert game.get_genre() == expected.get('path')

@pytest.mark.parametrize('test_input', [pytest.lazy_fixture('game')])
def test_get_filename(test_input):
    game, expected = test_input
    assert game.get_genre() == expected.get('filename')







