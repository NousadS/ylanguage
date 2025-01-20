import logging
from typing import Self

from .yerrors import YInvalidLoggingError, YInvalidRegexesError
from .ytokens import YToken


class YLexer:
    def __init__(self) -> None:
        self.types = YToken.__subclasses__()
        self.tokens: list[YToken] = []

    def log(self, *text: str, level: str = "debug") -> None:
        joined = " ".join(text)

        try:
            getattr(logging.getLogger("Y"), level)(joined, extra={"part": "LEXER"})
        except AttributeError:
            raise YInvalidLoggingError(f"Invalid log level: {level}")

    def typenize(self, new: str) -> YToken | None:
        tokens = [token(new) for token in self.types]
        checks = [token.check() for token in tokens]
        count = checks.count(True)

        self.log(f"Tokens for {repr(new)}:")

        log_tokens = [t.as_str() for t in tokens]

        log_tokens_rows = [log_tokens[i : i + 2] for i in range(0, len(log_tokens), 2)]
        log_checks_rows = [checks[i : i + 2] for i in range(0, len(checks), 2)]

        max_lenght = max(len(t) for t in log_tokens)

        log_tokens_rows = [[t.ljust(max_lenght) for t in r] for r in log_tokens_rows]

        log_checks_rows = [
            [str(c).ljust(max_lenght) for c in r] for r in log_checks_rows
        ]

        for r, c in zip(log_tokens_rows, log_checks_rows):
            self.log(f"{'    '.join(r)}")
            self.log(f"{'    '.join(c)}")

        self.log("")

        if count == 0:
            return None
        elif count == 1:
            return tokens[checks.index(True)]
        else:
            raise YInvalidRegexesError(
                f"Invalid regexes: <{new}> ({
                    ', '.join(
                        [token.name for token, check in zip(tokens, checks) if check]
                    )
                })"
            )

    def new(self, old: YToken | None) -> None:
        if old is not None:
            self.log("------------------")

            self.tokens.append(old)

    def tokenize(self, data: str) -> Self:
        self.log("TOKENIZE")

        data += "\n"

        token = None
        position = 0

        while position < len(data):
            if token is None:
                new_token = self.typenize(data[position])
            else:
                new_token = self.typenize(token.value + data[position])

            if new_token is None:
                self.new(token)

                token = self.typenize(data[position])
            else:
                token = new_token

            self.log(
                f"[{str(position).center(len(str(len(data))))}]",
                f"{f'<{repr(data[position])[1:-1]}>': <4}",
                f"{token}",
            )

            position += 1

        self.new(token)

        self.log("END TOKENIZE")

        return self

    def stringize(self) -> Self:
        self.log("STRINGIZE")

        log_before = len(self.tokens)

        position = 0
        span = 1

        while position < len(self.tokens):
            span = 1

            if self.tokens[position - 1] in ("STRING", "COMMENT"):
                span = 0

                self.tokens[position - 1].value += self.tokens[position].value

                if self.tokens[position] in ("STRING", "COMMENT"):
                    if self.tokens[position - 1].value[-2] != "\\":
                        if (
                            self.tokens[position - 1].value[0]
                            == self.tokens[position].value[0]
                        ):
                            span = 1

                del self.tokens[position]

            position += span

        self.log(
            f"Tokens lenght: {log_before} -> {len(self.tokens)} (-{log_before - len(self.tokens)})"
        )

        self.log("END STRINGIZE")

        return self

    def optimize(self) -> Self:
        self.log("OPTIMIZE")

        log_before = len(self.tokens)
        
        self.tokens = [t for t in self.tokens if t != "COMMENT"]

        self.log(
            f"Tokens lenght: {log_before} -> {len(self.tokens)} (-{log_before - len(self.tokens)})"
        )

        self.log("END OPTIMIZE")

        return self

    def serialize(self, mode: str = "str") -> str | list[dict[str, str]]:
        if mode == "list":
            return [token.as_dict() for token in self.tokens]
        elif mode == "tokens":
            return self.tokens.copy()
        else:
            return "\n".join([token.as_str() for token in self.tokens])
