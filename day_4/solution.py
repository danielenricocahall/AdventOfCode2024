import re

XMAS_PATTERN = re.compile(r"(?=(XMAS|SAMX))")


def find_occurrences_horizontally(puzzle: list[str]) -> int:
    xmas_occurrences_horizontally = sum(len(XMAS_PATTERN.findall(row)) for row in puzzle)
    return xmas_occurrences_horizontally


def find_occurrences_diagonally(puzzle: list[str], strings: list[str]) -> int:
    diagonal_occurrences = 0
    cols = len(puzzle[0])
    for s in strings:
        for i in range(len(puzzle) - len(s) + 1):
            for j in range(cols - len(s) + 1):
                occurrence = all(puzzle[i + k][j + k] == c for k, c in enumerate(s))
                diagonal_occurrences += occurrence
    return diagonal_occurrences


def transpose_puzzle(puzzle: list[str]) -> list[str]:
    transposed_puzzle = list(zip(*puzzle))
    transposed_puzzle = list(map(lambda x: "".join(x), transposed_puzzle))
    return transposed_puzzle


def display_puzzle(puzzle: list[str]):
    print(*puzzle, sep=f"\n")


def find_all_x_mas(puzzle: list[str]):
    rows = len(puzzle)
    cols = len(puzzle[0])
    row, col = 1, 1
    all_x_mas = 0
    while row != rows:
        col = 1
        curr_rows = puzzle[row - 1:row + 2]
        while col != cols:
            window = [x[col - 1:col + 2] for x in curr_rows]
            left_cross = find_occurrences_diagonally(window, ["MAS", "SAM"])
            right_cross = find_occurrences_diagonally(window[::-1], ["MAS", "SAM"])
            if left_cross and right_cross:
                all_x_mas += 1
            col += 1
        row += 1
    return all_x_mas


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        puzzle = list(map(str.strip, fp.readlines()))
        rows = len(puzzle)
        cols = len(puzzle[0])
        horizontal_occurrences = find_occurrences_horizontally(puzzle)
        vertical_occurrences = find_occurrences_horizontally(transpose_puzzle(puzzle))
        diagonal_occurrences = find_occurrences_diagonally(puzzle, ["XMAS", "SAMX"])
        other_diagonal_occurrences = find_occurrences_diagonally(puzzle[::-1], ["XMAS", "SAMX"])
        print(diagonal_occurrences + horizontal_occurrences + vertical_occurrences + other_diagonal_occurrences)

        print(find_all_x_mas(puzzle))
