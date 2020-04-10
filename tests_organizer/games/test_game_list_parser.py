import mock
import pytest

# noinspection PyUnresolvedReferences
from tests_organizer.common.test_fixtures import basic_parser
from tests_organizer.common import tests_mocks

@mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse', tests_mocks.mocked_parser)
def test_validate(basic_parser):
    with pytest.raises(KeyError)  as execution_info:
        basic_parser.validate()
        assert "No game file located at" in str(execution_info.value)

@mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse', tests_mocks.mocked_parser)
def test_parse_fails_when_game_file_is_missing(basic_parser):

    with pytest.raises(KeyError)  as execution_info:
        basic_parser.parse()
        assert "No game file located at" in str(execution_info.value)

@mock.patch('organizer.parser.game_list_parser.GameListParser.validate', tests_mocks.mocked_validation)
@mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse', tests_mocks.mocked_parser)
def test_parse_with_validation_passing(basic_parser):
    basic_parser.parse()