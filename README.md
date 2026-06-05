## **Velocity** 

Velocity is a programming language built for making games. 

The project started as a way to learn how programming languages work and gradually grew into a language with its own lexer, parser, runtime, graphics system, audio support, input handling, and basic 3D rendering. 

Velocity is currently focused on game development and engine features while remaining easy to read and write. 

3D model Demo 
<img width="1192" height="888" alt="1448cd72-91c2-4373-9ce4-e3fa96fd2101" src="https://github.com/user-attachments/assets/51795d64-1eb2-4c9e-9314-37c1a5a1bcf5" />

## **Features** 

• Variables • Functions • Arrays • Conditional execution ( `when` ) • Loops • Keyboard input • Mouse input • Audio playback • 2D graphics • Text rendering • Image rendering • 3D cube rendering • OBJ model loading • Flat-shaded mesh rendering • FPS camera controls • Entity system • Collision detection 

## **Installation** 

Install pygame: 

```
pip install pygame
```

1 

Run Velocity: 

```
main.py
```

When prompted: 

```
File name (.vel): hello_world
```

Velocity will automatically load: 

```
hello_world.vel
```

## **Language Syntax** 

## **Variables** 

```
score = 100
player_name = "Velocity"
alive = true
```

## **Math** 

```
x = 5 + 3
y = x * 2
z = (y + 10) / 4
```

## **Arrays** 

```
numbers = [1, 2, 3]
log(numbers[0])
numbers[1] = 50
```

## **Functions** 

```
func add(a, b)
{
```

2 

```
    return a + b
}
result = add(10, 20)
log(result)
```

## **Conditions** 

```
when (score > 50)
{
    log("You win!")
}
```

## **Loops** 

Run every frame: 

```
loop(1f)
{
    log("Running")
}
```

Run for a fixed number of frames: 

```
loop(1f, 60)
{
    log("One second at 60 FPS")
}
```

## **Graphics** 

Create a window: 

```
window("My Game", 800, 600)
```

Draw a rectangle: 

3 

```
set_color(255, 0, 0)
draw_rect(
    100,
    100,
    200,
    100
)
```

Draw text: 

```
draw_text(
    "Hello World!",
    331,
    285
)
```

Draw a circle: 

```
draw_circle(
    400,
    300,
    50
)
```

## **3D Rendering** 

Load and draw an OBJ model: 

```
mesh = load_obj("skull.obj")
loop(1f)
{
    clear_screen()
    draw_mesh(
        mesh,
        0,
        0,
        8,
        0,
```

4 

```
        0,
        0,
        1
    )
    present()
}
```

## **Example Programs** 

## **hello_world.vel** 

Basic text rendering example. 

## **3dmodelDEMO.vel** 

Loads and renders a 3D OBJ model. 

## **fps.vel** 

Demonstrates first-person camera controls using mouse look and keyboard movement. 

## **Project Structure** 

```
main.py               Entry point
BLOCK_1_AST.py        AST system
BLOCK_2_LEXER.py      Lexer
BLOCK_3_PARSER.py     Parser
BLOCK_4_RUNTIME.py    Runtime / Interpreter
BLOCK_5_GRAPHICS.py   Graphics Engine
BLOCK_6_IMPORTS.py    Planned
BLOCK_7_STDLIB.py     Planned
BLOCK_8_COMPILER.py   Planned
```

## **Current Status** 

Velocity is currently in active development. 

5 

The core interpreter, graphics system, input handling, and 3D rendering pipeline are functional and being expanded with additional game-development features. 

## **Roadmap** 

## **Next** 

- Gravity • Jumping • draw_entity() 

## **Future** 

- Simple enemy AI 

- Raycast weapons 

- Expanded standard library 

- Improved module system 

- Compiler research

## Standard Library

### Arrays

```velocity
items = [1, 2, 3]

append(items, 4)

log(count(items))

remove(items)
```

Available functions:

```velocity
append(arr, value)
remove(arr)
count(arr)
```

### Strings

```velocity
text = "Velocity"

log(upper(text))
log(lower(text))
```

Available functions:

```velocity
upper(text)
lower(text)
contains(text, search)
replace(text, old, new)
split(text, separator)
```

### Random

```velocity
log(random())

log(range(1, 10))
```

Available functions:

```velocity
random()
range(min, max)
```

### Math

```velocity
log(absolute(-25))

log(floor(5.9))

log(ceiling(5.1))

log(squareroot(144))
```

Available functions:

```velocity
absolute(x)
floor(x)
ceiling(x)
squareroot(x)
```

### Type Information

```velocity
log(type(123))
log(type("hello"))
log(type(true))
```

Available function:

```velocity
type(value)
```

### File Storage

```velocity
save(
    "score.txt",
    "500"
)

score = load(
    "score.txt"
)
```

Available functions:

```velocity
save(file, data)
load(file)
```


## **License** 

MIT License 

6 

