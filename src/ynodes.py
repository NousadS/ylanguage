from typing import Self

from .ytokens import YStringToken, YToken


class YNode:
    def __init__(self, name: str):
        self.name: str = name

    def check(self) -> bool:
        return False

    def as_dict(self) -> dict[str, object]:
        return {"name": self.name}

    def as_str(self) -> str:
        return f"{self.name} ?"

    def __repr__(self) -> str:
        return self.as_str()

    def __str__(self) -> str:
        return self.as_str()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, YNode):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __contains__(self, item: str) -> bool:
        return self.__eq__(item)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class YValue(YNode):
    def __init__(self, name: str, tokens: list[YToken]):
        self.name: str = name
        self.tokens: list[YToken] = tokens

    def as_dict(self) -> dict[str, object]:
        return {"name": self.name, "tokens": [t.as_dict() for t in self.tokens]}

    def as_str(self) -> str:
        return f"{self.name}<{''.join([t.as_value() for t in self.tokens])}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, YValue):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        elif (
            isinstance(other, tuple)
            and len(other) == 2
            and isinstance(other[0], str)
            and isinstance(other[1], str)
        ):
            return self.name == other[0] and self.tokens[0].value == other[1]
        else:
            return False


class YIdentifierValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("Identifier", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "IDENTIFIER"


class YOperatorValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("Operator", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "OPERATOR"


class YIntegerBinaryValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("IntegerBinary", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "INTEGER_BINARY"


class YIntegerOctalValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("IntegerOctal", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "INTEGER_OCTAL"


class YIntegerDecimalValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("IntegerDecimal", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "INTEGER_DECIMAL"


class YIntegerHexadecimalValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("IntegerHexadecimal", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "INTEGER_HEXADECIMAL"


class YFloatBinaryValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("FloatBinary", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "FLOAT_BINARY"


class YFloatOctalValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("FloatOctal", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "FLOAT_OCTAL"


class YFloatDecimalValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("FloatDecimal", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "FLOAT_DECIMAL"


class YFloatHexadecimalValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("FloatHexadecimal", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "FLOAT_HEXADECIMAL"


class YPairValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("Pair", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "PAIR"


class YCommaValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("Comma", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == ("DELIMITER", ",")


class YLineValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("Line", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == ("DELIMITER", "\n")


class YStringValue(YValue):
    def __init__(self, tokens: list[YToken]) -> None:
        super().__init__("String", tokens)

    def check(self) -> bool:
        return len(self.tokens) == 1 and self.tokens[0] == "STRING"


class YScope(YNode):
    def __init__(self, name: str, nodes: list[YToken]):
        self.name: str = name
        self.nodes: list[YNode] = nodes

    def as_dict(self) -> dict[str, object]:
        return {"name": self.name, "nodes": [n.as_dict() for n in self.nodes]}

    def as_str(self) -> str:
        return f"{self.name}<{', '.join([n.as_str() for n in self.nodes])}>"


class YRoundScope(YScope):
    def __init__(self, nodes: list[YToken]) -> None:
        super().__init__("Round", nodes)

    def check(self) -> bool:
        return (
            len(self.nodes) >= 2
            and self.nodes.count(("Pair", "(")) == self.nodes.count(("Pair", ")"))
            and self.nodes[0] == ("Pair", "(")
            and self.nodes[-1] == ("Pair", ")")
        )


class YSquareScope(YScope):
    def __init__(self, nodes: list[YToken]) -> None:
        super().__init__("Square", nodes)

    def check(self) -> bool:
        return (
            len(self.nodes) >= 2
            and self.nodes.count(("Pair", "[")) == self.nodes.count(("Pair", "]"))
            and self.nodes[0] == ("Pair", "[")
            and self.nodes[-1] == ("Pair", "]")
        )


class YCurlyScope(YScope):
    def __init__(self, nodes: list[YToken]) -> None:
        super().__init__("Curly", nodes)

    def check(self) -> bool:
        return (
            len(self.nodes) >= 2
            and self.nodes.count(("Pair", "{")) == self.nodes.count(("Pair", "}"))
            and self.nodes[0] == ("Pair", "{")
            and self.nodes[-1] == ("Pair", "}")
        )


class YExpression(YNode):
    def __init__(self, name: str, nodes: list[YNode]):
        self.name: str = name
        self.nodes: list[YNode] = nodes

    def as_dict(self) -> dict[str, object]:
        return {"name": self.name, "nodes": [n.as_dict() for n in self.nodes]}

    def as_str(self) -> str:
        return f"{self.name} -> {' '.join([n.as_str() for n in self.nodes])}"


OPERANDS = (
    "Identifier",
    "Operator",
    "IntegerBinary",
    "IntegerOctal",
    "IntegerDecimal",
    "IntegerHexadecimal",
    "FloatBinary",
    "FloatOctal",
    "FloatDecimal",
    "FloatHexadecimal",
    "Round",
    "Square",
    "Curly",
    "String",
    #
    "CallExpression",
)


class YFlatExpression(YExpression):
    def __init__(self, nodes: list[YNode]):
        super().__init__("FlatExpression", nodes)

    def check(self) -> bool:
        for span in [2, 3]:
            call_expression: YCallExpression = None
            call_position: int = 0

            while len(self.nodes[call_position : call_position + 2]) == 2:
                call_expression = YCallExpression(
                    self.nodes[call_position : call_position + 2]
                )

                if call_expression.check():
                    self.nodes[call_position] = call_expression
                    del self.nodes[call_position + 1]
                else:
                    call_position += 1


        return (
            len(self.nodes) == 2
            and (
                (self.nodes[0] in OPERANDS and self.nodes[1] == "Operator")
                or (self.nodes[0] == "Operator" and self.nodes[1] in OPERANDS)
            )
        ) or (
            len(self.nodes) >= 3
            and len(self.nodes) % 2 == 1
            and all(self.nodes[i] in OPERANDS for i in range(0, len(self.nodes), 2))
            and all(
                self.nodes[i] == "Operator" for i in range(1, len(self.nodes) - 1, 2)
            )
        )


class YCallExpression(YExpression):
    def __init__(self, nodes: list[YNode]):
        super().__init__("CallExpression", nodes)

    def check(self) -> bool:
        return (
            len(self.nodes) == 2
            and self.nodes[0] == "Identifier"
            and self.nodes[1] == "Round"
        ) or (
            len(self.nodes) == 3
            and self.nodes[0] == "Identifier"
            and self.nodes[1] == "Square"
            and self.nodes[2] == "Round"
        )


class YCallExtendedExpression(YExpression):
    def __init__(self, nodes: list[YNode]):
        super().__init__("CallExtendedExpression", nodes)

    def check(self) -> bool:
        return (
            len(self.nodes) == 4
            and self.nodes[0] == "Identifier"
            and self.nodes[1] == "Round"
            and self.nodes[2] == ("Operator", ":")
            and self.nodes[3] == "Curly"
        ) or (
            len(self.nodes) == 5
            and self.nodes[0] == "Identifier"
            and self.nodes[1] == "Square"
            and self.nodes[2] == "Round"
            and self.nodes[3] == ("Operator", ":")
            and self.nodes[4] == "Curly"
        )


class YDefineExpression(YExpression):
    def __init__(self, nodes: list[YNode]):
        super().__init__("DefineExpression", nodes)

    def check(self) -> bool:
        return (
            len(self.nodes) > 2
            and self.nodes[0] == "Identifier"
            and self.nodes[1] == "Identifier"
            and (
                (
                    len(self.nodes) == 5
                    and self.nodes[2] == "Round"
                    and self.nodes[3] == ("Operator", ":")
                    and self.nodes[4] == "Curly"
                )
                or (
                    len(self.nodes) == 7
                    and self.nodes[2] == "Round"
                    and self.nodes[3] == ("Operator", "->")
                    and self.nodes[4] == "Identifier"
                    and self.nodes[5] == ("Operator", ":")
                    and self.nodes[6] == "Curly"
                )
                or (
                    len(self.nodes) == 4
                    and self.nodes[2] == ("Operator", ":")
                    and self.nodes[3] == "Curly"
                )
                or (
                    len(self.nodes) == 5
                    and self.nodes[2] == "Round"
                    and self.nodes[3] == ("Operator", ":")
                    and self.nodes[4] == "Curly"
                )
                or (
                    len(self.nodes) == 5
                    and self.nodes[2] == "Square"
                    and self.nodes[3] == ("Operator", ":")
                    and self.nodes[4] == "Curly"
                )
                or (
                    len(self.nodes) == 6
                    and self.nodes[2] == "Square"
                    and self.nodes[3] == "Round"
                    and self.nodes[4] == ("Operator", ":")
                    and self.nodes[5] == "Curly"
                )
            )
        )


class YElementExpression(YExpression):
    def __init__(self, nodes: list[YNode]):
        super().__init__("ElementExpression", nodes)

    def check(self) -> bool:
        return len(self.nodes) == 1 and self.nodes[0] in OPERANDS
