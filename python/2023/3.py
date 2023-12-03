from __future__ import annotations
import pathlib
from dataclasses import dataclass

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / 'input' / 'day3.txt'

input1 = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".strip()

input2 = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".strip()


@dataclass
class Element:
    start: int
    end: int
    val: str

    def is_part_number(self) -> bool:
        return not self.is_symbol()

    def is_symbol(self) -> bool:
        return self.start == self.end and not self.val.isdigit()

    def is_star(self) -> bool:
        return self.val == "*"

    @property
    def part_number(self) -> int:
        return int(self.val)

    def overlap(self, index: int) -> bool:
        return self.start - 1 <= index and self.end + 1 >= index

    def is_adjacent(self, symbols: list[Element]) -> bool:
        return any(self.overlap(s.start) for s in symbols)

    def adjacent_by(self, parts: list[Element]) -> tuple[Element, Element] | None:
        i = 0
        while i < len(parts) - 1:
            if parts[i].overlap(self.start) and parts[i + 1].overlap(self.start):
                return parts[i], parts[i + 1]
            i += 1
        return None


@dataclass
class Line:
    line_id: int
    elements: list[Element]
    raw: str = ""

    def symbols(self) -> list[Element]:
        return [s for s in self.elements if s.is_symbol()]

    def parts(self) -> list[Element]:
        return [s for s in self.elements if s.is_part_number()]

    def stars(self) -> list[Element]:
        return [s for s in self.elements if s.is_star()]


@dataclass
class Schematic:
    lines: list[Line]

    def get_by_id(self, id: int, f=None):
        if id < 0 or id >= len(self.lines):
            return []
        else:
            return f(self.lines[id]) if f else self.lines[id]

    def sum_part_numbers(self) -> int:
        sum_of_parts = 0
        line_id = 0
        while line_id < len(self.lines):
            prev_symbols = self.get_by_id(line_id - 1, lambda x: x.symbols())
            cur_line = self.lines[line_id]
            next_symbols = self.get_by_id(line_id + 1, lambda x: x.symbols())
            symbols = prev_symbols + cur_line.symbols() + next_symbols

            for part in cur_line.parts():
                if part.is_adjacent(symbols):
                    sum_of_parts += part.part_number

            line_id += 1
        return sum_of_parts

    def get_gear_ratio(self) -> int:
        gear_ratio = 0
        line_id = 0
        while line_id < len(self.lines):
            prev_parts = self.get_by_id(line_id - 1, lambda x: x.parts())
            cur_line = self.lines[line_id]
            next_parts = self.get_by_id(line_id + 1, lambda x: x.parts())
            parts = sorted(prev_parts + cur_line.parts() + next_parts, key=lambda x: (x.start, x.end))

            for star in cur_line.stars():
                if adjacents := star.adjacent_by(parts):
                    a, b = adjacents
                    gear_ratio = gear_ratio + (a.part_number * b.part_number)
            line_id += 1
        return gear_ratio


def parse_elements(line: str) -> list[Element]:
    res = []
    val = ""
    for i, c in enumerate(line):
        if c == "." or c == "\n":
            if val:
                res.append(Element(i - len(val), i - 1, val))
                val = ""
        elif not c.isdigit():
            if val:
                res.append(Element(i - len(val), i - 1, val))
                val = ""
            res.append(Element(i, i, c))
        else:
            val += c

    return res


def parse(lines: list[str]) -> Schematic:
    slines = []
    for line_id, line in enumerate(lines):
        pline = Line(line_id, parse_elements(line), line.strip())
        slines.append(pline)
    schematic = Schematic(slines)
    return schematic


print("input1:", parse(input1.splitlines()).sum_part_numbers(), "  expected: 4361")
print("input2:", parse(input2.splitlines()).get_gear_ratio(), "expected: 467835")

with open(input_file, "r") as file:
    lines = file.readlines()
    print("Part 1:", parse(lines).sum_part_numbers())
    print("Part 2:", parse(lines).get_gear_ratio())


