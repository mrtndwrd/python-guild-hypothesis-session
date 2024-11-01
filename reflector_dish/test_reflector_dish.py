from hypothesis import given, strategies as st

from reflector_dish import StringDish, OptimizedDish, Direction


# Step 1:
# Write a strategy function for the following:
# - The stringdish, the constructor takes a list[list[str]], where each string is either "O" (rolling rock), "#" (square rock), or "." (free space).
# - An optimized dish, which can be easily generated from a stringdish.
# - The possible directions, which are all possible values of the Direction enum.

string_dish_strategy = ...
optimized_dish_strategy = ...
direction_strategy = ...

# Step 2:
# Now that you have strategies to generate random (valid) dishs. Test the following properties:
# - Converting a stringdish to optimized and back should not change the dish.
# - Converting an optimized dish to stringdish and back should not change the dish.
# - Shifting the dish in any direction should not change the number of rocks.
# - Shifting the dish in any direction should not make any rocks fall off the dish.
# - Shifting the dish multiple times in the same direction should be the same as shifting it once.
# - Rocks should not pass through unmovable cells.
# - After a tilt in a specific direction, the rocks should move in that direction as far as possible, but not further.
#
# Note:
#   A strategy can be passed to a test function by using the @given decorator.
#
#   @given(string_dish_strategy)
#   def test_some_property(dish: StringDish):
#       assert ...
#
