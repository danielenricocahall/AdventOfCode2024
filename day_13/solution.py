import re
from dataclasses import dataclass

from pulp import PULP_CBC_CMD


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Movement):
            self.x += other.x
            self.y += other.y


@dataclass
class Movement:
    x: int
    y: int
    cost: int


@dataclass
class ClawMachine:
    button_a_movement: Movement
    button_b_movement: Movement
    prize_position: Position

    def minimum_tokens_to_prize(self):

        from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, value

        problem = LpProblem("Integer_Linear_Program", LpMaximize)

        x1 = LpVariable("x1", lowBound=0, cat=LpInteger)
        x2 = LpVariable("x2", lowBound=0, cat=LpInteger)

        problem += x1 + x2, "Objective_Function"

        problem += self.button_a_movement.x * x1 + self.button_b_movement.x * x2 == self.prize_position.x, "Constraint_1"
        problem += self.button_a_movement.y * x1 + self.button_b_movement.y * x2 == self.prize_position.y, "Constraint_2"

        status = problem.solve(PULP_CBC_CMD(msg=False))

        if status == 1:
            print(f"Minimum moves: ({value(x1)}, {value(x2)})")
            return self.button_a_movement.cost * value(x1) + self.button_b_movement.cost * value(x2)
        else:
            print("No optimal solution found.")


def parse_input_into_claw_machines(_input: list[str]):
    claw_machines = []
    current_claw_machine = []
    for line in _input:
        if not line:
            claw_machines.append(create_claw_machine(current_claw_machine, False))
            current_claw_machine = []
        else:
            current_claw_machine.append(line)
    return claw_machines


def create_claw_machine(claw_machine_configuration: list[str], account_for_unit_conversion_error: bool = False):
    button_a, button_b, prize = claw_machine_configuration
    button_a_movements = map(int, re.findall(r'\d+', button_a))
    button_b_movements = map(int, re.findall(r'\d+', button_b))
    prize_location = map(int, re.findall(r'\d+', prize))
    if account_for_unit_conversion_error:
        prize_location = map(lambda x: x + 10000000000000, prize_location)
    prize_coordinates = Position(*prize_location)
    claw_machine = ClawMachine(Movement(*button_a_movements, 3), Movement(*button_b_movements, 1), prize_coordinates)
    return claw_machine


if __name__ == "__main__":
    with open('./puzzle_test.txt') as fp:
        _input = list(map(str.strip, fp.readlines()))

        claw_machines = parse_input_into_claw_machines(_input)
        minimum_tokens_for_all_claw_machines = 0
        for claw_machine in claw_machines:
            minimum_tokens = claw_machine.minimum_tokens_to_prize()
            if minimum_tokens:
                minimum_tokens_for_all_claw_machines += minimum_tokens
        print(minimum_tokens_for_all_claw_machines)
