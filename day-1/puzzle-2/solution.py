# Now we have to look out for ordinals; here's a mapping to transform them if found
ordinals = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def main():
    # Sum of calibration values
    total = 0

    with open("../input.txt", "r") as file:
        for line in file:
            # Since ordinals can overlap, such as in the example line "eightwothree",
            # we can't just replace the ordinals in the line. So I'm going to just
            # record the indices where we find a digit or ordinal, then sort the record at the end.
            # NOTE: Might be worthwhile revisiting a solution without sorting; bisect probably works
            # just as well though Python 3.8 doesn't support bisect with keys unfortunately.
            
            # Tuples of (digit, position)
            digits = []
            
            # Start by checking ordinals
            for ordinal, digit in ordinals.items():
                # We have to loop here so we can find all instances of an ordinal appearing multiple times in a line
                index = -1
                while (index := line.find(ordinal, index + 1)) != -1:
                    digits.append((digit, index))
            
            # Finally a last pass to find normal digit characters
            digits += [(int(c), i) for i, c in enumerate(line) if ord('0') <= ord(c) <= ord('9')]

            # Sort that stuff
            digits.sort(key=lambda x: x[1])

            # Now we can just pull the first and last item to get the number for this line
            # NOTE: Again assuming we have at least 1 valid digit per line
            value = int(f"{digits[0][0]}{digits[-1][0]}")
            total += value

    print(f"Calibration value = {total}")

main()
