
import math
import os
from typing import List, Dict, Tuple

class Junction(object):
    def __init__(self, x:int, y:int, z:int):
        self.x = x
        self.y = y
        self.z = z
        self.circuit = -1

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    @property
    def in_circuit(self):
        return self.circuit != -1



class JunctionBoxes(object):
    def __init__(self, data:List[str]):
        self._junctions:List[Junction] = []
        self._distances:Dict[int: Tuple[Junction, Junction]] = {}
        self._circuits:Dict[int: int] = {}
        self._next_circuit:int = 1

        # Create our junctions and calculate the distances
        for line in data:
            x, y, z = line.split(",")
            self.AddJunction(int(x), int(y), int(z))


    def _connect(self, j1:Junction, j2:Junction):
        # Check for circuits which already exist and combine them together if applicable
        # print(f"Connecting {j1}@{j1.circuit} to {j2}@{j2.circuit}", end=" - ")
        if j1.in_circuit and not j2.in_circuit:
            j2.circuit = j1.circuit
            self._circuits[j1.circuit] += 1

        elif j2.in_circuit and not j1.in_circuit:
            j1.circuit = j2.circuit
            self._circuits[j2.circuit] += 1

        elif j1.in_circuit and j2.in_circuit:
            # These two are already in the same circuit, so we "nothing happens", per the puzzle
            if j1.circuit == j2.circuit:
                # print("On the same circuit already.")
                return

            self._circuits[j1.circuit] += self._circuits.pop(j2.circuit)

            # Perhaps a slight mismanagement of data in that I now need to loop through all the junctions and move the
            # ones as circuit j2 to circuit j1, but oh well...
            circ = j2.circuit
            for j in self._junctions:
                if j.circuit == circ:
                    # print(f"{j}->{j1.circuit}", end=" - ")
                    j.circuit = j1.circuit

        else:
            j1.circuit = self._next_circuit
            j2.circuit = self._next_circuit
            self._circuits[self._next_circuit] = 2
            self._next_circuit += 1


    @property
    def prod_three_largest_circuits(self):
        return math.prod(sorted(self._circuits.values() ,reverse=True)[0:3])


class JunctionBoxes1(JunctionBoxes):
    def __init__(self, data:List[str], connections):
        super().__init__(data)

        self.MakeCircuits(connections)


    def AddJunction(self, x:int, y:int, z:int):
        new_junction = Junction(x, y, z)
        for j in self._junctions:
            # Technically, if all we care about is shortest distance, we dont neet to sqrt() this and get the actual
            # distance here, as the ordering of distance^2 will be the same as the ordering of distance, however, I
            # Want to calculate the actual distance because I am guessing it will have something importance in part 2
            distance = math.sqrt(((j.x - new_junction.x)**2 + (j.y - new_junction.y)**2 + (j.z - new_junction.z)**2))
            if distance not in self._distances.keys():
                self._distances[distance] = []
            else:
                # The puzzle input does not tell us what to do whemn making curcuits if there is a distance which is the
                # same as another distance, so this is a warning message I guess...
                print("THERE IS A DUPLICATE DISTANCE!!!!")

            self._distances[distance] = tuple([j, new_junction])

        self._junctions.append(new_junction)


    def MakeCircuits(self, circuits):
        # After all the junctions have been made and the distances calculated, we can make circuits by connecting the
        # shortest distances together 'circuits' number of times

        # Get the 'circuits' closest distances which need to be connected together
        distances = sorted(self._distances.keys())[0:circuits]

        for d in distances:
            self._connect(self._distances[d][0], self._distances[d][1])


class JunctionBoxes2(JunctionBoxes):
    def __init__(self, data):
        super().__init__(data)

        self.MakeCircuits()


    @property
    def final_connection_x_product(self):
        return self._puzzle_two_result


    def AddJunction(self, x:int, y:int, z:int):
        # We will add our junctions mostly the same way, with the one difference being we assign each new junction to
        # its own circuit from the very start
        new_junction = Junction(x, y, z)
        new_junction.circuit = self._next_circuit
        self._circuits[self._next_circuit] = 1
        self._next_circuit += 1

        for j in self._junctions:
            distance = math.sqrt(((j.x - new_junction.x)**2 + (j.y - new_junction.y)**2 + (j.z - new_junction.z)**2))
            if distance not in self._distances.keys():
                self._distances[distance] = []
            else:
                # The puzzle input does not tell us what to do whemn making curcuits if there is a distance which is the
                # same as another distance, so this is a warning message I guess...
                print("THERE IS A DUPLICATE DISTANCE!!!!")

            self._distances[distance] = tuple([j, new_junction])

        self._junctions.append(new_junction)


    def MakeCircuits(self):
        # Also, almost the same as puzzle one, except our ending case is based on when we reach a circuit length of 1
        distances = sorted(self._distances.keys())

        for d in distances:
            self._connect(self._distances[d][0], self._distances[d][1])

            # Once we get here, no need to connect anty more
            if len(self._circuits) == 1:
                self._puzzle_two_result = self._distances[d][0].x * self._distances[d][1].x
                break




if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    with open(os.path.join(TOP, "input"), "r") as f:
        data = f.read()

    result = JunctionBoxes1(data.splitlines(), 1000)
    print(result.prod_three_largest_circuits)

    result = JunctionBoxes2(data.splitlines())
    print(result.final_connection_x_product)
