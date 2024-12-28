from .ytype import YType


class YIdentifier(YType):
    def __init__(self, value: any):
        super().__init__("IDENTIFIER", value)

    def check(self) -> bool:
        return not self.value[0].isdigit() and all(c.isalnum() for c in self.value)
