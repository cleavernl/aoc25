from mathsheet import Mathsheet, ConvolutedMathsheet

data = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

def test_puzzle_one():
    result = Mathsheet(data.splitlines())
    assert result.total_sum == 4277556


def test_puzzle_two():
    result = ConvolutedMathsheet(data.splitlines())
    assert result.total_sum == 3263827
