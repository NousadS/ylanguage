from .ytype import YType


class YDelimiter(YType):
    def __init__(self, value: any, **kwargs):
        super().__init__("DELIMITER", value, **kwargs)

    def check(self) -> bool:
        return self.value in ("\n", ";", ":", ",")
