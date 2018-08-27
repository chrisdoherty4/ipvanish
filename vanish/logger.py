import logging


class style(object):
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

    @staticmethod
    def format(message, format):
        return "".join([format, message, style.ENDC])


class Formatter(logging.Formatter):
    def format(self, record):
        return record.msg


_formatter = Formatter()

_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)

logger = logging.getLogger('vanish')
logger.setLevel(logging.INFO)
logger.addHandler(_handler)
