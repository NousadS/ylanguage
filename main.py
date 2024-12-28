import json

from filer import Argumenter, Reader, Writer
from lexer import Lexer

if __name__ == "__main__":
    argumenter = Argumenter()

    reader = Reader(argumenter)

    lexer = Lexer(reader.source)

    writer = Writer(
        argumenter,
        json.dumps(
            lexer.tokens,
            ensure_ascii=False,
            indent=4,
        ),
    )
