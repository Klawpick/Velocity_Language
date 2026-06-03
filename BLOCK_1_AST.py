# ==================================================
# VELOCITY BLOCK 1 - AST SYSTEM
# ==================================================

# ------------------------------
# Base Node
# ------------------------------

class Node:
    pass


# ==================================================
# PROGRAM
# ==================================================

class Program(Node):
    def __init__(self, statements):
        self.statements = statements


# ==================================================
# EXPRESSIONS
# ==================================================

class Number(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Boolean(Node):
    def __init__(self, value):
        self.value = value


class Identifier(Node):
    def __init__(self, name):
        self.name = name


class UnaryOperation(Node):
    def __init__(self, operator, value):
        self.operator = operator
        self.value = value

class ArrayLiteral(Node):
    def __init__(self, items):
        self.items = items


# ==================================================
# OPERATIONS
# ==================================================

class BinaryOperation(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


# ==================================================
# VARIABLES
# ==================================================

class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value


# ==================================================
# FUNCTIONS
# ==================================================

class FunctionDefinition(Node):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body


class FunctionCall(Node):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class ReturnStatement(Node):
    def __init__(self, value):
        self.value = value


# ==================================================
# CONTROL FLOW
# ==================================================

class WhenStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class LoopStatement(Node):

    def __init__(
        self,
        interval_value,
        interval_type,
        repeat_count,
        body
    ):
        self.interval_value = interval_value
        self.interval_type = interval_type
        self.repeat_count = repeat_count
        self.body = body


# ==================================================
# IMPORTS
# ==================================================

class ImportStatement(Node):
    def __init__(self, module_name):
        self.module_name = module_name
        
class ArrayAccess(Node):
    def __init__(self, array, index):
        self.array = array
        self.index = index

class ArrayAssignment(Node):
    def __init__(
        self,
        array,
        index,
        value
    ):
        self.array = array
        self.index = index
        self.value = value