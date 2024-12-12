from collections import defaultdict


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
    def get_neighbors(i: int, j: int):
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

    current_region = 0
    all_regions = defaultdict(set)
    def _find_regions(current_position: tuple[int, int]):
        i, j = current_position
        current_character = puzzle[i][j]
        visited[i][j] = True
        neighbors = get_neighbors(i, j)
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

    print(all_regions)








if __name__ == "__main__":
    with open('./puzzle_test1.txt') as fp:
        puzzle = list(map(str.strip, fp.readlines()))
        find_region(puzzle)

