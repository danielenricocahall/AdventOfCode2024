from collections import Counter


def part_1(_left, _right) -> int:
    _left = sorted(_left)
    _right = sorted(_right)
    return sum(abs(x - y) for x, y in zip(_left, _right))


def part_2(_left, _right):
    frequency_in_right = Counter(_right)
    similarity_score = sum(n * frequency_in_right[n] for n in left)
    return similarity_score


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        lines = map(str.strip, fp.readlines())
        numbers = list(map(lambda x: x.split("   "), lines))
        left, right = zip(*numbers)
        left = list(map(int, left))
        right = list(map(int, right))
        part_1_result = part_1(left, right)
        part_2_result = part_2(left, right)
        print(part_1_result)
        print(part_2_result)
