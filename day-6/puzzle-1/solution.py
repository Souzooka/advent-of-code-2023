from math import ceil, floor


def winPossibilities(time: int, distance: int) -> int:
    # time itself in the puzzle input is rather low, so it could be iterated over linearly
    # without issues. However, we can overengineer this a little and perhaps it would help with puzzle 2 a bit.
    # We only have to check the first half of time since the range of possible wins is mirrored over the middle point
    # (e.g. for a time of 30ms and 200mm in the example, wins can be accomplished by holding the button from any time
    # since 11ms to (30-11) or 19ms.)
    # Additionally, we can use a binary search to find the lower bound for a possible win in log time, and from there
    # the problem can be solved.
    low = 1 # 0 would never win (unless the distance record is negative...?)
    high = time // 2

    # First we can check if high here (the midpoint) would be the race distance if we held the button for that long.
    # if not, then there are no combinations which can win the race. (Perhaps we're just tied for perfect WR which is still nice)
    if high * (time - high) <= distance:
        return 0

    while low != high:
        current = (low + high) / 2

        if floor(current) * (time - floor(current)) <= distance:
            # No win
            low = ceil(current)
        else:
            # Win
            high = floor(current)

    return (time - low) - low + 1


def main() -> None:
    total = 1

    with open("../input.txt", "r") as file:
        lines = file.readlines()

        # Line 1 is times
        # For the purposes of this puzzle I assume that both times and distances are the same length
        # and that the input lines are always in the same order and start with the same prefix, yadayadyada
        times = [int(time) for time in lines[0][len('Time:      '):].split(' ') if time != '']
        # Line 2 is distances
        distances = [int(distance) for distance in lines[1][len('Distance:  '):].split(' ') if distance != '']

        for time, distance in zip(times, distances):
            total *= winPossibilities(time, distance)

    print(f"Total = {total}")

main()
