from .ytype import YType


class YNumeric(YType):
    def __init__(self, value: any, **kwargs):
        super().__init__("NUMERIC", value, **kwargs)

    def check(self) -> bool:
        return (
            not self.value.startswith(("-", "_"))
            and not self.value.endswith(("-", "_", ",", "."))
            and all(c.isdigit() or c in ("-", "_", ",", ".") for c in self.value)
        )
