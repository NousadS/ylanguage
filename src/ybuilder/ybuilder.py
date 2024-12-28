import json
import pathlib
import types
from json import JSONEncoder
from pathlib import Path

from ..ylexer import YLexer
from ..yparser import YParser
from .yreader import YReader
from .ywriter import YWriter


class YBuilder:
    def __init__(self, filename: str = "main.y", encoding: str = "utf-8"):
        self.input = Path(filename)
        self.output = Path(self.input).with_suffix(".by")

        self.encoding = encoding

        self.reader = YReader()
        self.writer = YWriter()

        self.lexer = YLexer()
        self.parser = YParser()

    def build(self) -> None:
        self.data = self.reader.read(self.input, self.encoding)

        self.lexer_data = self.lexer.tokenize(self.data)
        self.lexer_data = self.lexer.serialize(self.lexer_data)

        self.parser_data = self.parser.parse(self.lexer_data)
        self.parser_data = self.parser.serialize(self.parser_data)

        self.code = self.parser_data

        self.writer.write(
            self.output,
            self.encoding,
            json.dumps(self.code, indent=4, ensure_ascii=False),
        )
