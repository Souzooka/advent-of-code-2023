
def main():
    # Sum of powers of the sets
    total = 0

    with open("../input.txt", "r") as file:
        for line in file:
            # Remove the game ID info from the string; we don't need anything from it here either
            colonIndex = line.index(":")
            line = line[colonIndex + 1:]

            # Record the max cubes found for the game
            maxCubes = {
                'red': 0,
                'green': 0,
                'blue': 0,
            }

            # Individual sets
            sets = [s.strip() for s in line.split(';')]
            for cubeSet in sets:
                # Individual categories; we're going to assume that each color only appears once in a set
                categories = [s.strip() for s in cubeSet.split(',')]
                for category in categories:
                    numCubes, color = category.split(' ')
                    # Color should be red, green, or blue
                    maxCubes[color] = max(maxCubes[color], int(numCubes))

            # Add the power to the total
            total += (maxCubes['red'] * maxCubes['green'] * maxCubes['blue'])

    print(f"Sum = {total}")

main()
