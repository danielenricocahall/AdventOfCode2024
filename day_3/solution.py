import operator
import re
from functools import reduce

MUL_PATTERN = re.compile(r'mul\(([0-9]+,[0-9]+)\)')
DONT_PATTERN = re.compile(r"don't\(\)")
DO_PATTERN = re.compile(r"do\(\)")


def part_1(corrupted_memory: str) -> int:
    matches = MUL_PATTERN.findall(corrupted_memory)
    result = sum(map(multiply_instructions, matches))
    return result


def part_2(corrupted_memory: str) -> int:
    result = 0
    do = True
    start_pos, end_pos = 0, 1
    while end_pos < len(corrupted_memory):
        if match := MUL_PATTERN.findall(corrupted_memory, start_pos, end_pos):
            if do:
                result += multiply_instructions(match[0])
            start_pos = end_pos
        elif DONT_PATTERN.findall(corrupted_memory, start_pos, end_pos):
            do = False
        elif DO_PATTERN.findall(corrupted_memory, start_pos, end_pos):
            do = True
        end_pos += 1
    return result

def multiply_instructions(instructions: str) -> int:
    operands = map(int, instructions.split(","))
    return reduce(operator.mul, operands)


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        corrupted_memory = fp.read()

        print(part_1(corrupted_memory))
        print(part_2(corrupted_memory))
