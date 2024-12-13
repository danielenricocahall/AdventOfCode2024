import re
from dataclasses import dataclass


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


@dataclass
class ClawMachine:
    button_a_movement: Movement
    button_b_movement: Movement
    prize_position: Position


def parse_input_into_claw_machines(_input: list[str]):
    claw_machines = []
    current_claw_machine = []
    for line in _input:
        if not line:
            claw_machines.append(create_claw_machine(current_claw_machine))
            current_claw_machine = []
        else:
            current_claw_machine.append(line)
    return claw_machines


def create_claw_machine(claw_machine_configuration: list[str]):
    button_a, button_b, prize = claw_machine_configuration
    button_a_movements = map(int, re.findall(r'\d+', button_a))
    button_b_movements = map(int, re.findall(r'\d+', button_b))
    prize_location = map(int, re.findall(r'\d+', prize))
    prize_coordinates = Position(*prize_location)
    claw_machine = ClawMachine(Movement(*button_a_movements), Movement(*button_b_movements), prize_coordinates)
    return claw_machine

if __name__ == "__main__":
    with open('./puzzle_test.txt') as fp:
        _input = list(map(str.strip, fp.readlines()))

        print(parse_input_into_claw_machines(_input))