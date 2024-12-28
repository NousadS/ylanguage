from .ytype import YType


class YOperator(YType):
    def __init__(self, value: any):
        super().__init__("OPERATOR", value)

    def check(self) -> bool:
        return all(c in r"!$%&*+,-./:;<=>?@\^_`|~" for c in self.value)
