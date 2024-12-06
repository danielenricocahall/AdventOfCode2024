from collections import namedtuple

GUARD_SYMBOL = "^"
OBSTACLE_SYMBOL = "#"
ROTATION_DEGREES = 90

GuardLocation = namedtuple('GuardLocation', ['x', 'y'])


def find_initial_guard_location(puzzle: list[list[str]]) -> GuardLocation:
    for y, row in enumerate(puzzle):
        if GUARD_SYMBOL in row:
            x = row.index(GUARD_SYMBOL)
            return GuardLocation(x, y)


def predict_guard_route(puzzle: list[list[str]], guard_location: GuardLocation):
    distinct_positions = set()
    current_rotation = 0
    rotation_to_next_location = {
        ROTATION_DEGREES * 0: lambda guard_location: GuardLocation(guard_location.x, guard_location.y - 1),
        ROTATION_DEGREES * 1: lambda guard_location: GuardLocation(guard_location.x + 1, guard_location.y),
        ROTATION_DEGREES * 2: lambda guard_location: GuardLocation(guard_location.x, guard_location.y + 1),
        ROTATION_DEGREES * 3: lambda guard_location: GuardLocation(guard_location.x - 1, guard_location.y)
    }
    while not guard_leaving_map(puzzle, guard_location):
        next_guard_location = rotation_to_next_location[current_rotation](guard_location)
        if puzzle[next_guard_location.y][next_guard_location.x] != OBSTACLE_SYMBOL:
            guard_location = next_guard_location
            distinct_positions.add(guard_location)
        else:
            current_rotation = (current_rotation + ROTATION_DEGREES) % (4 * ROTATION_DEGREES)
        print(f"***STEP {len(distinct_positions)} TAKEN***")
        # for debugging on the test
        #puzzle[guard_location.y][guard_location.x] = "X"
        #display_puzzle(puzzle)
    return len(distinct_positions)



def guard_leaving_map(puzzle: list[list[str]], guard_location: GuardLocation) -> bool:
    x, y = guard_location
    return y >= len(puzzle) - 1 or x >= len(puzzle[0]) - 1 or y < 0 or x < 0


def display_puzzle(puzzle: list[str]):
    print(*puzzle, sep=f"\n")


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        lines = map(str.split, fp.readlines())
        puzzle = [list(line[0]) for line in lines]
        guard_location = find_initial_guard_location(puzzle)
        print(predict_guard_route(puzzle, guard_location))
