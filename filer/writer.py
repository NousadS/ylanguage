from .argumenter import Argumenter


class Writer:
    def __init__(self, parser: Argumenter, code: str):
        self.filename = parser.output
        self.encoding = parser.encoding

        with open(self.filename, "w", encoding=self.encoding) as file:
            file.write(code)