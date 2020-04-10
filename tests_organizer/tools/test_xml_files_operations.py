import mock

from organizer.tools.xml_files_operations import XmlFilesOperations

FILE_NAME = "toto.xml"

@mock.patch('organizer.tools.xml_files_operations.etree.ElementTree')
def test_write(mock_document):

    XmlFilesOperations.write(mock_document, FILE_NAME)
    mock_document.write.assert_called_with(FILE_NAME, pretty_print=True)

@mock.patch('organizer.tools.xml_files_operations.etree.XMLParser')
@mock.patch('organizer.tools.xml_files_operations.etree')
def test_parse(mock_etree, mock_xml_parser):

    XmlFilesOperations.parse(FILE_NAME)
    mock_etree.parse.assert_called_with(FILE_NAME, mock_xml_parser())

