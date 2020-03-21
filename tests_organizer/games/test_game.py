import os

import pytest

from organizer.games.game import Game

GENRE = 'Action'
SUBFOLDER = 'toto'
FILENAME = 'tata.zip'
REL_PATH = os.path.join(SUBFOLDER, FILENAME)
ROOT = os.path.join('home', 'pi', 'roms')

@pytest.fixture
def game():
    return Game(GENRE, REL_PATH, ROOT)

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


def test_get_filename(game):
    assert game.get_filename() == FILENAME


def test_get_genre(game):
    assert game.get_genre() == GENRE

def test_get_current_path(game):
    game = Game(GENRE, REL_PATH, ROOT)
    assert game.get_current_path() == os.path.join(ROOT, REL_PATH)

def test_get_root_path(game):
    assert game.get_root_path() == ROOT