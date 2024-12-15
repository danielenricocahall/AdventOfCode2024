import re
from dataclasses import dataclass
from typing import Callable

ROWS, COLS = 103, 101


#ROWS, COLS = 7, 11


@dataclass
class RobotPosition:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, RobotVelocity):
            self.x += other.x
            self.y += other.y
            if self.x < 0:
                self.x = COLS + self.x
            if self.y < 0:
                self.y = ROWS + self.y
            self.x = self.x % COLS
            self.y = self.y % ROWS
        return self


@dataclass
class RobotVelocity:
    x: int
    y: int


class Robot:
    position: RobotPosition
    velocity: RobotVelocity

    def __init__(self, position: list[int], velocity: list[int]):
        self.position = RobotPosition(*position)
        self.velocity = RobotVelocity(*velocity)

    def calculate_position_over_time(self, time: int):
        for _ in range(time):
            self.position += self.velocity


def display_robot_positions_debug(robots: list[Robot]):
    def assign_robot_counts(position):
        if position == ".":
            position = 1
        else:
            position += 1
        return position

    _display_robots_positions(robots, assign_robot_counts)


def display_robot_positions_to_find_christmas_tree(robots: list[Robot]):
    _display_robots_positions(robots, lambda *args: "#")


def _display_robots_positions(robots: list[Robot], robot_symbol_assignment: Callable):
    floor_layout = [["."] * COLS for _ in range(ROWS)]
    for robot in robots:
        floor_layout[robot.position.y][robot.position.x] = robot_symbol_assignment(floor_layout[robot.position.y][robot.position.x])
    print(*["".join(map(str, row)) for row in floor_layout], sep='\n')
    print('\n')


def parse_positions_and_velocities_into_robots(lines: list[str]) -> list[Robot]:
    robots = []
    for line in lines:
        numbers = list(map(int, re.findall(r'-?\d+', line)))
        position, velocity = numbers[:2], numbers[2:]
        robots.append(Robot(position, velocity))
    return robots


def compute_safety_factor(robots: list[Robot]):
    # top left
    quadrant_1 = lambda robot: 0 <= robot.position.y < ROWS // 2 and 0 <= robot.position.x < COLS // 2

    # top right
    quadrant_2 = lambda robot: 0 <= robot.position.y < ROWS // 2 and COLS // 2 < robot.position.x < COLS

    # bottom left
    quadrant_3 = lambda robot: ROWS // 2 < robot.position.y < ROWS and 0 <= robot.position.x < COLS // 2

    # bottom right
    quadrant_4 = lambda robot: ROWS // 2 < robot.position.y < ROWS and COLS // 2 < robot.position.x < COLS

    return len(list(filter(quadrant_1, robots))) * len(list(filter(quadrant_2, robots))) * len(
        list(filter(quadrant_3, robots))) * len(list(filter(quadrant_4, robots)))


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        lines = list(map(str.strip, fp.readlines()))
        robots = parse_positions_and_velocities_into_robots(lines)
        for i in range(10000):
            for robot in robots:
                robot.calculate_position_over_time(1)
            print(f"Seconds: {i}")
            print('\n')
            display_robot_positions_to_find_christmas_tree(robots)
        print(compute_safety_factor(robots))
