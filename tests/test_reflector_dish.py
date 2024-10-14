from hypothesis import given, strategies as st

from experiment.code import NaiveDish, OptimizedDish, Direction
import copy


def naive_board_strategy(width: int, height: int):
    return st.lists(
        st.lists(
            st.sampled_from(["O", "#", "."]),
            min_size=width,
            max_size=width,
        ),
        min_size=height,
        max_size=height,
    )


naive_dish_strategy = st.builds(NaiveDish, board=naive_board_strategy(10, 10))
optimized_dish_strategy = naive_dish_strategy.map(lambda board: board.to_optimized())
direction_strategy = st.sampled_from(
    [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST],
)


@given(naive_dish_strategy)
def test_conversion_naive(dish: NaiveDish):
    """Converting a board to optimized and back should not change the board."""
    assert dish == dish.to_optimized().to_naive()


@given(optimized_dish_strategy, direction_strategy)
def test_conversion_with_shift(dish: OptimizedDish, direction: Direction):
    """Converting a board to optimized and back should not change the board."""
    dish.shift(direction=direction)

    assert dish.to_naive().to_optimized() == dish


@given(
    optimized_dish_strategy,
    direction_strategy,
)
def test_conservation_of_rocks(dish: OptimizedDish, direction: Direction):
    """Performing one of the tilts should not change the number of rocks."""
    num_rocks = len(dish.rocks)

    dish.shift(direction)
    assert num_rocks == len(dish.rocks)


@given(optimized_dish_strategy, direction_strategy)
def test_rocks_stay_on_dish(dish: OptimizedDish, direction: Direction):
    """Performing one of the tilts should not make any rocks fall off the dish."""
    dish.shift(direction)
    assert all((0 <= x < dish.width and 0 <= y < dish.height) for x, y in dish.rocks)


@given(direction_strategy)
def test_rocks_dont_pass_through_unmovable(direction: Direction):
    """
    Rocks should not pass through unmovable cells.
    Note: used example based testcase here as it is much easier.
    """
    # fmt: off
    naive_dish = NaiveDish(
        [
            [".", ".", ".", ".", ".",],
            [".", "#", "#", "#", ".",],
            [".", "#", "O", "#", ".",],
            [".", "#", "#", "#", ".",],
            [".", ".", ".", ".", ".",],
        ]
    )
    # fmt: on
    optimized_board = naive_dish.to_optimized()
    optimized_board.shift(direction)

    assert naive_dish == optimized_board.to_naive()


@given(optimized_dish_strategy, direction_strategy)
def test_movement_is_idempotent(dish: OptimizedDish, direction: Direction):
    """
    Shifting the dish twice in the same direction should be the same as shifting it once.
    """
    dish.shift(direction)

    dish_copy = copy.deepcopy(dish)
    dish.shift(direction)

    assert dish == dish_copy


@given(optimized_dish_strategy, direction_strategy)
def test_rocks_should_move_towards_tilt(dish: OptimizedDish, direction: Direction):
    """
    Rocks should roll as far as they can towards the tilt.
    Validate this by tilting and then checking that the next position is invalid,
    meaning that the rock couldn't move any further.
    """
    dish.shift(direction)
    naive_dish = dish.to_naive()

    diff = {
        Direction.NORTH: (0, -1),
        Direction.SOUTH: (0, 1),
        Direction.WEST: (-1, 0),
        Direction.EAST: (1, 0),
    }

    for x, y in dish.rocks:
        # Current position should be occupied
        assert naive_dish.board[y][x] == "O"

        dx, dy = diff[direction]

        new_x, new_y = x + dx, y + dy

        if new_x < 0 or new_x >= dish.width or new_y < 0 or new_y >= dish.height:
            # Rock is at the edge of the dish
            continue

        # Next position should be occupied
        assert naive_dish.board[y + dy][x + dx] in ["O", "#"]
