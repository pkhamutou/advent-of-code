import pathlib
import functools

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day12.txt"

input = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".strip()


def parse(lines: list[str], unfold_factor: int) -> list[tuple[str, list[int]]]:
    result = []
    for line in lines:
        springs, groups = line.split(" ")
        springs = "?".join([springs] * unfold_factor)
        groups = [int(x) for x in groups.split(",")] * unfold_factor
        result.append((springs, groups))
    return result


def count_arrangments(springs: str, groups: list[int]) -> int:
    S = len(springs)
    G = len(groups)

    @functools.cache
    def count(spring_id: int, group_id: int, cur: int) -> int:
        if spring_id == S:
            if group_id == G and cur == 0:
                return 1
            elif group_id == G - 1 and groups[group_id] == cur:
                return 1
            else:
                return 0

        cnt = 0
        for c in (".", "#"):
            if springs[spring_id] == c or springs[spring_id] == "?":
                if c == "." and cur == 0:
                    cnt += count(spring_id + 1, group_id, 0)
                elif c == "." and cur > 0 and group_id < G and groups[group_id] == cur:
                    cnt += count(spring_id + 1, group_id + 1, 0)
                elif c == "#":
                    cnt += count(spring_id + 1, group_id, cur + 1)
        return cnt

    return count(0, 0, 0)


def solve(lines: list[str], unfold_factor=1):
    parsed = parse(lines, unfold_factor)
    return sum(count_arrangments(springs, groups) for springs, groups in parsed)


print("E1:", solve(input.splitlines(), 1))
print("E2:", solve(input.splitlines(), 5))

with input_file.open("r") as file:
    lines = file.read().strip().split("\n")
    print("P1:", solve(lines, 1))
    print("P2:", solve(lines, 5))
