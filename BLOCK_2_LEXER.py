# ==================================================
# VELOCITY BLOCK 2 - LEXER
# ==================================================

KEYWORDS = {
    "func",
    "return",
    "when",
    "loop",
    "import",
    "true",
    "false"
}


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.tokens = []

    def current(self):
        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    def advance(self):
        self.position += 1

    # ==========================================
    # NUMBERS
    # ==========================================

    def read_number(self):

        result = ""

        while (
            self.current() is not None
            and (
                self.current().isdigit()
                or self.current() == "."
            )
        ):
            result += self.current()
            self.advance()

        value = float(result)

    # frame interval

        if self.current() == "f":

            self.advance()

            return Token(
                "FRAME_INTERVAL",
                value
            )

    # second interval

        if (
            self.current() == "s"
            and self.source[
                self.position:self.position + 3
            ] == "sec"
        ):

            self.position += 3

            return Token(
                "SECOND_INTERVAL",
                value
            )

        return Token(
            "NUMBER",
            value
        )

    # ==========================================
    # STRINGS
    # ==========================================

    def read_string(self):

        self.advance()

        result = ""

        while (
            self.current() is not None
            and self.current() != '"'
        ):
            result += self.current()
            self.advance()

        self.advance()

        return Token("STRING", result)

    # ==========================================
    # IDENTIFIERS / KEYWORDS
    # ==========================================

    def read_identifier(self):

        result = ""

        while (
            self.current() is not None
            and (
                self.current().isalnum()
                or self.current() == "_"
            )
        ):
            result += self.current()
            self.advance()

        if result in KEYWORDS:
            return Token("KEYWORD", result)

        return Token("IDENTIFIER", result)

    # ==========================================
    # MAIN TOKENIZER
    # ==========================================

    def tokenize(self):

        while self.current() is not None:

            char = self.current()

            # whitespace

            if char.isspace():
                self.advance()
                continue

            # comments

            if char == "#":

                while (
                    self.current() is not None
                    and self.current() != "\n"
                ):
                    self.advance()

                continue

            # numbers

            if char.isdigit():
                self.tokens.append(
                    self.read_number()
                )
                continue

            # strings

            if char == '"':
                self.tokens.append(
                    self.read_string()
                )
                continue

            # identifiers

            if char.isalpha() or char == "_":
                self.tokens.append(
                    self.read_identifier()
                )
                continue

            # double operators

            two = self.source[
                self.position:self.position + 2
            ]

            if two in [
                "==",
                "!=",
                ">=",
                "<="
            ]:
                self.tokens.append(
                    Token("OPERATOR", two)
                )

                self.position += 2
                continue

            # single operators

            if char in "+-*/=><":

                self.tokens.append(
                    Token("OPERATOR", char)
                )

                self.advance()
                continue

            # symbols

            if char in "(){}[],:":

                self.tokens.append(
                    Token("SYMBOL", char)
                )

                self.advance()
                continue

            raise Exception(
                f"Unexpected character: {char}"
            )

        self.tokens.append(
            Token("EOF", None)
        )

        return self.tokens