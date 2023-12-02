import pathlib
from dataclasses import dataclass

root = pathlib.Path(__file__).parent.parent.parent
input_file = root / 'input' / 'day2.txt'


@dataclass
class SetOfCubes:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    id: int
    sets: list[SetOfCubes]

    def power(self) -> int:
        reds = max((x.red for x in self.sets))
        greens = max((x.green for x in self.sets))
        blues = max((x.blue for x in self.sets))
        return reds * greens * blues


RED = "red"
GREEN = "green"
BLUE = "blue"
OFFSET = len("Game ")


def parse(line: str) -> Game:
    colon_index = line.index(":", 0)
    game_id = int(line[OFFSET:colon_index])
    sets = line[colon_index+2:].split("; ")
    psets = []
    for s in sets:
        cubes = SetOfCubes(0, 0, 0)
        for c in s.split(", "):
            val =  int(c[0:c.index(" ")])
            if RED in c:
                cubes.red = val
            elif GREEN in c:
                cubes.green = val
            elif BLUE in c:
                cubes.blue = val
        psets.append(cubes)
    return Game(game_id, psets)


def is_game_possible(game: Game) -> bool:
    reds, greens, blues = 12, 13, 14
    for cubes in game.sets:
        if cubes.red > reds or cubes.green > greens or cubes.blue > blues:
            return False
    return True


def sum_game_ids(lines: list[str]) -> int:
    id_sum = 0
    power_sum = 0
    for line in lines:
        game = parse(line)
        power_sum += game.power()
        if is_game_possible(game):
            id_sum += game.id
    return id_sum, power_sum


with input_file.open("r") as file:
    lines = file.readlines()
    id_sum, power_sum = sum_game_ids(lines)
    print(f"{id_sum=} {power_sum=}")
