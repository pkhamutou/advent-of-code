import pathlib

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / 'input' / 'day1.txt'


digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def extract_digits(line: str) -> int:
    values = []

    for i, c in enumerate(line):
        if c.isdigit():
            values.append(int(c))
        else:
            sub_str = line[i:]
            for d, digit in enumerate(digits, 1):
                if sub_str.startswith(digit):
                    values.append(d)

    return (values[0] * 10) + values[-1] if values else 0


with input_file.open("r") as file:
    lines = file.readlines()
    result = sum((extract_digits(line) for line in lines))
    print(result)

