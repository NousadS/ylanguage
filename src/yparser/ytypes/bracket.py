from .ytype import YType


class YBracket(YType):
    def __init__(self, value: any, **kwargs):
        super().__init__("BRACKET", value, **kwargs)

    def check(self) -> bool:
        return self.value in ("(", ")", "[", "]", "{", "}", "<", ">")
