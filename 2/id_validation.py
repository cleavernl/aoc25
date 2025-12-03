
import os
import math

class Puzzle(object):
    def __init__(self, data:str):
        self._invalid_ids = []

        ranges = data.split(",")

        for r in ranges:
            lower_limit, upper_limit = (val for val in r.split("-"))
            self.find_invalid(lower_limit, upper_limit)

    @property
    def total(self):
        # Just in case there are any overlapping ranges, remove all duplicate entries
        return sum(set(self._invalid_ids))


class Puzzle1(Puzzle):
    def find_invalid(self, lower_limit:str, upper_limit:str):
        lower_digits = len(lower_limit)
        upper_digits = len(upper_limit)

        lower_limit = int(lower_limit)
        upper_limit = int(upper_limit)

        # This will loop through each "number of digits" in the provided range
        # i.e., a range of 1-9 will loop through [1] and a range of 1-100 will loop through [1,2,3]
        for digits in range(lower_digits, upper_digits+1, 2):
            # NOTE: Any time there is an odd number of digits, we can not have a repreating pattern, so we loop through
            # our range in an increment of 2

            # This will get us to loop through all numbers of the specified number of digits
            # i.e. in the case of 2 digits [10, ..., 99] and 3 digits [100, ..., 999]
            for num in range(int(math.pow(10, (digits/2) - 1)), int(math.pow(10, (digits/2)))):
                invalid_id = int(f"{num}{num}")
                if lower_limit <= invalid_id <= upper_limit:
                    self._invalid_ids.append(invalid_id)

                if invalid_id >= upper_limit:
                    break


class Puzzle2(Puzzle):
    def find_invalid(self, lower_limit:str, upper_limit:str):
        upper_digits = len(upper_limit)

        lower_limit = int(lower_limit)
        upper_limit = int(upper_limit)

        # Loop throug all possible invalid IDs, starting with the ones that repeat twice (like in p1), then go to the
        # ones that repeat 3 times, then 4, etc.
        repeats = 2
        while True:
            if repeats > upper_digits:
                break

            num = 1
            while True:
                invalid_id = int(f"{num}" * repeats)

                if invalid_id > upper_limit:
                    break

                if lower_limit <= invalid_id <= upper_limit:
                    self._invalid_ids.append(invalid_id)

                num += 1

            repeats += 1



if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    with open(os.path.join(TOP, "input"), "r") as f:
        data = f.read()

    result = Puzzle1(data)
    print(result.total)

    result = Puzzle2(data)
    print(result.total)
