import os

import mock
import pytest
from lxml import etree

from organizer.parser.game_list_parser import GameListParser
from tests_organizer.common import gamelist

PARSED_DOCUMENT = etree.fromstring(gamelist.XML_DOCUMENT)
GAMELIST_ROOT_VALUES = [os.path.join('home', 'pi', 'roms'), 'GAMES', os.path.join(os.getcwd(), 'home', 'pi', 'roms')]

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