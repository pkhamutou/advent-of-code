import pathlib
import math
import itertools

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day8.txt"

input = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".strip()

input2 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".strip()


def parse(lines: list[str]):
    instructions: list[int] = [0 if i == "L" else 1 for i in lines[0]]
    d = {}
    for line in lines[2:]:
        element, lrs = line.strip().split(" = ")
        l = lrs[1:4]
        r = lrs[6:9]
        d[element] = (l, r)
    return instructions, d


def solvep1(instructions: list[int], d: dict[str, tuple[str, str]]) -> int:
    cur = "AAA"
    for cnt, idx in enumerate(itertools.cycle(instructions)):
        if cur == "ZZZ":
            return cnt
        cur = d[cur][idx]


def solvep2(instructions: list[int], d: dict[str, tuple[str, str]]) -> int:
    curs = [k for k in d if k.endswith("A")]
    multiples = {}

    for cnt, idx in enumerate(itertools.cycle(instructions)):
        for i, c in enumerate(curs):
            curs[i] = d[c][idx]
            if curs[i].endswith("Z"):
                multiples[i] = cnt + 1

        if len(multiples) == len(curs):
            return math.lcm(*multiples.values())


print(solvep1(*parse(input.splitlines())))
print(solvep2(*parse(input2.splitlines())))


with input_file.open("r") as file:
    lines = file.read().strip().split("\n")
    instructions, d = parse(lines)
    print("P1:", solvep1(instructions, d))
    print("P2:", solvep2(instructions, d))
