#!/usr/bin/env python3

import os


class Dial(object):
    def __init__(self, position:int):
        self._current_position = position
        self._zeros = 0

    def __str__(self):
        return f"current position: {self._current_position}\nzeros: {self._zeros}"

    def Rotate(self, command:str) -> None:
        direction = -1 if command[0] == "L" else 1

        distance = int(command[1:])
        movement = direction * (distance % 100)

        # Get the new position
        new_position = self._current_position + movement
        if new_position < 0:
            new_position += 100
        elif new_position >= 100:
            new_position -= 100

        # Get the number of times passing zero
        if direction == 1 and self._current_position != 0:
            initial_zero_distance = 100 - self._current_position
        elif self._current_position != 0:
            initial_zero_distance = self._current_position
        else:
            initial_zero_distance = 100
        self._current_position = new_position

        if distance >= initial_zero_distance:
            distance -= initial_zero_distance
            self._zeros += 1 + (distance // 100)

        # print(self)


if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    dial = Dial(50)
    # breakpoint()

    with open(os.path.join(TOP, "input")) as f:
        data = f.readlines()

    for command in data:
        dial.Rotate(command)

    print(dial._zeros)
