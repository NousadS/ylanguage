import re
from typing import Self


class YToken:
    def __init__(self, name: str, value: str, regex: str) -> None:
        self.name = name
        self.value = value
        self.regex = regex

    def check(self) -> bool:
        self.regex = (
            re.compile(self.regex, re.UNICODE | re.DOTALL)
            if isinstance(self.regex, re.Pattern)
            else self.regex
        )

        matched = re.match(self.regex, self.value)

        return matched is not None and matched.span() == (0, len(self.value))

    def as_value(self) -> str:
        return repr(self.value)[1:-1]

    def as_dict(self) -> dict[str, object]:
        return {"name": self.name, "value": self.value}

    def as_str(self) -> str:
        return f"{self.name}<{self.as_value()}>"
    
    def __repr__(self) -> str:
        return self.as_str()

    def __str__(self) -> str:
        return self.as_str()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, YToken):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        elif isinstance(other, tuple):
            return self.name == other[0] and self.value == str(other[1])
        else:
            raise NotImplementedError

    def __contains__(self, item: str) -> bool:
        return self.__eq__(item)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class YIdentifierToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("IDENTIFIER", value, r"[^\W\d][\w]*")


class YOperatorToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("OPERATOR", value, r"[^\w\s\d#(){}\[\]\'\"\`\,]+")


class YDelimiterToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("DELIMITER", value, r"[\,\n]")


class YIntegerBinaryToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("INTEGER_BINARY", value, r"0b[0-1]*")


class YIntegerOctalToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("INTEGER_OCTAL", value, r"0o[0-7]*")


class YIntegerDecimalToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("INTEGER_DECIMAL", value, r"(0d[0-9]*|[0-9]+)")


class YIntegerHexadecimalToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("INTEGER_HEXADECIMAL", value, r"0x[0-9a-fA-F]*")


class YFloatBinaryToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("FLOAT_BINARY", value, r"0b[0-1]+\.[0-1]*")


class YFloatOctalToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("FLOAT_OCTAL", value, r"0o[0-7]+\.[0-7]*")


class YFloatDecimalToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("FLOAT_DECIMAL", value, r"(0d)?[0-9]+\.[0-9]*")


class YFloatHexadecimalToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("FLOAT_HEXADECIMAL", value, r"0x[0-9a-fA-F]+\.[0-9a-fA-F]*")


class YSpaceToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("SPACE", value, r"[ ]+|[\t]+|[\f\v]+")


class YPairToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("PAIR", value, r"[\(\[\{\)\]\}]")


class YStringToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("STRING", value, r"[\'\"\`]")

class YCommentToken(YToken):
    def __init__(self, value: str) -> None:
        super().__init__("COMMENT", value, r"\#")
