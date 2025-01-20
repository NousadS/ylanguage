import logging
from turtle import pos
from typing import Self

from .yerrors import YBadSyntaxError, YInvalidChecksError, YInvalidLoggingError
from .ynodes import (
    YCallExpression,
    YCurlyScope,
    YExpression,
    YNode,
    YRoundScope,
    YScope,
    YSquareScope,
    YValue,
)
from .ytokens import YToken


class YParser:
    def __init__(self) -> None:
        self.values = YValue.__subclasses__()
        self.scopes = YScope.__subclasses__()
        self.expressions = YExpression.__subclasses__()

    def log(self, *text: str, level: str = "debug") -> None:
        joined = " ".join(text)

        try:
            getattr(logging.getLogger("Y"), level)(joined, extra={"part": "PARSER"})
        except AttributeError:
            raise YInvalidLoggingError(f"Invalid log level: {level}")

    def typenize(self, new: list[YToken], classes: list[type]) -> YNode | None:
        nodes = [node(new.copy()) for node in classes]
        checks = [node.check() for node in nodes]
        count = checks.count(True)

        if count == 0:
            return None
        elif count == 1:
            return nodes[checks.index(True)]
        else:
            errors = ", ".join(
                [node.name for node, check in zip(nodes, checks) if check]
            )

            raise YInvalidChecksError(f"Invalid checks: <{new}> ({errors})")

    def parse(self, data: list[YToken]) -> list[YScope | YNode]:
        self.log("PARSE")

        data = [t for t in data if t != "SPACE"]

        parsed: list[YNode] = []
        node: YNode = None

        position: int = 0
        span: int = 0

        while position < len(data):
            while node is None:
                node = self.typenize(data[position : position + span], self.values)

                if node is None:
                    span += 1

                if position + span > len(data):
                    raise YBadSyntaxError("Bad Syntax")

            position += span
            span = 0

            parsed.append(node)
            self.log(f"[{str(position).center(len(str(len(data))))}]", str(node))

            node = None

        self.log("END PARSE")

        return parsed

    def scope(self, data: list[YNode]) -> list[YScope | YNode]:
        self.log("SCOPE")

        scoped: list[YScope | YNode] = []
        scope: YScope = None

        position: int = 0
        span: int = 0

        while position < len(data):
            while scope is None:
                scope = self.typenize(data[position : position + span], self.scopes)

                if scope is None:
                    span += 1

                if position + span > len(data):
                    scoped.append(data[position])

                    position += 1
                    span = 0

                    break

            position += span
            span = 0

            if scope is not None:
                scoped.append(scope)

                self.log(f"[{str(position).center(len(str(len(data))))}]", str(scope))

            scope = None

        for e in scoped:
            if isinstance(e, YScope):
                e.nodes = self.scope(e.nodes[1:-1])

                if isinstance(e, YCurlyScope) and not any(
                    n == "Comma" for n in e.nodes
                ):
                    e.nodes = self.expressionize(e.nodes)
                else:
                    e.nodes = self.expressionize(e.nodes, "Comma")

        self.log("END SCOPE")

        return scoped

    def expressionize(
        self, data: list[YScope | YNode], delimiter: str = "Line"
    ) -> list[YExpression]:
        self.log("EXPRESSIONIZE")

        expressioned: list[YExpression] = []

        new: list[list[YNode]] = [[]]

        if delimiter == "Comma":
            data = [n for n in data if n != "Line"]

        for element in data:
            if element == delimiter:
                new.append([])
            else:
                new[-1].append(element)

        data = new

        for position, element in enumerate(data):
            if element != []:
                expression: YExpression = self.typenize(
                    element, self.expressions
                )

                if expression is None:
                    print(element)
                    raise ValueError("Bad Syntax")

                if expression is not None:
                    expressioned.append(expression)

                    self.log(
                        f"[{str(position).center(len(str(len(data))))}]",
                        str(expression),
                    )

        self.log("END EXPRESSIONIZE")

        return expressioned

    def serialize(
        self, expressioned: list[YExpression], mode: str = "str"
    ) -> str | list[dict[str, str]]:
        if mode == "dict":
            return [expression.as_dict() for expression in expressioned]
        elif mode == "ast":
            return expressioned.copy()
        else:
            return "\n".join([expression.as_str() for expression in expressioned])
