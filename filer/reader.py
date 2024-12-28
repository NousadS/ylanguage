from .argumenter import Argumenter


class Reader:
    def __init__(self, parser: Argumenter):
        self.filename = parser.input
        self.encoding = parser.encoding

        with open(self.filename, "r", encoding=self.encoding) as file:
            self.source = file.read()