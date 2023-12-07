import pathlib
import time as c

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day6.txt"

input = """\
Time:      7  15   30
Distance:  9  40  200
"""


def parse(lines: list[str], with_kerning: bool) -> list[tuple[int, int]]:
    time = lines[0].split(":")[1]
    dist = lines[1].split(":")[1]
    if with_kerning:
        time = [int(time.replace(" ", ""))]
        dist = [int(dist.replace(" ", ""))]
    else:
        time = [int(x) for x in time.split(" ") if x]
        dist = [int(x) for x in dist.split(" ") if x]
    pairs = zip(time, dist)
    return list(pairs)


def solve2(pairs: list[tuple[int, int]]) -> int:
    result = 1
    s = c.time()
    for time, dist in pairs:
        cnt = 0
        for ms in range(time + 1):
            d = (time - ms) * ms
            if d > dist:
                cnt += 1
        result *= cnt
    print(f"{c.time() - s:.3f} seconds")
    return result


def solve(pairs: list[tuple[int, int]]) -> int:
    result = 1
    s = c.time()
    for time, dist in pairs:
        start, end = 0, 0
        for ms in range(time + 1):
            d = (time - ms) * ms
            if d > dist:
                start = ms
                break
        for ms in reversed(range(time + 1)):
            d = (time - ms) * ms
            if d > dist:
                end = ms
                break
        result *= end + 1 - start
    print(f"{c.time() - s:.3f} seconds")
    return result


with input_file.open("r") as file:
    lines = file.readlines()
    print("P1:", solve(parse(lines, False)))
    print("P2:", solve(parse(lines, True)))
