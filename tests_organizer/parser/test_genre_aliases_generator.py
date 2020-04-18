from lxml import etree

import mock
import pytest

from organizer.parser.genre_aliases_generator import GenreAliasesGenerator
from tests_organizer.common import genre_associations
from tests_organizer.common.fixtures import root_values

PARSED_DOCUMENT = etree.fromstring(genre_associations.XML_DOCUMENT)
IS_SINGLE_FOLDER = [True, False]
REPLACEMENT_LIST = [None, ['Action', 'Platform'], ['Platform', 'Action']]

@pytest.fixture(params = IS_SINGLE_FOLDER)
def single_folder(request):
    yield request.param

@pytest.fixture(params = REPLACEMENT_LIST)
def replacement_list(request):
    yield request.param

@pytest.fixture()
def generator(root_values, single_folder, replacement_list):
    yield GenreAliasesGenerator(root_values, single_folder, replacement_list)

@pytest.fixture()
def ready_generator(generator):
    with mock.patch('os.path.isfile') as is_file:
        with mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse') as parser:
            parser.return_value = PARSED_DOCUMENT
            is_file.return_value = True
            yield generator

@pytest.mark.parametrize('generator_parameter', [
    pytest.lazy_fixture('ready_generator'),
    pytest.param(pytest.lazy_fixture('generator'), marks=pytest.mark.xfail(reason="Document does not exists", strict=True))
])
def test_document_exist(generator_parameter):
    assert generator_parameter.document_exists()
