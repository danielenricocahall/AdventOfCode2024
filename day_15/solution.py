import itertools
from dataclasses import dataclass

WALL = "#"
BOX = "O"
ROBOT = "@"


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)


def build_map_and_movements(lines: list[str]) -> tuple[list[list[str]], str]:
    map_from_lanternfish = []
    movements = ""
    finished_with_map: bool = False
    for line in map(str.strip, lines):
        if not line:
            finished_with_map = True
            continue
        if not finished_with_map:
            map_from_lanternfish.append(list(line))
        else:
            movements += line
    return map_from_lanternfish, movements


def move_boxes(map_from_lanternfish: list[list[str]], movements: str):
    MOVEMENT_TO_POSITION_MAPPING = {
        '^': Position(0, -1),
        'v': Position(0, 1),
        '>': Position(1, 0),
        '<': Position(-1, 0)

    }

    def apply_movement(map_from_lanternfish: list[list[str]], position: Position, movement: str):
        next_potential_position = position + MOVEMENT_TO_POSITION_MAPPING[movement]
        if map_from_lanternfish[next_potential_position.y][next_potential_position.x] == WALL:
            return False
        elif map_from_lanternfish[next_potential_position.y][next_potential_position.x] == BOX:
            if apply_movement(map_from_lanternfish, next_potential_position, movement):
                map_from_lanternfish[next_potential_position.y][next_potential_position.x], \
                map_from_lanternfish[position.y][position.x] = \
                    map_from_lanternfish[position.y][position.x], map_from_lanternfish[next_potential_position.y][
                        next_potential_position.x]
                return True
        else:
            map_from_lanternfish[next_potential_position.y][next_potential_position.x], map_from_lanternfish[position.y][position.x] = \
                map_from_lanternfish[position.y][position.x], map_from_lanternfish[next_potential_position.y][next_potential_position.x]

            return True
    print("Initial State")
    display_map(map_from_lanternfish)
    current_robot_position = get_initial_position_of_robot(map_from_lanternfish)
    for movement in movements:
        print(f"Move {movement}")
        if apply_movement(map_from_lanternfish, current_robot_position, movement):
            current_robot_position += MOVEMENT_TO_POSITION_MAPPING[movement]
        display_map(map_from_lanternfish)


def get_initial_position_of_robot(map_from_lanternfish: list[list[str]]) -> Position:
    rows = len(map_from_lanternfish)
    cols = len(map_from_lanternfish[0])
    initial_position = next(
        (i, j) for i, j in itertools.product(range(rows), range(cols)) if map_from_lanternfish[i][j] == ROBOT)
    return Position(*initial_position)


def calculate_gps(map_from_lanternfish: list[list[str]]) -> int:
    gps = 0
    rows = len(map_from_lanternfish)
    cols = len(map_from_lanternfish[0])
    for i in range(rows):
        for j in range(cols):
            if map_from_lanternfish[i][j] == BOX:
                gps = gps + (100 * i) + j
    return gps



def display_map(map_from_lanternfish: list[list[str]]):
    print(*["".join(x) for x in map_from_lanternfish], sep='\n')
    print('\n')





if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        map_from_lanternfish, movements = build_map_and_movements(fp.readlines())
        move_boxes(map_from_lanternfish, movements)
        print(calculate_gps(map_from_lanternfish))
