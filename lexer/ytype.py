class YType:
    def __init__(self, type: str, value: str) -> None:
        self.type: str = str(type).upper()
        self.value: str = str(value)

    def check(self) -> bool:
        return False

    def __repr__(self):
        return f"{self.type}<{self.value}>"


