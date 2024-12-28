class YType:
    def __init__(self, type: str, value: str) -> None:
        self.type: str = str(type).upper()
        self.value: str = str(value)

    def check(self) -> bool:
        return False

    def __repr__(self):
        return f"{self.type}({self.value})"


class YInteger(YType):
    def __init__(self, value: any):
        super().__init__("INTEGER", value)

    def check(self) -> bool:
        return all(c.isdigit() or c == "_" or c == "-" for c in self.value)


class YUnaryOperator(YType):
    def __init__(self, value: any):
        super().__init__("UNARY_OPERATOR", value)

    def check(self) -> bool:
        return self.value in ["+", "-"]


class YIdentifier(YType):
    def __init__(self, value: any):
        super().__init__("IDENTIFIER", value)

    def check(self) -> bool:
        return (
            len(self.value) > 0
            and not self.value[0].isdigit()
            and all(
                c.isdigit() or c.isalnum() or c == "_" or c == "-" for c in self.value
            )
        )


class Lexer:
    def __init__(self, text: str) -> None:
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
            for ytype in YType.__subclasses__():
                if ytype == self.token.__class__:
                    new_token = ytype(self.token.value + self.character)

                    if new_token.check():
                        self.token = new_token

                        break
            else:
                if self.token is not None:
                    self.tokens.append(self.token)
                
                self.token = None

                for ytype in YType.__subclasses__():
                    new_token = ytype(self.character)

                    if new_token.check():
                        self.token = new_token

                        break

            self.position += 1

        if self.token is not None:
            self.tokens.append(self.token)
            

if __name__ == "__main__":
    code = "hello 123_123 define world +123"
    lexer = Lexer(code)
    lexer.tokenize()

    print(lexer.tokens)
