import itertools
import operator
from functools import partial, lru_cache, reduce


def concatenation(a: int, b: int) -> int:
    return int(str(a) + str(b))


OPERATORS = [operator.add, operator.mul, concatenation]


def equation_is_valid(required_result: int, operands: list[int]):
    operator_combos = itertools.product(OPERATORS, repeat=len(operands) - 1)

    def reducer(operator_combo, x: tuple[int, int], y: tuple[int, int]):
        index, _x = x
        next_index, _y = y
        return next_index, operator_combo[index](_x, _y)

    for operator_combo in operator_combos:
        _, result = reduce(partial(reducer, operator_combo), enumerate(operands))
        if result == required_result:
            return True
    return False


def compute_total_calibration_result(equation_components: dict[int, list[int]]):
    calibration_result = 0
    for result, operands in equation_components.items():
        if equation_is_valid(result, operands):
            calibration_result += result
    return calibration_result


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        lines = map(str.strip, fp.readlines())
        equation_components = {}
        for line in lines:
            result, *operands = line.split(": ")
            operands = list(map(int, operands[0].split(" ")))
            result = int(result)
            equation_components[result] = operands
        print(compute_total_calibration_result(equation_components))
