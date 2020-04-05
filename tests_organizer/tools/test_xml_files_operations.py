import mock
import pytest

from organizer.tools.xml_files_operations import XmlFilesOperations

FILE_NAME = "toto.xml"

@pytest.fixture()
def mock_parser():
    parser = mock.patch('organizer.tools.xml_files_operations.etree.XMLParser').start()
    with mock.patch('organizer.tools.xml_files_operations.etree.XMLParser', return_value=parser):
        yield parser

    parser.stop()

@mock.patch('organizer.tools.xml_files_operations.etree.ElementTree')
def test_write(mock_document):

    XmlFilesOperations.write(mock_document, FILE_NAME)
    mock_document.write.assert_called_with(FILE_NAME, pretty_print=True)

@mock.patch('organizer.tools.xml_files_operations.etree')
def test_parse(mock_xml, mock_parser):

    XmlFilesOperations.parse(FILE_NAME)
    mock_xml.parse.assert_called_with(FILE_NAME, mock_parser)

