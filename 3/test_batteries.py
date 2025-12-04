from batteries import BatteryBanks

def test_puzzle_one():
    tests = [
        [["987654321111111"], 98],
        [["811111111111119"], 89],
        [["987654321111111", "811111111111119", "234234234234278", "818181911112111"], 357]
    ]

    for test in tests:
        result = BatteryBanks(test[0])
        assert result.max_joltage == test[1]


def test_puzzle_two():
    tests = [
        [["987654321111111"], 987654321111],
        [["811111111111119"], 811111111119],
        [["987654321111111", "811111111111119", "234234234234278", "818181911112111"], 3121910778619]
    ]

    for test in tests:
        result = BatteryBanks(test[0], 12)
        assert result.max_joltage == test[1]
