from .ytypes import parser_types


class YParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        self.position += 1

    def parse(self):
        ast = []
        while self.current_token():
            node = self.parse_statement()
            if node:
                ast.append(node)
        return ast

    def parse_statement(self):
        token = self.current_token()

        if isinstance(token, NumericToken):
            return self.parse_numeric_expression()

        if isinstance(token, StringToken):
            self.advance()
            return {"type": "String", "value": token.value}

        if isinstance(token, IdentifierToken):
            return self.parse_identifier_expression()

        if isinstance(token, BracketToken):
            return self.parse_bracket_structure()

        # Skip unhandled tokens (e.g., DELIMITER, SPACE)
        self.advance()
        return None

    def parse_numeric_expression(self):
        token = self.current_token()
        self.advance()

        # Unary operation: [OPERATOR] [VALUE]
        if self.current_token() and isinstance(self.current_token(), IdentifierToken):
            operator = token
            operand = self.current_token()
            self.advance()
            return {
                "type": "UnaryExpression",
                "operator": operator.value,
                "operand": operand.value
            }

        # Binary operation: [VALUE] [OPERATOR] [VALUE]
        if self.current_token() and isinstance(self.current_token(), IdentifierToken):
            operator = self.current_token()
            self.advance()
            if self.current_token() and isinstance(self.current_token(), NumericToken):
                rhs = self.current_token()
                self.advance()
                return {
                    "type": "BinaryExpression",
                    "operator": operator.value,
                    "left": token.value,
                    "right": rhs.value
                }

        return {"type": "Number", "value": token.value}

    def parse_identifier_expression(self):
        token = self.current_token()
        self.advance()
        return {"type": "Identifier", "name": token.value}

    def parse_bracket_structure(self):
        opening_bracket = self.current_token()
        self.advance()

        elements = []
        while self.current_token() and not isinstance(self.current_token(), BracketToken):
            if isinstance(self.current_token(), DelimiterToken):
                self.advance()
                continue

            elements.append(self.parse_statement())

        closing_bracket = self.current_token()
        self.advance()

        return {
            "type": "BracketStructure",
            "bracketType": opening_bracket.value,
            "elements": elements
        }o