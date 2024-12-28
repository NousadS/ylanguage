from .ytype import YType


class YInteger(YType):
    def __init__(self, value: any):
        super().__init__("INTEGER", value)

    def check(self) -> bool:
        return all(c.isdigit() or c == "_" or c == "-" for c in self.value)
