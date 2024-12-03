import operator
import re
from functools import reduce

if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        instruction = fp.read()
        matches = re.findall(r'mul\(([0-9]+,[0-9]+)\)', instruction)
        result = 0
        for match in matches:
            operands = map(int, match.split(","))
            result += reduce(operator.mul, operands)

        print(result)


