from .ytypes import YType


class YLexer:
    def __init__(self) -> None:
        self.order = YType.__subclasses__()

    def tokenize(self, data: str) -> list[YType]:
        data += "\n"
        tokens: list = []

        token: str = ""
        token_type: YType = None
        position: int = 0

        while position < len(data):
            character: str = data[position]
            matched: bool = False

            for new_token_type in self.order:
                new_token = token + character if token else character

                if new_token_type(new_token).check():
                    token = new_token
                    token_type = new_token_type
                    matched = True
                    break

            if not matched:
                if token:
                    tokens.append(token_type(token))

                    token = ""
                    token_type = None

                for new_token_type in self.order:
                    if new_token_type(character).check():
                        token = character
                        token_type = new_token_type
                        break

            position += 1

        if token:
            tokens.append(token_type(token))

        return tokens

    def serialize(self, tokens: list[YType]) -> list:
        return [{"type": token.type, "value": token.value} for token in tokens]
