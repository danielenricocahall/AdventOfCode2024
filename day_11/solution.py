from collections import defaultdict
from datetime import datetime


def unpack_dict(vals: dict[int | tuple[int, int], int]):
    unpacked = defaultdict(int)
    for k, v in vals.items():
        if isinstance(k, int):
            unpacked[k] += v
        elif isinstance(k, tuple):
            for val in k:
                unpacked[val] += v
    return unpacked


def blink(stones: list[int], num_blinks: int) -> int:
    count = len(stones)
    current_counts = defaultdict(int)
    for stone in stones:
        current_counts[stone] += 1
    for _ in range(num_blinks):
        next_counts = defaultdict(int)
        for k, v in current_counts.items():
            next_counts[apply_rule(k)] += v
        count += sum(v for k, v in next_counts.items() if isinstance(k, tuple))
        current_counts = next_counts
    return count


def apply_rule(stone: int) -> int | tuple[int, int]:
    if stone == 0:
        return 1
    elif len(str(stone)) % 2 == 0:
        splitted_stones = split_stone(stone)
        return splitted_stones
    else:
        return stone * 2024


def split_stone(stone: int) -> tuple[int, int]:
    str_stone = str(stone)
    left_digits, right_digits = str_stone[:len(str_stone) // 2], str_stone[len(str_stone) // 2:]
    right_digits = strip_leading_zeroes_if_needed(right_digits)
    return int(left_digits), int(right_digits)


def strip_leading_zeroes_if_needed(stone_str: str):
    while stone_str.startswith("0") and len(stone_str) > 1:
        stone_str = stone_str[1:]
    return stone_str


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        stones = list(map(int, fp.read().split()))
    start = datetime.now()
    stones_after_blinking = blink(stones, 75)
    end = datetime.now()
    print(end - start)
    print(stones_after_blinking)
