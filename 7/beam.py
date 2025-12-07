
import os
from typing import List


class Manifold(object):
    def __init__(self, data:List[str]):
        self._beam_indecies = []
        self._beam_weights = []
        self._manifold = data
        self._splits = 0

        self.Fire()


    @property
    def splits(self):
        return self._splits

    @property
    def timelines(self):
        return sum(self._beam_weights[-1])


    def Fire(self):
        # Find starting position
        # Each element in _beam_indecies now contains an (index, weight) where wheight is the number of timelines which
        # could result in this index
        self._beam_indecies.append([self._manifold[0].find("S")])
        self._beam_weights.append([1])

        # Loop through the rest of the rows in the manifold
        for i in range(1, len(self._manifold)):
            ind = self._beam_indecies[-1].copy()
            weights = self._beam_weights[-1].copy()
            # Find the locations where we need to split
            splitters = [s for s, ch in enumerate(self._manifold[i]) if ch == "^"]
            for j in splitters:
                if j in ind:
                    # Split the beam here
                    self._splits += 1

                    weight = weights.pop(ind.index(j))
                    ind.remove(j)

                    if j-1 in ind:
                        weights[ind.index(j-1)] += weight
                    else:
                        ind.append(j-1)
                        weights.append(weight)

                    if j+1 in ind:
                        weights[ind.index(j+1)] += weight
                    else:
                        ind.append(j+1)
                        weights.append(weight)

            self._beam_indecies.append(ind)
            self._beam_weights.append(weights)


if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    with open(os.path.join(TOP, "input"), "r") as f:
        data = f.read()

    result = Manifold(data.splitlines())
    print(result.splits)

    print(result.timelines)
