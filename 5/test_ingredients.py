from ingredients import Ingredients

data = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

def test_puzzle_one():
    ingreds = Ingredients(data.splitlines())
    assert ingreds.total_fresh == 3


def test_puzzle_two():
    ingreds = Ingredients(data.splitlines())
    assert ingreds.max_fresh == 14
