
import os
from typing import List


class Ingredients(object):
    def __init__(self, data:List[str]):
        self._fresh_ranges = []
        self._fresh_ids = []
        self._spoiled_ids = []

        for line in data:
            if "-" in line:
                lower, upper = line.split("-")
                self.AddRange(int(lower), int(upper))
            elif not line:
                self.NoramlizeRanges()
            else:
                self.AddIngredient(int(line))

    @property
    def total_fresh(self):
        return len(self._fresh_ids)

    @property
    def max_fresh(self):
        total = 0
        for r in self._fresh_ranges:
            total += r[1] - r[0] + 1
        return total

    def AddRange(self, lower:int, upper:int):
        # self._fresh_ranges ~ [(5, 10), (20, 30), (38, 90)]
        for r in self._fresh_ranges:
            # This new range starts in the middle of an existing range and ends higher
            if r[0] <= lower <= r[1] and upper >= r[1]:
                r[1] = upper
                return

            # This new range starts lower than an existing range and ends in the middle
            elif lower <= r[0] and r[0] <= upper <= r[1]:
                r[0] = lower
                return

            # This new range starts lower and ends higher than an existing range
            elif lower <= r[0] and upper >= r[1]:
                r[0] = lower
                r[1] = upper
                return

            # This range falls completely within an existing range
            elif r[0] >= lower and r[1] <= upper:
                return

        # If we get here, the new range is completely exclusive from all other ranges
        self._fresh_ranges.append([lower, upper])


    def NoramlizeRanges(self):
        # Since we can add in ranges overlapping more than one section, they will not be perfectly normalized after a
        # first pass. Ther eis almost certainly a better way to do this, probably at initial insert time, but I don't
        # care enough to do it right now. Instead, just remove and reinsert each range until the initial length is the
        # same as the end length
        initial_length = 0
        while initial_length != len(self._fresh_ranges):
            initial_length = len(self._fresh_ranges)
            for i in range(initial_length):
                r = self._fresh_ranges.pop(0)
                self.AddRange(r[0], r[1])


    def AddIngredient(self, num):
        for r in self._fresh_ranges:
            if r[0] <= num <= r[1]:
                self._fresh_ids.append(num)
                return

        self._spoiled_ids.append(num)



if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    with open(os.path.join(TOP, "input"), "r") as f:
        data = f.read()

    result = Ingredients(data.splitlines())
    print(result.total_fresh)

    print(result.max_fresh)
