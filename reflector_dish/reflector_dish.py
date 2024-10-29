"""
Very ugly and inefficient implementation of the reflector dish problem (https://adventofcode.com/2023/day/14).
The code is not optimized and is not efficient. It is just to show how we can use hypothesis to test the code.
"""

from __future__ import annotations
from functools import cached_property
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Four possible directions to tilt the dish towards."""

    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


@dataclass
class NaiveDish:
    """
    A naive implementation of the reflector dish.

    This class does not implement any of the logic required to solve the problem.
    Instead, it can be used to easily generate and show (valid) boards which can be
    converted to optimized boards to solve the problem.
    """

    dish: list[list[str]]

    @property
    def height(self) -> int:
        return len(self.dish)

    @property
    def width(self) -> int:
        return len(self.dish[0])

    def print_dish(self):
        """Pretty print the dish to console."""
        for line in self.dish:
            print("".join(line))

    def to_optimized(self) -> OptimizedDish:
        """Convert the naive dish to an optimized dish."""
        return OptimizedDish(
            height=self.height,
            width=self.width,
            rocks=[
                (x, y)
                for y, row in enumerate(self.dish)
                for x, cell in enumerate(row)
                if cell == "O"
            ],
            unmovable={
                (x, y)
                for y, row in enumerate(self.dish)
                for x, cell in enumerate(row)
                if cell == "#"
            },
        )


@dataclass
class OptimizedDish:

    height: int
    width: int
    rocks: list[tuple[int, int]]
    unmovable: set[tuple[int, int]]

    def to_naive(self) -> NaiveDish:
        """Convert the optimized dish to a naive dish."""
        dish = [["." for _ in range(self.width)] for _ in range(self.height)]
        for x, y in self.rocks:
            dish[y][x] = "O"
        for x, y in self.unmovable:
            dish[y][x] = "#"

        return NaiveDish(dish=dish)

    def shift(self, direction: Direction):
        """Shift the dish in the given direction. Tilting all the rocks towards that direction."""
        match direction:
            case Direction.NORTH:
                self.rocks = self._shift_north()
            case Direction.SOUTH:
                self.rocks = self._shift_south()
            case Direction.WEST:
                self.rocks = self._shift_west()
            case Direction.EAST:
                self.rocks = self._shift_east()

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, OptimizedDish):
            return False

        return (
            self.height == value.height
            and self.width == value.width
            and self.unmovable == value.unmovable
            and sorted(self.rocks) == sorted(value.rocks)
        )

    def _shift_north(self):
        new_positions = []
        for x, y in self.rocks:
            end = 0
            for s in range(y, -1, -1):
                if (x, s) in self.unmovable:
                    end = s + 1
                    break

            path = [(x, s) for s in range(end, y)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rocks])

            pos = end + rocks_between
            new_positions.append((x, pos))

        return new_positions

    def _shift_south(self):
        new_positions = []
        for x, y in self.rocks:
            end = self.height - 1
            for s in range(y, self.height):
                if (x, s) in self.unmovable:
                    end = s - 1
                    break

            path = [(x, s) for s in range(y + 1, end + 1)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rocks])

            pos = end - rocks_between
            new_positions.append((x, pos))

        return new_positions

    def _shift_west(self):
        new_positions = []
        for x, y in self.rocks:
            end = 0
            for s in range(x, -1, -1):
                if (s, y) in self.unmovable:
                    end = s + 1
                    break

            path = [(s, y) for s in range(end, x)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rocks])

            pos = end + rocks_between
            new_positions.append((pos, y))

        return new_positions

    def _shift_east(self):
        new_positions = []
        for x, y in self.rocks:
            end = self.width - 1
            for s in range(x, self.width):
                if (s, y) in self.unmovable:
                    end = s - 1
                    break

            path = [(s, y) for s in range(x + 1, end + 1)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rocks])

            pos = end - rocks_between
            new_positions.append((pos, y))

        return new_positions
