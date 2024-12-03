import operator
import re
from functools import reduce

MUL_PATTERN = re.compile(r'mul\(([0-9]+,[0-9]+)\)')
DONT_PATTERN = re.compile(r"don't\(\)")
DO_PATTERN = re.compile(r"do\(\)")


def part_1(corrupted_memory: str) -> int:
    matches = MUL_PATTERN.findall(corrupted_memory)
    result = 0
    for match in matches:
        result += multiply_instructions(match)
    return result


def part_2(corrupted_memory: str) -> int:
    current_string = ""
    i = 0
    result = 0
    do = True
    while i < len(corrupted_memory):
        current_string += corrupted_memory[i]
        if match := MUL_PATTERN.findall(current_string):
            if do:
                result += multiply_instructions(match[0])
            current_string = ""
        elif DONT_PATTERN.findall(current_string):
            do = False
        elif DO_PATTERN.findall(current_string):
            do = True
        i += 1
    return result


def multiply_instructions(instructions: str) -> int:
    operands = map(int, instructions.split(","))
    return reduce(operator.mul, operands)


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        corrupted_memory = fp.read()

        print(part_1(corrupted_memory))
        print(part_2(corrupted_memory))
