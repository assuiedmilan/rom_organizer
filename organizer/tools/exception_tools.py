import traceback


class ExceptionPrinter(object):

    @staticmethod
    def print_exception(exception_to_print, rethrow=False):
        traceback.print_exc()
        print(exception_to_print.message)

        if rethrow:
            raise exception_to_print
