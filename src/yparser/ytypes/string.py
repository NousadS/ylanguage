from .ytype import YType


class YString(YType):
    def __init__(self, value: any, **kwargs):
        super().__init__("STRING", value, **kwargs)

    def check(self) -> bool:
        return any(
            (
                self.value.startswith(quote)
                and (
                    self.value.endswith(quote) if self.value.count(quote) == 2 else True
                )
            )
            for quote in ("'", '"', "#", "`")
        )
