from paper import Floor

example = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

def test_puzzle_one():
    floor = Floor(example.splitlines())
    assert floor.accessible == 13


def test_puzzle_two():
    floor = Floor(example.splitlines())
    floor.RemoveAccessible()
    assert(floor.total_removed == 43)
