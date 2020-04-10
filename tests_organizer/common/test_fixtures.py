import pytest

from organizer.parser.game_list_parser import GameListParser


@pytest.fixture()
def basic_parser():
    return GameListParser('')