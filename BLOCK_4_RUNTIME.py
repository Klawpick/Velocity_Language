from BLOCK_1_AST import *
from BLOCK_5_GRAPHICS import Graphics
import math
import random


class ReturnException(Exception):

    def __init__(self, value):
        self.value = value


class Runtime:

    def __init__(self):

        self.variables = {}

        self.functions = {}

        self.graphics = Graphics()

        self.imported_modules = set()

        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = -5

    # =====================================
    # EXECUTE
    # =====================================

    def execute(self, node):

        if isinstance(node, Program):

            result = None

            for statement in node.statements:
                result = self.execute(statement)

            return result

        # Ignore imports for now

        if isinstance(
                node,
                ArrayAssignment
        ):
            arr = self.variables[
                node.array
            ]

            idx = int(
                self.evaluate(
                    node.index
                )
            )

            value = self.evaluate(
                node.value
            )

            arr[idx] = value

            return value

        if isinstance(node, ImportStatement):
            filename = (
                    node.module_name
                    .replace(".", "/")
                    + ".vel"
            )

            if filename in self.imported_modules:
                return None

            self.imported_modules.add(
                filename
            )

            with open(
                    filename,
                    "r"
            ) as file:
                source = file.read()

            from BLOCK_2_LEXER import Lexer
            from BLOCK_3_PARSER import Parser

            tokens = Lexer(
                source
            ).tokenize()

            ast = Parser(
                tokens
            ).parse()

            self.execute(ast)

            return None

        # Assignment

        if isinstance(node, Assignment):

            value = self.evaluate(
                node.value
            )

            self.variables[
                node.name
            ] = value

            return value

        # Function Definition

        if isinstance(
            node,
            FunctionDefinition
        ):

            self.functions[
                node.name
            ] = node

            return None

        # Function Call

        if isinstance(
            node,
            FunctionCall
        ):

            return self.call_function(
                node
            )

        # Return

        if isinstance(
            node,
            ReturnStatement
        ):

            value = self.evaluate(
                node.value
            )

            raise ReturnException(
                value
            )

        # When

        if isinstance(
            node,
            WhenStatement
        ):

            condition = self.evaluate(
                node.condition
            )

            if condition:

                for statement in node.body:

                    self.execute(
                        statement
                    )

            return None

        # Loop

        if isinstance(
                node,
                LoopStatement
        ):

            # Frame loops

            if node.interval_type == "frame":

                if node.repeat_count is None:

                    running = True

                    while running:

                        running = (
                            self.graphics
                            .process_events()
                        )

                        for statement in node.body:
                            self.execute(
                                statement
                            )

                        self.graphics.limit_fps(
                            60
                        )

                else:

                    count = int(
                        self.evaluate(
                            node.repeat_count
                        )
                    )

                    for _ in range(count):

                        self.graphics.process_events()

                        for statement in node.body:
                            self.execute(
                                statement
                            )

                        self.graphics.limit_fps(
                            60
                        )

                return None

        raise Exception(
            f"Cannot execute {type(node)}"
        )

    # =====================================
    # EVALUATE
    # =====================================

    def evaluate(self, node):

        if isinstance(
            node,
            Number
        ):
            return node.value

        if isinstance(
            node,
            UnaryOperation
        ):

            value = self.evaluate(
                node.value
            )

            if node.operator == "-":
                return -value

            raise Exception(
                f"Unknown unary operator {node.operator}"
            )

        if isinstance(
            node,
            String
        ):
            return node.value

        if isinstance(
            node,
            Boolean
        ):
            return node.value

        if isinstance(
            node,
            Identifier
        ):

            if (
                node.name
                not in self.variables
            ):

                raise Exception(
                    f"Unknown variable: {node.name}"
                )

            return self.variables[
                node.name
            ]

        if isinstance(
            node,
            ArrayLiteral
        ):

            return [
                self.evaluate(x)
                for x in node.items
            ]

        if isinstance(
            node,
            ArrayAccess
        ):

            arr = self.evaluate(
                node.array
            )

            idx = int(
                self.evaluate(
                    node.index
                )
            )

            return arr[idx]

        if isinstance(
            node,
            BinaryOperation
        ):

            left = self.evaluate(
                node.left
            )

            right = self.evaluate(
                node.right
            )

            op = node.operator

            if op == "+":
                return left + right

            if op == "-":
                return left - right

            if op == "*":
                return left * right

            if op == "/":
                return left / right

            if op == ">":
                return left > right

            if op == "<":
                return left < right

            if op == ">=":
                return left >= right

            if op == "<=":
                return left <= right

            if op == "==":
                return left == right

            if op == "!=":
                return left != right

            raise Exception(
                f"Unknown operator {op}"
            )

        if isinstance(
            node,
            FunctionCall
        ):

            return self.call_function(
                node
            )

        raise Exception(
            f"Cannot evaluate {type(node)}"
        )
    # =====================================
    # FUNCTIONS
    # =====================================

    def call_function(self, node):

        # -----------------------------
        # log
        # -----------------------------

        if node.name == "log":

            values = [
                self.evaluate(arg)
                for arg in node.arguments
            ]

            print(*values)

            return None

        if node.name == "camera":
            self.camera_x = self.evaluate(
                node.arguments[0]
            )

            self.camera_y = self.evaluate(
                node.arguments[1]
            )

            self.camera_z = self.evaluate(
                node.arguments[2]
            )

            self.graphics.set_camera(
                self.camera_x,
                self.camera_y,
                self.camera_z
            )

            return None

        if node.name == "set_color":
            r = self.evaluate(
                node.arguments[0]
            )

            g = self.evaluate(
                node.arguments[1]
            )

            b = self.evaluate(
                node.arguments[2]
            )

            self.graphics.set_color(
                r,
                g,
                b
            )

            return None

        if node.name == "rect_collision":

            x1 = self.evaluate(node.arguments[0])
            y1 = self.evaluate(node.arguments[1])
            w1 = self.evaluate(node.arguments[2])
            h1 = self.evaluate(node.arguments[3])

            x2 = self.evaluate(node.arguments[4])
            y2 = self.evaluate(node.arguments[5])
            w2 = self.evaluate(node.arguments[6])
            h2 = self.evaluate(node.arguments[7])

            return (
                x1 < x2 + w2
                and
                x1 + w1 > x2
                and
                y1 < y2 + h2
                and
                y1 + h1 > y2
            )

        if node.name == "draw_circle":
            args = [
                self.evaluate(arg)
                for arg in node.arguments
            ]

            self.graphics.draw_circle(
                *args
            )

            return None

        # -----------------------------
        # window
        # -----------------------------

        if node.name == "window":

            title = self.evaluate(
                node.arguments[0]
            )

            width = int(
                self.evaluate(
                    node.arguments[1]
                )
            )

            height = int(
                self.evaluate(
                    node.arguments[2]
                )
            )

            self.graphics.create_window(
                title,
                width,
                height
            )

            return None
        if node.name == "key_pressed":

            key = self.evaluate(
                node.arguments[0]
            )

            return self.graphics.key_pressed(
                key
            )

        if node.name == "draw_image":

            path = self.evaluate(
                node.arguments[0]
            )

            x = self.evaluate(
                node.arguments[1]
            )

            y = self.evaluate(
                node.arguments[2]
            )

            if len(node.arguments) >= 5:

                width = self.evaluate(
                    node.arguments[3]
                )

                height = self.evaluate(
                    node.arguments[4]
                )

                self.graphics.draw_image(
                    path,
                    x,
                    y,
                    width,
                    height
                )

            else:

                self.graphics.draw_image(
                    path,
                    x,
                    y
                )

            return None

        if node.name == "play_sound":
            path = self.evaluate(
                node.arguments[0]
            )

            self.graphics.play_sound(
                path
            )

            return None

        if node.name == "mouse_x":

            return self.graphics.mouse_x()

        if node.name == "mouse_y":

            return self.graphics.mouse_y()

        if node.name == "mouse_pressed":
            button = self.evaluate(
                node.arguments[0]
            )

            return self.graphics.mouse_pressed(
                button
            )

        if node.name == "camera_rotation":
            pitch = self.evaluate(
                node.arguments[0]
            )

            yaw = self.evaluate(
                node.arguments[1]
            )

            self.graphics.set_camera_rotation(
                pitch,
                yaw
            )

            return None

        if node.name == "sin":
            return math.sin(
                self.evaluate(
                    node.arguments[0]
                )
            )

        if node.name == "cos":
            return math.cos(
                self.evaluate(
                    node.arguments[0]
                )
            )

        if node.name == "mouse_dx":
            return self.graphics.mouse_dx()

        if node.name == "mouse_dy":
            return self.graphics.mouse_dy()

        if node.name == "dt":
            return self.graphics.dt()
        # -----------------------------
        # clear_screen
        # -----------------------------

        if node.name == "clear_screen":

            self.graphics.clear_screen()

            return None

        # -----------------------------
        # present
        # -----------------------------

        if node.name == "present":

            self.graphics.present()

            return None

        if node.name == "keep_alive":

            self.graphics.keep_alive()

            return None

        # -----------------------------
        # draw_triangle
        # -----------------------------

        if node.name == "draw_triangle":

            args = [
                self.evaluate(arg)
                for arg in node.arguments
            ]

            self.graphics.draw_triangle(
                *args
            )

            return None

        # -----------------------------
        # draw_rect
        # -----------------------------

        if node.name == "draw_rect":

            args = [
                self.evaluate(arg)
                for arg in node.arguments
            ]

            self.graphics.draw_rect(
                *args
            )

            return None

        if node.name == "draw_cube":

            args = [
                self.evaluate(arg)
                for arg in node.arguments
            ]

            self.graphics.draw_cube(
                *args
            )

            return None

        if node.name == "draw_line":

            args = [
                self.evaluate(arg)
                for arg in node.arguments
            ]

            self.graphics.draw_line(
                *args
            )

            return None

        if node.name == "load_obj":
            path = self.evaluate(
                node.arguments[0]
            )

            return self.graphics.load_obj(
                path
            )

        if node.name == "draw_mesh":
            mesh = self.evaluate(
                node.arguments[0]
            )

            x = self.evaluate(
                node.arguments[1]
            )

            y = self.evaluate(
                node.arguments[2]
            )

            z = self.evaluate(
                node.arguments[3]
            )

            rot_x = self.evaluate(
                node.arguments[4]
            )

            rot_y = self.evaluate(
                node.arguments[5]
            )

            rot_z = self.evaluate(
                node.arguments[6]
            )

            scale = self.evaluate(
                node.arguments[7]
            )

            self.graphics.draw_mesh(
                mesh,
                x,
                y,
                z,
                rot_x,
                rot_y,
                rot_z,
                scale
            )

            return None

        # -----------------------------
        # draw_text
        # -----------------------------

        if node.name == "draw_text":

            text = self.evaluate(
                node.arguments[0]
            )

            x = self.evaluate(
                node.arguments[1]
            )

            y = self.evaluate(
                node.arguments[2]
            )

            self.graphics.draw_text(
                text,
                x,
                y
            )

            return None

        # -----------------------------
        # rect_collision
        # -----------------------------

        if node.name == "rect_collision":

            x1 = self.evaluate(
                node.arguments[0]
            )

            y1 = self.evaluate(
                node.arguments[1]
            )

            w1 = self.evaluate(
                node.arguments[2]
            )

            h1 = self.evaluate(
                node.arguments[3]
            )

            x2 = self.evaluate(
                node.arguments[4]
            )

            y2 = self.evaluate(
                node.arguments[5]
            )

            w2 = self.evaluate(
                node.arguments[6]
            )

            h2 = self.evaluate(
                node.arguments[7]
            )

            return (
                x1 < x2 + w2
                and
                x1 + w1 > x2
                and
                y1 < y2 + h2
                and
                y1 + h1 > y2
            )

        if node.name == "mesh_collision":
            a = self.evaluate(
                node.arguments[0]
            )

            b = self.evaluate(
                node.arguments[1]
            )

            return (

                    a["x"] < b["x"] + b["w"]
                    and
                    a["x"] + a["w"] > b["x"]

                    and

                    a["y"] < b["y"] + b["h"]
                    and
                    a["y"] + a["h"] > b["y"]

                    and

                    a["z"] < b["z"] + b["d"]
                    and
                    a["z"] + a["d"] > b["z"]

            )

        if node.name == "entity":

            return {
                "x": 0,
                "y": 0,
                "z": 0,

                "w": 1,
                "h": 1,
                "d": 1
            }

        if node.name == "clone":
            obj = self.evaluate(
                node.arguments[0]
            )

            return dict(obj)

        if node.name == "set":

            obj = self.evaluate(
                node.arguments[0]
            )

            key = self.evaluate(
                node.arguments[1]
            )

            value = self.evaluate(
                node.arguments[2]
            )

            obj[key] = value

            return None

        if node.name == "get":

            obj = self.evaluate(
                node.arguments[0]
            )

            key = self.evaluate(
                node.arguments[1]
            )

            return obj[key]

        if node.name == "has":
            obj = self.evaluate(
                node.arguments[0]
            )

            key = self.evaluate(
                node.arguments[1]
            )

            return key in obj

        # -----------------------------
        # ARRAYS
        # -----------------------------

        if node.name == "contains":
            text = str(
                self.evaluate(
                    node.arguments[0]
                )
            )

            search = str(
                self.evaluate(
                    node.arguments[1]
                )
            )

            return search in text

        if node.name == "replace":
            text = str(
                self.evaluate(
                    node.arguments[0]
                )
            )

            old = str(
                self.evaluate(
                    node.arguments[1]
                )
            )

            new = str(
                self.evaluate(
                    node.arguments[2]
                )
            )

            return text.replace(
                old,
                new
            )

        if node.name == "split":
            text = str(
                self.evaluate(
                    node.arguments[0]
                )
            )

            separator = str(
                self.evaluate(
                    node.arguments[1]
                )
            )

            return text.split(
                separator
            )

        if node.name == "save":
            filename = str(
                self.evaluate(
                    node.arguments[0]
                )
            )

            data = str(
                self.evaluate(
                    node.arguments[1]
                )
            )

            with open(
                    filename,
                    "w"
            ) as file:
                file.write(data)

            return None

        if node.name == "load":
            filename = str(
                self.evaluate(
                    node.arguments[0]
                )
            )

            with open(
                    filename,
                    "r"
            ) as file:
                return file.read()

        if node.name == "append":

            arr = self.evaluate(
                node.arguments[0]
            )

            value = self.evaluate(
                node.arguments[1]
            )

            arr.append(value)

            return None

        if node.name == "remove":

            arr = self.evaluate(
                node.arguments[0]
            )

            if len(arr) == 0:
                return None

            return arr.pop()

        if node.name == "count":

            value = self.evaluate(
                node.arguments[0]
            )

            return len(value)

        # -----------------------------
        # STRINGS
        # -----------------------------

        if node.name == "upper":

            text = self.evaluate(
                node.arguments[0]
            )

            return str(text).upper()

        if node.name == "lower":

            text = self.evaluate(
                node.arguments[0]
            )

            return str(text).lower()

        # -----------------------------
        # RANDOM
        # -----------------------------

        if node.name == "random":

            return random.random()

        if node.name == "range":

            minimum = int(
                self.evaluate(
                    node.arguments[0]
                )
            )

            maximum = int(
                self.evaluate(
                    node.arguments[1]
                )
            )

            return random.randint(
                minimum,
                maximum
            )

        # -----------------------------
        # MATH
        # -----------------------------

        if node.name == "absolute":

            value = self.evaluate(
                node.arguments[0]
            )

            return abs(value)

        if node.name == "floor":

            value = self.evaluate(
                node.arguments[0]
            )

            return math.floor(value)

        if node.name == "ceiling":

            value = self.evaluate(
                node.arguments[0]
            )

            return math.ceil(value)

        if node.name == "squareroot":

            value = self.evaluate(
                node.arguments[0]
            )

            return math.sqrt(value)

        # -----------------------------
        # TYPE
        # -----------------------------

        if node.name == "type":

            value = self.evaluate(
                node.arguments[0]
            )

            if isinstance(value, bool):
                return "boolean"

            if isinstance(value, str):
                return "string"

            if isinstance(value, list):
                return "array"

            if isinstance(value, (int, float)):
                return "number"

            if isinstance(value, dict):
                return "entity"

            return "unknown"

        # -----------------------------
        # User Functions
        # -----------------------------

        if node.name not in self.functions:

            raise Exception(
                f"Unknown function: {node.name}"
            )

        func = self.functions[
            node.name
        ]

        old_variables = dict(
            self.variables
        )

        for parameter, argument in zip(
            func.parameters,
            node.arguments
        ):

            self.variables[
                parameter
            ] = self.evaluate(
                argument
            )

        try:

            for statement in func.body:

                self.execute(
                    statement
                )

        except ReturnException as ret:

            self.variables = old_variables

            return ret.value

        self.variables = old_variables

        return None
