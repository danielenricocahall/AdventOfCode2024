import itertools
import math
from collections import defaultdict

DEFAULT_LOCATION_SYMBOL = "."


def compute_antenna_locations(puzzle: list[list[str]]) -> dict[str, list]:
    antenna_locations = defaultdict(list)
    for i, row in enumerate(puzzle):
        for j, column in enumerate(puzzle):
            if (location := puzzle[i][j]) != DEFAULT_LOCATION_SYMBOL:
                antenna_locations[location].append((i, j))
    return antenna_locations


def compute_antinodes(antenna_to_location_map: dict[str, list[tuple]], puzzle: list[list[str]] | None = None):
    rows = len(puzzle)
    cols = len(puzzle[0])
    antinode_locations = set()

    def is_valid_antinode_location(location: tuple[int, int]) -> bool:
        return 0 <= location[0] < rows and 0 <= location[1] < cols

    for antenna, antenna_locations in antenna_to_location_map.items():
        all_antenna_location_pairs = itertools.combinations(antenna_locations, 2)
        for location, other_location in all_antenna_location_pairs:
            vert_distance = location[0] - other_location[0]
            horiz_distance = location[1] - other_location[1]
            antinode_location_1 = (location[0] + vert_distance, location[1] + horiz_distance)
            antinode_location_2 = (other_location[0] + (-vert_distance), other_location[1] + (-horiz_distance))
            if is_valid_antinode_location(antinode_location_1):
                antinode_locations.add(antinode_location_1)
                # puzzle[antinode_location_1[0]][antinode_location_1[1]] = "#"
            if is_valid_antinode_location(antinode_location_2):
                antinode_locations.add(antinode_location_2)
                # puzzle[antinode_location_2[0]][antinode_location_2[1]] = "#"
        # display_puzzle(map(lambda x: "".join(x), puzzle))
    return len(antinode_locations)


def display_puzzle(puzzle):
    print(*puzzle, sep=f"\n")


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        puzzle = list(map(lambda x: list(x.strip()), fp.readlines()))
        antenna_to_location = compute_antenna_locations(puzzle)

        print(compute_antinodes(antenna_to_location, puzzle))
