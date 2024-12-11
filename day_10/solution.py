from collections import Counter
from functools import lru_cache

TRAILHEAD = 0
END_OF_TRAIL = 9

def get_trailheads(topographic_map: list[list[int]]) -> set[tuple[int, int]]:
    trailheads = list()
    for i in range(len(topographic_map)):
        for j in range(len(topographic_map[0])):
            if topographic_map[i][j] == TRAILHEAD:
                trailheads.append((i, j))
    return trailheads

def find_trails(trailhead: tuple[int, int], topographic_map: list[list[int]], distinct: bool = False):
    visited = set()
    def _find_trails(current_position: tuple[int, int], next_value: int):
        i, j = current_position
        window = []
        if topographic_map[i][j] != next_value:
            return 0
        if next_value == END_OF_TRAIL:
            if distinct and (current_position in visited):
                return 0
            visited.add(current_position)
            return 1
        if i > 0:
            window.append((i - 1, j))
        if i < len(topographic_map) - 1:
            window.append((i + 1, j))
        if j > 0:
            window.append((i, j - 1))
        if j < len(topographic_map[0]) - 1:
            window.append((i, j + 1))
        return sum(_find_trails(position, next_value + 1) for position in window)
    result = _find_trails(trailhead, TRAILHEAD)
    return result


if __name__ == "__main__":
    topographic_map = []
    trail_heads = 0
    with open('./puzzle.txt') as fp:
        for line in fp.readlines():
            topographic_map.append(list(map(int, line.strip())))

    trailheads = get_trailheads(topographic_map)

    print(sum(find_trails(trailhead, topographic_map, False) for trailhead in trailheads))