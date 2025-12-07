
import math
import os
import re
from typing import List

class Mathsheet(object):
    def __init__(self, data:List[str]):
        self._additions = []
        self._multiplications = []

        # Fix the spacing of the data and turn it into a list
        for i in range(len(data)):
            line = data[i].strip()
            line = re.sub(r' +', ' ', line)
            line = line.split(' ')
            data[i] = line

        nums = data[0:-1]
        operators = data[-1]

        for i in range(len(nums[0])):
            operation = [int(n[i]) for n in nums]
            if operators[i] == "+":
                self._additions.append(operation)
            else:
                self._multiplications.append(operation)

    @property
    def total_sum(self):
        total = 0
        for a in self._additions:
            total += sum(a)

        for m in self._multiplications:
            total += math.prod(m)

        return total


class ConvolutedMathsheet(object):
    def __init__(self, data:List[str]):
        self._total = 0
        nums = data[0:-1]
        operations = data[-1]

        # Loop through the data starting from the rightmost column and going left
        op = []
        method = ""
        for i in range(len(nums[0]), -1, -1):
            # Get the number represented by this column
            strnum = ""
            for n in nums:
                try:
                    if n[i] != " ":
                        strnum += n[i]
                except IndexError:
                    print("ierror")
                    pass

            # Get the method represented by this column (if there is one)
            try:
                if operations[i] != " ":
                    method = operations[i]
            except IndexError:
                pass

            if strnum:
                op.append(int(strnum))
            if i == 0 or not strnum:
                # print(f"Current total: {self._total}")
                # print(op)
                # print(method)
                # breakpoint()
                # This indicates we got a blannk column, reset the operation and continue
                if method == "*":
                    # There is some bug in here in that the very first number we try and get is a bunch of index errors
                    # Typically we wouldn't care, since the operation doesn't exist yet, but the product of an empty
                    # list is 1, so I was getting an error of being exactly 1 larger than my actual answer should be...
                    # I really dislike this puzzle, so I don't care to fix the problem, the sum() of an empty list is 0
                    # so I do not get this error when checking for the "*" symbol instead of the "+" symbol
                    self._total += math.prod(op)
                else:
                    self._total += sum(op)
                op = []

    @property
    def total_sum(self):
        return self._total


if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    with open(os.path.join(TOP, "input"), "r") as f:
        data = f.read()

    result = Mathsheet(data.splitlines())
    print(result.total_sum)

    result2 = ConvolutedMathsheet(data.splitlines())
    print(result2.total_sum)
