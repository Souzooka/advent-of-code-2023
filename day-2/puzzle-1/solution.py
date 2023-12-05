# Maximum amount of each cube as stated in puzzle specification
MAX_VALUES = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def isValidGame(sets: str):
    for cubeSet in sets:
        # Individual categories; we're going to assume that each color only appears once in a set
        categories = [s.strip() for s in cubeSet.split(',')]
        for category in categories:
            numCubes, color = category.split(' ')
            # Color should be red, green, or blue
            if int(numCubes) > MAX_VALUES[color]:
                return False

    return True

def main():
    # Sum of IDs of possible games
    total = 0

    with open("../input.txt", "r") as file:
        for line in file:
            # First, parse the ID then remove that data from the string
            colonIndex = line.index(":")
            gameID = int(line[5:colonIndex])
            line = line[colonIndex + 1:]

            # Individual sets
            sets = [s.strip() for s in line.split(';')]
            if isValidGame(sets):
                total += gameID

    print(f"Sum = {total}")

main()
