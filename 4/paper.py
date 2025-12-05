
import os

class Floor(object):
    def __init__(self, data):
        self._floor = []
        self._accessible_rolls = []
        self.total_removed = 0

        for row in data:
            self._floor.append([c == "@" for c in row ])

        self.FindAccessible()


    @property
    def accessible(self):
        return len(self._accessible_rolls)


    def _is_paper(self, x, y):
        # Since python lets us index a negative number, we need to account for that here
        if min(x, y, 0) != 0:
            return False
        try:
            return self._floor[x][y]
        except IndexError:
            return False


    def FindAccessible(self):
        for row in range(len(self._floor)):
            for column in range(len(self._floor[row])):
                # Only count locations with paper in them
                if not self._floor[row][column]:
                    continue

                #
                # All cells we need to be check are some offset of our current x,y location
                #
                #     [-1, -1] [+0, -1] [+1, -1]
                #     [-1, +0] [  ... ] [+1, +0]
                #     [-1, +1] [+0, +1] [+1, +1]
                #

                # Count the number of surrounding 'True' elements
                surrounding_rolls = 0
                for x_offset in range(-1, 2):
                    for y_offset in range(-1, 2):
                        if x_offset == 0 and y_offset == 0:
                            continue

                        if self._is_paper(row + y_offset, column + x_offset):
                            # breakpoint()
                            surrounding_rolls += 1

                            if surrounding_rolls >= 4:
                                break
                    if surrounding_rolls >= 4:
                        break

                if surrounding_rolls < 4:
                    self._accessible_rolls.append(tuple([row, column]))


    def RemoveAccessible(self):
        while self.accessible != 0:
            for x, y in self._accessible_rolls:
                self._floor[x][y] = False
                self.total_removed += 1

            self._accessible_rolls = []

            self.FindAccessible()


if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    with open(os.path.join(TOP, "input"), "r") as f:
        data = f.readlines()

    result = Floor(data)
    print(result.accessible)

    result.RemoveAccessible()
    print(result.total_removed)
