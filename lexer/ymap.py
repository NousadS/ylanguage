from .ytype import YType


class YMap(YType):
    def __init__(self, value: any):
        super().__init__("MAP", value)

    def check(self) -> bool:
        return any(
            (
                self.value[0] == start and self.value[-1] == end
                if (self.value.count(end) == 2 if start == end else end in self.value)
                else self.value[0] == start
            )
            for start, end in [
                ("(", ")"),
                ("{", "}"),
                ("[", "]"),
                ('"', '"'),
                ("'", "'"),
                ("#", "#"),
            ]
        )
