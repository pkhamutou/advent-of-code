import pathlib

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day10.txt"


input = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".strip()


input1 = """\
..F7.
.FJ|.
SJ.L7
|.F-J
L-J..""".strip()

input = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF""".strip()

input = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".strip()

with input_file.open("r") as file:
    input = file.read().strip()


map = input.split("\n")
ROWS = len(map)
COLS = len(map[0])


def find_start():
    for row in range(ROWS):
        for col in range(COLS):
            if map[row][col] == "S":
                return row, col


def at(row: int, col: int) -> str | None:
    if (row < 0 or row >= ROWS) or (col < 0 or col >= COLS):
        return None
    else:
        return map[row][col]


def find_start_pipe(row, col):
    down, up, right, left = (at(row + 1, col), at(row - 1, col), at(row, col + 1), at(row, col - 1))
    if down in {"|", "L", "J"}:
        if up in {"|", "F", "7"}:
            return "|"
        if right in {"-", "J", "7"}:
            return "F"
        if left in {"-", "F", "L"}:
            return "7"
    if up in {"|", "F", "7"}:
        if right in {"-", "J", "7"}:
            return "L"
        if left in {"-", "F", "L"}:
            return "J"
    if left in {"-", "F", "L"} and right in {"-", "J", "7"}:
        return "-"


def follow_loop(start_row: int, start_col: int, start_pipe: str):
    if start_pipe in {"-", "L"}:
        next_row, next_col, prev_cardinal_direction = start_row, start_col + 1, "W"  # go East/Right
    elif start_pipe in {"|", "F", "7"}:
        next_row, next_col, prev_cardinal_direction = start_row + 1, start_col, "N"  # go South/Down
    elif start_pipe == "J":
        next_row, next_col, prev_cardinal_direction = start_row - 1, start_col, "S"  # go North/Up

    maze = [[0] * COLS for _ in range(ROWS)]

    loop = True
    steps = 0
    prev = prev_cardinal_direction  # what a long name!

    while loop:
        pipe = at(next_row, next_col)
        maze[next_row][next_col] = 1

        if pipe == "S":
            loop = False
        elif pipe == "F":
            if prev == "E":
                next_row += 1
                prev = "N"
            elif prev == "S":
                next_col += 1
                prev = "W"
            else:
                raise Exception(f"{steps=} {pipe=} {next_row=} {next_col=} {prev=}")
        elif pipe == "7":
            if prev == "W":
                next_row += 1
                prev = "N"
            elif prev == "S":
                next_col -= 1
                prev = "E"
            else:
                raise Exception(f"{steps=} {pipe=} {next_row=} {next_col=} {prev=}")
        elif pipe == "J":
            if prev == "N":
                next_col -= 1
                prev = "E"
            elif prev == "W":
                next_row -= 1
                prev = "S"
            else:
                raise Exception(f"{steps=} {pipe=} {next_row=} {next_col=} {prev=}")
        elif pipe == "L":
            if prev == "E":
                next_row -= 1
                prev = "S"
            elif prev == "N":
                next_col += 1
                prev = "W"
            else:
                raise Exception(f"{steps=} {pipe=} {next_row=} {next_col=} {prev=}")
        elif pipe == "|":
            if prev == "N":
                next_row += 1
                prev = "N"
            elif prev == "S":
                next_row -= 1
                prev = "S"
            else:
                raise Exception(f"{steps=} {pipe=} {next_row=} {next_col=} {prev=}")
        elif pipe == "-":
            if prev == "E":
                next_col -= 1
                prev = "E"
            elif prev == "W":
                next_col += 1
                prev = "W"
            else:
                raise Exception(f"{steps=} {pipe=} {next_row=} {next_col=} {prev=}")
        else:
            raise Exception(f"{steps=} {pipe=} {next_row=} {next_col=} {prev=}")
        steps += 1

    print(steps)
    print(input)
    for row in maze:
        print("".join(str(x) for x in row))

    print(count_enclosed_tiles(maze, start_pipe))


def count_enclosed_tiles(maze: list[list[int]], start_pipe: str) -> int:
    total_count = 0
    for row_id in range(ROWS):
        for col_id in range(COLS):
            if maze[row_id][col_id] == 0:
                row = map[row_id]
                cnt = 0
                stack = []
                for i in filter(lambda i: maze[row_id][i] == 1, range(col_id + 1, COLS)):
                    c = row[i]
                    c = start_pipe if c == "S" else c
                    if c == "-":
                        cnt += 0
                    elif c == "|":
                        cnt += 1
                    elif c == "F":
                        stack.append("F")
                    elif c == "L":
                        stack.append("L")
                    elif c == "J":
                        prev = stack.pop()
                        if prev == "F":
                            cnt += 1
                        elif prev == "L":
                            cnt += 0
                    elif c == "7":
                        prev = stack.pop()
                        if prev == "F":
                            cnt += 0
                        elif prev == "L":
                            cnt += 1
                    elif c == ".":
                        cnt += 0
                assert not stack, f"{stack=} {row=} {col_id=}"
                if cnt % 2 == 1:
                    total_count += 1
    return total_count


start_row, start_col = find_start()
print(start_row, start_col)
start_pipe = find_start_pipe(start_row, start_col)
print(start_pipe)
follow_loop(start_row, start_col, start_pipe)
