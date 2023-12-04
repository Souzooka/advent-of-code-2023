def main():
    # Sum of calibration values
    total = 0

    with open("../input.txt", "r") as file:
        for line in file:
            # We can strip out non-digit characters by using a list comprehension
            digits = [c for c in line if ord('0') <= ord(c) <= ord('9')]
            # And get first and last digit using simple indexing
            # NOTE: I assume we get at least 1 digit in each line here
            value = int(f"{digits[0]}{digits[-1]}")
            total += value

    print(f"Calibration value = {total}")

main()
