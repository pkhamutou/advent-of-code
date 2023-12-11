import pathlib
import itertools

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / "input" / "day11.txt"


input = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".strip()


class Image:
    def __init__(self, lines: list[str], scale: int = 2):
        num = 1
        plot = []
        for line in lines:
            row = []
            for c in line.strip():
                if c == "#":
                    row.append(str(num))
                    num += 1
                else:
                    row.append(c)
            plot.append(row)
        self.plot = plot
        self.scale = scale
        self.ROWS = len(self.plot)
        self.COLS = len(self.plot[0])
        self.last_galaxy_id = num - 1

    def print(self):
        print(self.coords)
        for row in self.plot:
            print("".join(row))

    def with_expanded(self):
        self.empty_rows = [i for i, row in enumerate(self.plot) if all(x == "." for x in row)]
        self.empty_cols = [i for i in range(self.COLS) if all(row[i] == "." for row in self.plot)]
        return self

    def with_coordinates(self):
        coords = {}
        for row_id in range(self.ROWS):
            for col_id in range(self.COLS):
                d = self.plot[row_id][col_id]
                if d.isdigit():
                    coords[int(d)] = (row_id, col_id)
        self.coords = coords
        return self

    def get_sum_of_lengths(self):
        sum_of_lengths = 0
        for a, b in itertools.combinations(range(1, self.last_galaxy_id + 1), 2):
            ax, ay = self.coords[a]
            bx, by = self.coords[b]
            x_dist = abs(ax - bx)
            y_dist = abs(ay - by)

            dist = x_dist + y_dist
            min_x, max_x = (ax, bx) if ax < bx else (bx, ax)
            min_y, max_y = (ay, by) if ay < by else (by, ay)

            extra_rows = sum(1 for x in self.empty_rows if x > min_x and x < max_x)
            if extra_rows:
                extra_rows = (extra_rows * self.scale) - extra_rows

            extra_cols = sum(1 for x in self.empty_cols if x > min_y and x < max_y)
            if extra_cols:
                extra_cols = (extra_cols * self.scale) - extra_cols

            sum_of_lengths += dist + extra_cols + extra_rows
        return sum_of_lengths


img = Image(input.splitlines(), 2).with_expanded().with_coordinates()
print("Ex:", img.get_sum_of_lengths())

with input_file.open("r") as file:
    lines = file.read().strip().split("\n")
    img = Image(lines, 2).with_expanded().with_coordinates()
    print("P1:", img.get_sum_of_lengths())
    img = Image(lines, 1_000_000).with_expanded().with_coordinates()
    print("P2:", img.get_sum_of_lengths())
