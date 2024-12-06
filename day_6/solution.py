import copy
from collections import namedtuple, defaultdict

GUARD_SYMBOL = "^"
OBSTRUCTION_SYMBOL = "#"
ROTATION_DEGREES = 90

MapLocation = namedtuple('MapLocation', ['x', 'y'])


def find_initial_guard_location(puzzle: list[list[str]]) -> MapLocation:
    for y, row in enumerate(puzzle):
        if GUARD_SYMBOL in row:
            x = row.index(GUARD_SYMBOL)
            return MapLocation(x, y)


def predict_guard_route(puzzle: list[list[str]],
                        guard_location: MapLocation,
                        track_obstructions: bool = False,
                        experimental_obstruction_location: MapLocation | None = None):
    distinct_positions = set()
    current_rotation = 0
    obstructions = defaultdict(int)
    rotation_to_next_location = {
        ROTATION_DEGREES * 0: lambda guard_location: MapLocation(guard_location.x, guard_location.y - 1),
        ROTATION_DEGREES * 1: lambda guard_location: MapLocation(guard_location.x + 1, guard_location.y),
        ROTATION_DEGREES * 2: lambda guard_location: MapLocation(guard_location.x, guard_location.y + 1),
        ROTATION_DEGREES * 3: lambda guard_location: MapLocation(guard_location.x - 1, guard_location.y)
    }
    while not guard_leaving_map(puzzle, guard_location):
        next_potential_guard_location = rotation_to_next_location[current_rotation](guard_location)
        if puzzle[next_potential_guard_location.y][next_potential_guard_location.x] != OBSTRUCTION_SYMBOL:
            guard_location = next_potential_guard_location
            distinct_positions.add(guard_location)
        else:
            current_rotation = (current_rotation + ROTATION_DEGREES) % (4 * ROTATION_DEGREES)
            if track_obstructions:
                obstructions[(current_rotation, next_potential_guard_location)] += 1
                if obstructions[(current_rotation, experimental_obstruction_location)] > 1:
                    return -1
        # for debugging on the test
        # print(f"***STEP {len(distinct_positions)} TAKEN***")
        # puzzle[guard_location.y][guard_location.x] = "X"
        # display_puzzle(puzzle)
    return distinct_positions


def guard_leaving_map(puzzle: list[list[str]], guard_location: MapLocation) -> bool:
    x, y = guard_location
    return y >= len(puzzle) - 1 or x >= len(puzzle[0]) - 1 or y < 0 or x < 0


def find_obstruction_locations_to_cause_loops(puzzle: list[list[str]], guard_location: MapLocation, original_guard_route: set[MapLocation]):
    number_of_obstruction_locations = 0
    for location in original_guard_route:
        if location != guard_location:
            test_puzzle = copy.deepcopy(puzzle)
            test_puzzle[location.y][location.x] = OBSTRUCTION_SYMBOL
            if predict_guard_route(test_puzzle, guard_location, True, location) == -1:
                number_of_obstruction_locations += 1
    return number_of_obstruction_locations


def display_puzzle(puzzle: list[str]):
    print(*puzzle, sep=f"\n")


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        lines = map(str.split, fp.readlines())
        puzzle = [list(line[0]) for line in lines]
        guard_location = find_initial_guard_location(puzzle)
        guard_route = predict_guard_route(puzzle, guard_location)
        print(len(guard_route))
        print(find_obstruction_locations_to_cause_loops(puzzle, guard_location, guard_route))
