import pathlib

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day5.txt"


class Range:
    def __init__(self, line: str):
        dst, src, rng = line.strip().split(" ")
        self.dst_start = int(dst)
        self.src_start = int(src)
        self.rng = int(rng)
        self.src_end = self.src_start + self.rng

    def map_interval(self, interval: tuple[int, int]) -> tuple[int, int]:
        start, end = interval
        start = self.dst_start + (start - self.src_start)
        end = self.dst_start + (end - self.src_start)
        return start, end

    def __repr__(self):
        return f"Range({self.dst_start, self.src_start, self.src_end, self.rng})"


def parse_seed_ranges(line: str, with_ranges: bool) -> list[tuple[int, int]]:
    ints = [int(x) for x in line.split(": ")[1].split(" ")]
    if not with_ranges:
        return [(x, x + 1) for x in ints]
    else:
        ranges = [(ints[i], ints[i] + ints[i + 1]) for i in range(0, len(ints), 2)]
        return ranges


def parse_maps(maps: list[str]) -> list[list[Range]]:
    result = []
    for map in maps:
        A = []
        for line in map.split("\n")[1:]:
            A.append(Range(line))
        result.append(A)
    return result


class Ranges:
    def __init__(self, ranges: list[Range]):
        self.ranges = ranges

    def map_intervals(self, intervals: list[tuple[int, int]]):
        """
        - we assume that ranges do not overlap.
        """
        mapped_intervals = []
        for r in self.ranges:
            not_matched_intervals = []
            while intervals:
                (start, end) = intervals.pop()
                before = (start, min(r.src_start, end))
                inter = (max(r.src_start, start), min(r.src_end, end))
                after = (max(r.src_end, start), end)
                if before[1] > before[0]:
                    not_matched_intervals.append(before)
                if inter[1] > inter[0]:
                    mapped_intervals.append(r.map_interval(inter))
                if after[1] > after[0]:
                    not_matched_intervals.append(after)
            intervals = not_matched_intervals
        return mapped_intervals + intervals


def solve(lines: list[str], with_ranges: bool) -> int:
    seeds, *maps = lines
    pairs = parse_seed_ranges(seeds, with_ranges)
    ranges: list[Ranges] = [Ranges(x) for x in parse_maps(maps)]

    min_total = float("inf")
    for start, end in pairs:
        intervals = [(start, end)]
        for range in ranges:
            intervals = range.map_intervals(intervals)
        min_for_range, _ = min(intervals)
        min_total = min(min_total, min_for_range)
    return min_total


with input_file.open("r") as file:
    lines = file.read().strip().split("\n\n")
    print("P1:", solve(lines, False))
    print("P2:", solve(lines, True))
