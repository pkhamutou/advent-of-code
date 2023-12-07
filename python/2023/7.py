import pathlib
import enum
from functools import total_ordering
from collections import Counter

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day7.txt"

input = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

strengths = {
    "A": 12,
    "K": 11,
    "Q": 10,
    "J": 9,
    "T": 8,
    "9": 7,
    "8": 6,
    "7": 5,
    "6": 4,
    "5": 3,
    "4": 2,
    "3": 1,
    "2": 0,
}


class Rank(enum.IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_KING = 5
    FIVE_OF_KING = 6


def get_rank(c: Counter) -> Rank:
    if len(c) == 5:
        return Rank.HIGH_CARD
    elif len(c) == 4:
        return Rank.ONE_PAIR
    elif len(c) == 3:
        return Rank.THREE_OF_KIND if 3 in c.values() else Rank.TWO_PAIR
    elif len(c) == 2:
        return Rank.FOUR_OF_KING if 4 in c.values() else Rank.FULL_HOUSE
    else:
        return Rank.FIVE_OF_KING


def get_rank_with_joker(pair: str) -> Rank:
    c = Counter(pair)
    if len(c) == 1:
        return Rank.FIVE_OF_KING
    elif jc := c.get("J"):
        most_common = [a for a, _ in c.most_common(2) if a != "J"][0]
        replaced = pair.replace("J", most_common)
        return get_rank(Counter(replaced))
    else:
        return get_rank(c)


class Hand:
    def __init__(self, pair: str, bid: int, with_joker: bool):
        self.pair = pair
        self.bid = bid
        self.rank = get_rank_with_joker(pair) if with_joker else get_rank(Counter(pair))
        self.strenghts = strengths | {"J": -1} if with_joker else strengths

    def __lt__(self, other) -> bool:
        if self.rank == other.rank:
            for a, b in zip(self.pair, other.pair):
                if self.strenghts[a] < self.strenghts[b]:
                    return True
                elif self.strenghts[a] > self.strenghts[b]:
                    return False
            return False
        else:
            return self.rank < other.rank

    def __repr__(self):
        return f"Hand({self.pair}, {self.bid})"


def parse(lines: list[str], with_joker: bool) -> list[Hand]:
    hands = []
    for line in lines:
        pair, bid = line.strip().split(" ")
        hands.append(Hand(pair, int(bid), with_joker))
    return hands


def solve(hands: list[Hand]) -> int:
    return sum((hand.bid * rank) for rank, hand in enumerate(sorted(hands), 1))


with input_file.open("r") as file:
    lines = file.readlines()
    print("P1:", solve(parse(lines, False)))
    print("P2:", solve(parse(lines, True)))
