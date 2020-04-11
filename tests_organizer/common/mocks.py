import mock
from lxml import etree

from tests_organizer.common import gamelist

PARSED_DOCUMENT = etree.fromstring(gamelist.XML_DOCUMENT)

mocked_parser = mock.Mock()
mocked_parser.return_value = PARSED_DOCUMENT

mocked_validation = mock.Mock()
mocked_validation.return_value = True