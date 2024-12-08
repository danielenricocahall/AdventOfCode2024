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


def predict_guard_route(puzzle: list[list[str]], guard_location: MapLocation, experimental_obstruction_location=None):
    distinct_positions = set()
    visited_states = set()  # Tracks (direction, position)
    current_rotation = 0
    rotation_to_next_location = {
        ROTATION_DEGREES * 0: lambda loc: MapLocation(loc.x, loc.y - 1),
        ROTATION_DEGREES * 1: lambda loc: MapLocation(loc.x + 1, loc.y),
        ROTATION_DEGREES * 2: lambda loc: MapLocation(loc.x, loc.y + 1),
        ROTATION_DEGREES * 3: lambda loc: MapLocation(loc.x - 1, loc.y),
    }

    while True:
        state = (current_rotation, guard_location)
        if state in visited_states:
            return -1  # Loop detected
        visited_states.add(state)

        distinct_positions.add(guard_location)
        next_potential_guard_location = rotation_to_next_location[current_rotation](guard_location)
        if guard_leaving_map(puzzle, next_potential_guard_location):
            break
        elif puzzle[next_potential_guard_location.y][next_potential_guard_location.x] != OBSTRUCTION_SYMBOL:
            guard_location = next_potential_guard_location
        else:
            current_rotation = (current_rotation + ROTATION_DEGREES) % (4 * ROTATION_DEGREES)

    return distinct_positions


def guard_leaving_map(puzzle: list[list[str]], guard_location: MapLocation) -> bool:
    x, y = guard_location
    return y < 0 or y >= len(puzzle) or x < 0 or x >= len(puzzle[0])



def find_obstruction_locations_to_cause_loops(puzzle: list[list[str]], guard_location: MapLocation, original_guard_route: set[MapLocation]):
    number_of_obstruction_locations = 0
    for location in original_guard_route:
        if location != guard_location and puzzle[location.y][location.x] != OBSTRUCTION_SYMBOL:
            test_puzzle = copy.deepcopy(puzzle)
            test_puzzle[location.y][location.x] = OBSTRUCTION_SYMBOL
            if predict_guard_route(test_puzzle, guard_location, location) == -1:
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
