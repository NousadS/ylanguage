from .ydelimiter import YDelimiter  # noqa: F401
from .yidentifier import YIdentifier  # noqa: F401
from .yinteger import YInteger  # noqa: F401
from .ymap import YMap  # noqa: F401
from .yoperator import YOperator  # noqa: F401
from .ytype import YType


class Lexer:
    def __init__(self, text: str) -> None:
        self.order = YType.__subclasses__()

        self.data = text

        self.token = None
        self.position = 0
        
        self.tokens = []

        self.tokenize()

    @property
    def character(self) -> str | None:
        if self.position >= len(self.data):
            return None

        return self.data[self.position]

    def tokenize(self):
        while self.character is not None:
            for ytype in self.order:
                if ytype == self.token.__class__:
                    new_token = ytype(self.token.value + self.character)

                    if new_token.check():
                        self.token = new_token

                        break
            else:
                if self.token is not None:
                    self.tokens.append(self.token)

                self.token = None

                for ytype in self.order:
                    new_token = ytype(self.character)

                    if new_token.check():
                        self.token = new_token

                        break

            self.position += 1

        if self.token is not None:
            self.tokens.append(self.token)

        return self
