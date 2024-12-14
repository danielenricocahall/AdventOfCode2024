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

        def compute_determinant(matrix: list[list[int]]) -> int:
            a1, b1 = matrix[0]
            a2, b2= matrix[1]
            return a1 * b2 - b1 * a2


        A = [[self.button_a_movement.x, self.button_b_movement.x],
             [self.button_a_movement.y, self.button_b_movement.y]]
        b = [self.prize_position.x, self.prize_position.y]

        D = compute_determinant(A)
        D_x = compute_determinant([[b[0], self.button_b_movement.x],
                                   [b[1], self.button_b_movement.y]])
        D_y = compute_determinant([[self.button_a_movement.x, b[0]],
                                   [self.button_a_movement.y, b[1]]])

        x_sol = D_x / D
        y_sol = D_y / D

        if int(x_sol) == x_sol and int(y_sol) == y_sol:
            print(x_sol, y_sol)
            return self.button_a_movement.cost * x_sol + self.button_b_movement.cost * y_sol
        else:
            print("No solution found")


def parse_input_into_claw_machines(_input: list[str], account_for_unit_conversion: bool = False):
    claw_machines = []
    current_claw_machine = []
    for line in _input:
        if not line:
            claw_machines.append(create_claw_machine(current_claw_machine, account_for_unit_conversion))
            current_claw_machine = []
        else:
            current_claw_machine.append(line)
    claw_machines.append(create_claw_machine(current_claw_machine, account_for_unit_conversion))
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
    with open('./puzzle.txt') as fp:
        _input = list(map(str.strip, fp.readlines()))

        claw_machines = parse_input_into_claw_machines(_input,True)
        minimum_tokens_for_all_claw_machines = 0
        for claw_machine in claw_machines:
            minimum_tokens = claw_machine.minimum_tokens_to_prize()
            if minimum_tokens:
                minimum_tokens_for_all_claw_machines += minimum_tokens
        print(minimum_tokens_for_all_claw_machines)
