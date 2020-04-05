import mock

from organizer.tools.xml_files_operations import XmlFilesOperations

FILE_NAME = "toto.xml"

@mock.patch('organizer.tools.xml_files_operations.etree.ElementTree')
def test_write(mock_document):

    XmlFilesOperations.write(mock_document, FILE_NAME)
    mock_document.write.assert_called()

@mock.patch('organizer.tools.xml_files_operations.etree')
def test_parse(mock_xml):

    XmlFilesOperations.parse(FILE_NAME)
    mock_xml.parse.assert_called()

