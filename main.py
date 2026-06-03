from BLOCK_2_LEXER import Lexer
from BLOCK_3_PARSER import Parser
from BLOCK_4_RUNTIME import Runtime

import re

file_name = input("File name (.vel): ").strip()

if not re.match(r"^[a-zA-Z0-9_\-]+$", file_name):
    print("Invalid file name.")
    quit()

file_name += ".vel"

try:
    with open(file_name, "r") as file:
        source = file.read()

except FileNotFoundError:
    print(f"'{file_name}' does not exist.")
    quit()

print("===== SOURCE =====")

print(source)

print("\n===== TOKENS =====")

tokens = Lexer(source).tokenize()

for token in tokens:
    print(token)

print("\n===== PARSING =====")

parser = Parser(tokens)

ast = parser.parse()

print("AST Created Successfully")

print("\n===== EXECUTION =====")

runtime = Runtime()

runtime.execute(ast)

print("\n===== DONE =====")
