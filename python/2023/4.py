from __future__ import annotations
import pathlib
import functools
from dataclasses import dataclass

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day4.txt"

input1 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".strip()

input2 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".strip()


@dataclass
class Card:
    id: int
    matching_nums: int
    copies: int = 1


def parse_line(line: str) -> tuple[list[str], set[str]]:
    _, points = line.split(": ")
    winning, guessed = points.split(" | ")
    return [n for n in winning.split(" ") if n], {n for n in guessed.split(" ") if n}


def get_matching_numbers(nums: tuple[list[str], set[str]]):
    winning, guessed = nums
    return [x for x in winning if x in guessed]


def total_points(nums: tuple[list[str], set[str]]) -> int:
    return functools.reduce(lambda points, _: points * 2 or 1, get_matching_numbers(nums), 0)


def get_total_points(lines: list[str]):
    total_sum = sum(total_points(parse_line(line.strip())) for line in lines)
    return total_sum


print(get_total_points(input1.splitlines()), "expected: 13")

with input_file.open("r") as file:
    print(get_total_points(file.readlines()))


def process_scratchcards(lines: list[str]):
    cards = []

    for i, line in enumerate(lines):
        pline = parse_line(line.strip())
        card = Card(i, len(get_matching_numbers(pline)))
        cards.append(card)

    result = count_cards(cards)
    return result


def count_cards(cards: list[Card]) -> int:
    result = 0
    length = len(cards)
    for card in cards:
        next_ids = range(card.id + 1, min(length, card.id + 1 + card.matching_nums))
        for _ in range(card.copies):
            result += 1
            for id in next_ids:
                cards[id].copies += 1
    return result


print(process_scratchcards(input2.splitlines()), "expected: 30")

with input_file.open("r") as file:
    print(process_scratchcards(file.readlines()))
