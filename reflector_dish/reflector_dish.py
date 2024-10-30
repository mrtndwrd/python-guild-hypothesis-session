"""
Very ugly and inefficient implementation of the reflector dish problem (https://adventofcode.com/2023/day/14).
The code is not optimized and is not efficient. It is just to show how we can use hypothesis to test the code.

The problem is about a two-dimensional surface (the dish) that can be tilted in four directions (N, S, W, E).
The dish has round (rolling) rocks (O), and square (unmovable) rocks (#). 
When the dish is tilted, the round rocks (O) move in the direction of the tilt until they hit a square rock (#) or the edge of the dish.

For example, this is what a dish looks like, with the round rocks (O) and square rocks (#):
O....#....          OOOO.#.O..
O.OO#....#          OO..#....#
.....##...          OO..O##..O
OO.#O....O   shift  O..#.OO...
.O.....O#.   north  ........#.
O.#..O.#.#    ->    ..#....#.#
..O..#O..O          ..O..#.O.O
.......O..          ..O.......
#....###..          #....###..
#OO..#....          #....#....
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Four possible directions to tilt the dish towards."""

    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


@dataclass
class StringDish:
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
        """Convert the string dish to an optimized dish."""
        return OptimizedDish(
            height=self.height,
            width=self.width,
            rolling_rocks=[
                (x, y)
                for y, row in enumerate(self.dish)
                for x, cell in enumerate(row)
                if cell == "O"
            ],
            unmovable_rock={
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
    rolling_rocks: list[tuple[int, int]]
    unmovable_rock: set[tuple[int, int]]

    def to_naive(self) -> StringDish:
        """Convert the optimized dish to a string dish."""
        dish = [["." for _ in range(self.width)] for _ in range(self.height)]
        for x, y in self.rolling_rocks:
            dish[y][x] = "O"
        for x, y in self.unmovable_rock:
            dish[y][x] = "#"

        return StringDish(dish=dish)

    def shift(self, direction: Direction):
        """Shift the dish in the given direction. Tilting all the rocks towards that direction."""
        match direction:
            case Direction.NORTH:
                self.rolling_rocks = self._shift_north()
            case Direction.SOUTH:
                self.rolling_rocks = self._shift_south()
            case Direction.WEST:
                self.rolling_rocks = self._shift_west()
            case Direction.EAST:
                self.rolling_rocks = self._shift_east()

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, OptimizedDish):
            return False

        return (
            self.height == value.height
            and self.width == value.width
            and self.unmovable_rock == value.unmovable_rock
            and sorted(self.rolling_rocks) == sorted(value.rolling_rocks)
        )

    def _shift_north(self):
        new_positions = []
        for x, y in self.rolling_rocks:
            end = 0
            for s in range(y, -1, -1):
                if (x, s) in self.unmovable_rock:
                    end = s + 1
                    break

            path = [(x, s) for s in range(end, y)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rolling_rocks])

            pos = end + rocks_between
            new_positions.append((x, pos))

        return new_positions

    def _shift_south(self):
        new_positions = []
        for x, y in self.rolling_rocks:
            end = self.height - 1
            for s in range(y, self.height):
                if (x, s) in self.unmovable_rock:
                    end = s - 1
                    break

            path = [(x, s) for s in range(y + 1, end + 1)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rolling_rocks])

            pos = end - rocks_between
            new_positions.append((x, pos))

        return new_positions

    def _shift_west(self):
        new_positions = []
        for x, y in self.rolling_rocks:
            end = 0
            for s in range(x, -1, -1):
                if (s, y) in self.unmovable_rock:
                    end = s + 1
                    break

            path = [(s, y) for s in range(end, x)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rolling_rocks])

            pos = end + rocks_between
            new_positions.append((pos, y))

        return new_positions

    def _shift_east(self):
        new_positions = []
        for x, y in self.rolling_rocks:
            end = self.width - 1
            for s in range(x, self.width):
                if (s, y) in self.unmovable_rock:
                    end = s - 1
                    break

            path = [(s, y) for s in range(x + 1, end + 1)]
            rocks_between = sum([1 for (a, b) in path if (a, b) in self.rolling_rocks])

            pos = end - rocks_between
            new_positions.append((pos, y))

        return new_positions
