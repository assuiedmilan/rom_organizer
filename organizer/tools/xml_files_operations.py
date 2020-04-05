from lxml import etree

from organizer.tools.exception_tools import ExceptionPrinter


class XmlFilesOperations(object):

    @staticmethod
    def write(document_to_write, target):
        document_to_write.write(target, pretty_print=True)

    @staticmethod
    def parse(file_to_parse):
        parser = etree.XMLParser(remove_blank_text=True)

        try:
            return etree.parse(file_to_parse, parser)
        except Exception as something_happened:
            ExceptionPrinter.print_exception(something_happened)

