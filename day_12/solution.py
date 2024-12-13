from collections import defaultdict
from datetime import datetime
from functools import lru_cache


def next_unvisited_region(visited: list[list[bool]]):
    rows = len(visited)
    cols = len(visited[0])
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                return i, j
    return None
def find_region(puzzle: list[str]):
    rows = len(puzzle)
    cols = len(puzzle[0])
    visited = [[False] * cols for _ in range(rows)]

    current_region = 0
    all_regions = defaultdict(set)
    def _find_regions(current_position: tuple[int, int]):
        i, j = current_position
        current_character = puzzle[i][j]
        visited[i][j] = True
        neighbors = get_neighbors(i, j, rows, cols)
        existing_regions = []
        for neighbor_i, neighbor_j in neighbors:
            if not visited[neighbor_i][neighbor_j]:
                if puzzle[neighbor_i][neighbor_j] == current_character:
                    existing_regions.append((neighbor_i, neighbor_j))
        return existing_regions

    while unvisited_region := next_unvisited_region(visited):
        all_regions[current_region].add(unvisited_region)
        new_regions = _find_regions(unvisited_region)
        while new_regions:
            new_region = new_regions.pop()
            all_regions[current_region].add(new_region)
            new_regions += _find_regions(new_region)
        current_region += 1
    return all_regions

#@lru_cache
def get_neighbors(i: int, j: int, rows: int, cols: int):
    neighbors = []
    if i > 0:
        neighbors.append((i - 1, j))
    if i < rows - 1:
        neighbors.append((i + 1, j))
    if j > 0:
        neighbors.append((i, j - 1))
    if j < cols - 1:
        neighbors.append((i, j + 1))
    return neighbors

def calculate_areas(regions: dict[int: set[tuple[int, int]]]):
    areas = [len(v) for k, v in regions.items()]
    return areas


def calculate_perimeters(regions: dict[int: set[tuple[int, int]]], puzzle):
    perimeters = []
    rows = len(puzzle)
    cols = len(puzzle[0])
    for k, v in regions.items():
        region_perimeter = 0
        for region in v:
            region_perimeter += 4
            neighbors = get_neighbors(*region, rows, cols)
            for neighbor in neighbors:
                if neighbor in v:
                    region_perimeter -= 1
        perimeters.append(region_perimeter)
    return perimeters


def calculate_total_price(areas: list[int], perimeters: list[int]):
    return sum(x * y for x, y in zip(areas, perimeters))



if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        puzzle = list(map(str.strip, fp.readlines()))
        start_time = datetime.now()
        regions = find_region(puzzle)
        areas = calculate_areas(regions)
        perimeters = calculate_perimeters(regions, puzzle)
        total_price = calculate_total_price(areas, perimeters)
        end_time = datetime.now()
        print(total_price)
        print(end_time - start_time)
