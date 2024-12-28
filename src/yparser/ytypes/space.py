from .ytype import YType


class YSpace(YType):
    def __init__(self, value: any, **kwargs):
        super().__init__("SPACE", value, **kwargs)

    def check(self) -> bool:
        return all(c in (" ", "\t") for c in self.value)
