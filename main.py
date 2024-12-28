class YType:
    def __init__(self, type: str, value: str) -> None:
        self.type: str = str(type).upper()
        self.value: str = str(value)

    def check(self) -> bool:
        return False

    def __repr__(self):
        return f"{self.type}<{self.value}>"


class YInteger(YType):
    def __init__(self, value: any):
        super().__init__("INTEGER", value)

    def check(self) -> bool:
        return all(c.isdigit() or c == "_" or c == "-" for c in self.value)


class YString(YType):
    def __init__(self, value: any):
        super().__init__("STRING", value)

    def check(self) -> bool:
        return any(
            (
                self.value[0] == delimiter and self.value[-1] == delimiter
                if self.value.count(delimiter) == 2
                else self.value[0] == delimiter
            )
            for delimiter in ('"', "'")
        )


class YMap(YType):
    def __init__(self, value: any):
        super().__init__("MAP", value)

    def check(self) -> bool:
        return any(
            (
                self.value[0] == start and self.value[-1] == end
                if end in self.value
                else self.value[0] == start
            )
            for start, end in [("(", ")"), ("{", "}"), ("[", "]")]
        )


class YIdentifier(YType):
    def __init__(self, value: any):
        super().__init__("IDENTIFIER", value)

    def check(self) -> bool:
        return not self.value[0].isdigit() and all(c.isalnum() for c in self.value)


class YOperator(YType):
    def __init__(self, value: any):
        super().__init__("OPERATOR", value)

    def check(self) -> bool:
        return all(c in r"!#$%&*+,-./:;<=>?@\^_`|~" for c in self.value)


class YDelimiter(YType):
    def __init__(self, value: any):
        super().__init__("DELIMITER", repr(value))

    def check(self) -> bool:
        return self.value == repr("\n")


class Lexer:
    def __init__(self, text: str) -> None:
        self.order = YType.__subclasses__()

        self.data = text
        self.tokens = []

        self.token = None
        self.position = 0

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


if __name__ == "__main__":
    code = 'hello 123_123 define "hello" привет +123 (1, 2, 3)\n'
    lexer = Lexer(code)
    lexer.tokenize()

    print(lexer.tokens)
