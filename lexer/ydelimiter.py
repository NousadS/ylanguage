from .ytype import YType


class YDelimiter(YType):
    def __init__(self, value: any):
        super().__init__("DELIMITER", repr(value))

    def check(self) -> bool:
        return self.value == repr("\n")
