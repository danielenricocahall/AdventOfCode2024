
def blink(stones: list[int], num_blinks: int) -> list[int]:
    for _ in range(num_blinks):
        stones = apply_rules(stones)
    return stones

def apply_rules(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            splitted_stones = split_stone(stone)
            new_stones.extend(splitted_stones)
        else:
            new_stones.append(stone * 2024)
    return new_stones


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
    stones_after_blinking = blink(stones, 25)
    print(len(stones_after_blinking))

