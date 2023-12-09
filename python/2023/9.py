import pathlib

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day9.txt"


input = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".strip()


def extrapolate_history(line: str) -> list[list[int]]:
    step = [int(x) for x in line.split(" ")]
    steps: list[list[int]] = [step]

    for _ in range(len(step) - 1):
        step = steps[-1]
        next_step = [step[i] - step[i - 1] for i in range(1, len(step))]
        if all(x == 0 for x in next_step):
            return steps
        else:
            steps.append(next_step)
    return steps


def predict_next_value(line: str) -> int:
    steps = extrapolate_history(line)
    return sum(x[-1] for x in steps)


def predict_prev_value(line: str) -> int:
    steps = extrapolate_history(line)
    val = 0
    for step in reversed(steps):
        val = step[0] - val
    return val


lines = input.split("\n")
print(sum(predict_next_value(line.strip()) for line in lines))
print(sum(predict_prev_value(line.strip()) for line in lines))


with input_file.open("r") as file:
    lines = file.read().strip().split("\n")
    print("P1:", sum(predict_next_value(line.strip()) for line in lines))
    print("P2:", sum(predict_prev_value(line.strip()) for line in lines))
