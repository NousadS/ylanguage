from .ytype import YType


class YIdentifier(YType):
    def __init__(self, value: any, **kwargs):
        super().__init__("IDENTIFIER", value, **kwargs)

    def check(self) -> bool:
        return not self.value[0].isdigit() and (
            all(c.isalnum() for c in self.value)
            or all(c in r"!$%&*+-./=?@\^_|~" for c in self.value)
        )
