class YType:
    def __init__(self, type: str, value: str) -> None:
        self.type: str = str(type).upper()
        self.value: str = str(value)

    def check(self) -> bool:
        return False

    def __repr__(self):
        return f"{self.type}<{self.value}>"

    def dict(self):
        return {"type": self.type, "value": self.value}

    def __eq__(self, other: "YType") -> bool:
        if isinstance(other, YType):
            return self.type == other.type and self.value == other.value
        else:
            return False

    def __ne__(self, other: "YType") -> bool:
        return not self.__eq__(other)
