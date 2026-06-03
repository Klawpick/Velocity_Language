from BLOCK_1_AST import *


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    # =====================================
    # HELPERS
    # =====================================

    def current(self):
        return self.tokens[self.position]

    def peek(self, offset=1):

        pos = self.position + offset

        if pos >= len(self.tokens):
            return self.tokens[-1]

        return self.tokens[pos]

    def advance(self):
        self.position += 1

    def expect(self, token_type, value=None):

        token = self.current()

        if token.type != token_type:
            raise Exception(
                f"Expected {token_type}, got {token.type}"
            )

        if (
            value is not None
            and token.value != value
        ):
            raise Exception(
                f"Expected {value}, got {token.value}"
            )

        self.advance()

        return token

    # =====================================
    # PRIMARY EXPRESSIONS
    # =====================================

    def parse_expression(self):

        return self.parse_comparison()

    def parse_primary(self):

        token = self.current()

        # Parentheses

        if (
                token.type == "SYMBOL"
                and token.value == "("
        ):
            self.advance()

            expr = self.parse_expression()

            self.expect(
                "SYMBOL",
                ")"
            )

            return expr

        # Number

        if token.type == "NUMBER":
            self.advance()

            return Number(
                token.value
            )

        if (
                token.type == "OPERATOR"
                and token.value == "-"
        ):
            self.advance()

            return UnaryOperation(
                "-",
                self.parse_primary()
            )

        # String

        if token.type == "STRING":
            self.advance()

            return String(
                token.value
            )

        # true

        if (
                token.type == "KEYWORD"
                and token.value == "true"
        ):
            self.advance()

            return Boolean(True)

        # false

        if (
                token.type == "KEYWORD"
                and token.value == "false"
        ):
            self.advance()

            return Boolean(False)

        # arrays

        if (
                token.type == "SYMBOL"
                and token.value == "["
        ):
            return self.parse_array()

        # identifiers

        if token.type == "IDENTIFIER":

            name = token.value

            self.advance()

            if (
                    self.current().type == "SYMBOL"
                    and self.current().value == "("
            ):
                return self.parse_function_call(
                    name
                )

            if (
                    self.current().type == "SYMBOL"
                    and self.current().value == "["
            ):
                self.advance()

                index = self.parse_expression()

                self.expect(
                    "SYMBOL",
                    "]"
                )

                return ArrayAccess(
                    Identifier(name),
                    index
                )

            return Identifier(name)

        raise Exception(
            f"Unexpected token {token}"
        )

    def parse_factor(self):

        left = self.parse_primary()

        while (
                self.current().type == "OPERATOR"
                and
                self.current().value in ["*", "/"]
        ):
            op = self.current().value

            self.advance()

            right = self.parse_primary()

            left = BinaryOperation(
                left,
                op,
                right
            )

        return left

    def parse_term(self):

        left = self.parse_factor()

        while (
                self.current().type == "OPERATOR"
                and
                self.current().value in ["+", "-"]
        ):
            op = self.current().value

            self.advance()

            right = self.parse_factor()

            left = BinaryOperation(
                left,
                op,
                right
            )

        return left

    def parse_comparison(self):

        left = self.parse_term()

        while (
                self.current().type == "OPERATOR"
                and
                self.current().value in [
                    ">",
                    "<",
                    ">=",
                    "<=",
                    "==",
                    "!="
                ]
        ):
            op = self.current().value

            self.advance()

            right = self.parse_term()

            left = BinaryOperation(
                left,
                op,
                right
            )

        return left

    # =====================================
    # ARRAYS
    # =====================================

    def parse_array(self):

        self.expect(
            "SYMBOL",
            "["
        )

        items = []

        while not (
            self.current().type == "SYMBOL"
            and self.current().value == "]"
        ):

            items.append(
                self.parse_expression()
            )

            if (
                self.current().type == "SYMBOL"
                and self.current().value == ","
            ):
                self.advance()

        self.expect(
            "SYMBOL",
            "]"
        )

        return ArrayLiteral(items)

    # =====================================
    # FUNCTION CALLS
    # =====================================

    def parse_function_call(self, name):

        self.expect(
            "SYMBOL",
            "("
        )

        arguments = []

        while not (
            self.current().type == "SYMBOL"
            and self.current().value == ")"
        ):

            arguments.append(
                self.parse_expression()
            )

            if (
                self.current().type == "SYMBOL"
                and self.current().value == ","
            ):
                self.advance()

        self.expect(
            "SYMBOL",
            ")"
        )

        return FunctionCall(
            name,
            arguments
        )

    # =====================================
    # EXPRESSIONS
    # =====================================
    # =====================================
    # ASSIGNMENTS
    # =====================================

    def parse_assignment(self):

        name = self.expect(
            "IDENTIFIER"
        ).value

        self.expect(
            "OPERATOR",
            "="
        )

        value = self.parse_expression()

        return Assignment(
            name,
            value
        )

    def parse_array_assignment(self):

        array_name = self.expect(
            "IDENTIFIER"
        ).value

        self.expect(
            "SYMBOL",
            "["
        )

        index = self.parse_expression()

        self.expect(
            "SYMBOL",
            "]"
        )

        self.expect(
            "OPERATOR",
            "="
        )

        value = self.parse_expression()

        return ArrayAssignment(
            array_name,
            index,
            value
        )

    # =====================================
    # RETURN
    # =====================================

    def parse_return(self):

        self.expect(
            "KEYWORD",
            "return"
        )

        value = self.parse_expression()

        return ReturnStatement(
            value
        )

    # =====================================
    # FUNCTION DEFINITIONS
    # =====================================

    def parse_function_definition(self):

        self.expect(
            "KEYWORD",
            "func"
        )

        name = self.expect(
            "IDENTIFIER"
        ).value

        self.expect(
            "SYMBOL",
            "("
        )

        parameters = []

        while not (
            self.current().type == "SYMBOL"
            and self.current().value == ")"
        ):

            parameters.append(
                self.expect(
                    "IDENTIFIER"
                ).value
            )

            if (
                self.current().type == "SYMBOL"
                and self.current().value == ","
            ):
                self.advance()

        self.expect(
            "SYMBOL",
            ")"
        )

        self.expect(
            "SYMBOL",
            "{"
        )

        body = []

        while not (
            self.current().type == "SYMBOL"
            and self.current().value == "}"
        ):
            body.append(
                self.parse_statement()
            )

        self.expect(
            "SYMBOL",
            "}"
        )

        return FunctionDefinition(
            name,
            parameters,
            body
        )

    # =====================================
    # WHEN
    # =====================================

    def parse_when(self):

        self.expect(
            "KEYWORD",
            "when"
        )

        self.expect(
            "SYMBOL",
            "("
        )

        condition = self.parse_expression()

        self.expect(
            "SYMBOL",
            ")"
        )

        self.expect(
            "SYMBOL",
            "{"
        )

        body = []

        while not (
            self.current().type == "SYMBOL"
            and self.current().value == "}"
        ):
            body.append(
                self.parse_statement()
            )

        self.expect(
            "SYMBOL",
            "}"
        )

        return WhenStatement(
            condition,
            body
        )

    # =====================================
    # LOOP
    # =====================================

        # =====================================
    # LOOP
    # =====================================

    def parse_loop(self):

        self.expect(
            "KEYWORD",
            "loop"
        )

        self.expect(
            "SYMBOL",
            "("
        )

        token = self.current()

        if token.type == "FRAME_INTERVAL":

            interval_value = token.value
            interval_type = "frame"

            self.advance()

        elif token.type == "SECOND_INTERVAL":

            interval_value = token.value
            interval_type = "second"

            self.advance()

        else:

            raise Exception(
                "Expected frame or second interval"
            )

        repeat_count = None

        if (
            self.current().type == "SYMBOL"
            and self.current().value == ","
        ):

            self.advance()

            repeat_count = self.parse_expression()

        self.expect(
            "SYMBOL",
            ")"
        )

        self.expect(
            "SYMBOL",
            "{"
        )

        body = []

        while not (
            self.current().type == "SYMBOL"
            and self.current().value == "}"
        ):

            body.append(
                self.parse_statement()
            )

        self.expect(
            "SYMBOL",
            "}"
        )

        return LoopStatement(
            interval_value,
            interval_type,
            repeat_count,
            body
        )

    def parse_import(self):

        self.expect(
            "KEYWORD",
            "import"
        )

        module = self.expect(
            "IDENTIFIER"
        ).value

        return ImportStatement(
            module
        )

    def parse_statement(self):

        token = self.current()

        if (
            token.type == "KEYWORD"
            and token.value == "func"
        ):
            return self.parse_function_definition()

        if (
            token.type == "KEYWORD"
            and token.value == "return"
        ):
            return self.parse_return()

        if (
            token.type == "KEYWORD"
            and token.value == "when"
        ):
            return self.parse_when()

        if (
            token.type == "KEYWORD"
            and token.value == "loop"
        ):
            return self.parse_loop()

        if (
            token.type == "KEYWORD"
            and token.value == "import"
        ):
            return self.parse_import()

        if (
                token.type == "IDENTIFIER"
                and
                self.peek().value == "["
        ):
            return self.parse_array_assignment()

        if (
            token.type == "IDENTIFIER"
            and self.peek().value == "="
        ):
            return self.parse_assignment()

        return self.parse_expression()

    def parse(self):

        statements = []

        while (
            self.current().type != "EOF"
        ):
            statements.append(
                self.parse_statement()
            )

        return Program(
            statements
        )