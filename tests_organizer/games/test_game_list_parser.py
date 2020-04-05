import mock
import pytest
from lxml import etree

from organizer.parser.game_list_parser import GameListParser

XML_DOCUMENT = """<?xml version="1.0"?>
<gameList>
    <provider>
        <System>psx</System>
        <software>Skraper</software>
        <database>ScreenScraper.fr</database>
        <web>http://www.screenscraper.fr</web>
    </provider>
    <game id="19562" source="ScreenScraper.fr">
        <path>./Akuji the Heartless.pbp</path>
        <name>Akuji The Heartless</name>
        <desc>The premise of Akuji the Heartless is not a happy one. Just as Akuji, a voodoo shaman, was about to get married, his bride-to-be was kidnapped and he was then killed by his very own brother. His seemingly loving sibling then ripped out his heart and sent Akuji to a dark and evil underworld. Akuji swore revenge on his brother and promised to avenge his true love.     As Akuji, you must collect the souls of your departed ancestors and give them to Baron Samedi, watcher of the underworld. If you are successful, he will grant your wish of revenge by giving you the opportunity to face your brother and do unto him as he did to you. More importantly, you will be together with your fiancee once again.    </desc>
        <rating>0.7</rating>
        <releasedate>19980624T000000</releasedate>
        <developer>Crystal Dynamics</developer>
        <publisher>Eidos Interactive</publisher>
        <genre>Platform-Action / Adventure-Action</genre>
        <players>1</players>
        <image>./media/images/Akuji the Heartless.png</image>
        <thumbnail>./media/box3d/Akuji the Heartless.png</thumbnail>
    </game>
</gameList>
"""

PARSED_DOCUMENT = etree.fromstring(XML_DOCUMENT)

mocked_parser = mock.Mock()
mocked_parser.return_value = PARSED_DOCUMENT

mocked_validation = mock.Mock()
mocked_validation.return_value = True

@pytest.fixture()
def basic_parser():
    return GameListParser('')

@mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse', mocked_parser)
def test_validate(basic_parser):
    with pytest.raises(KeyError)  as execution_info:
        basic_parser.validate()
        assert "No game file located at" in str(execution_info.value)

@mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse', mocked_parser)
def test_parse_fails_when_game_file_is_missing(basic_parser):

    with pytest.raises(KeyError)  as execution_info:
        basic_parser.parse()
        assert "No game file located at" in str(execution_info.value)

@mock.patch('organizer.parser.game_list_parser.GameListParser.validate', mocked_validation)
@mock.patch('organizer.tools.xml_files_operations.XmlFilesOperations.parse', mocked_parser)
def test_parse_with_validation_passing(basic_parser):
    basic_parser.parse()