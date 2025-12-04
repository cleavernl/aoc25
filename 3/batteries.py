
import os
from typing import List, Tuple

class BatteryBanks(object):
    def __init__(self, data:List[str], batteries_per_bank=2):
        self.batteries_per_bank = batteries_per_bank
        self._max_joltages = []

        for bank in data:
            self.AddBank(bank)

    @property
    def max_joltage(self):
        return sum(self._max_joltages)

    def _get_max_power(self, batteries:str) -> Tuple[int,int]:
        """
        Gets the max power from the specified bank of batteries.
        Returns the power and the index that power is at.
        """
        max_power = -1
        index = -1

        # Loop through all but the last battery in the bank to find the highest joltage
        for i in range(len(batteries)):
            power = int(batteries[i])
            if power > max_power:
                max_power = power
                index = i

                if power == 9:
                    break

        return tuple([max_power, index])


    def AddBank(self, bank:str):
        digits = []

        # We are turning on a total of N batteries.
        # For the first one we turn on, we need to hold N-1 batteries in reserve
        # For the second, it is N-2
        # Third N-3, etc.
        # Additionally, we need to start with the battery directly after the previous battery we turned on

        starting_index = 0

        # This range function will return the number of batteries we need to hold in reserve for each
        for batteries_held in range(self.batteries_per_bank-1, -1, -1):
            if batteries_held == 0:
                test_bank = bank[starting_index:]
            else:
                test_bank = bank[starting_index:(-1 * batteries_held)]

            digit, index = self._get_max_power(test_bank)
            starting_index += (index + 1)
            digits.append(digit)

        # Do a fancy python one-liner to push all our digits together
        self._max_joltages.append( int("".join([str(d) for d in digits])) )


        #
        # Old depricated way before adding puzzle 2
        #

        # # The first battery can not be the last battery in the bank
        # first_digit, index = self._get_max_power(bank[:-1])

        # # The second battery has to be after the first battery
        # second_digit, _ = self._get_max_power(bank[index+1:])

        # self._max_joltages.append(int(f"{first_digit}{second_digit}"))



if __name__ == "__main__":
    TOP = os.path.dirname(__file__)

    with open(os.path.join(TOP, "input"), "r") as f:
        data = f.readlines()

    # Clean the data of all newlines
    data = [d.strip() for d in data]

    result = BatteryBanks(data)
    print(result.max_joltage)

    result = BatteryBanks(data, 12)
    print(result.max_joltage)
