from io import TextIOWrapper
import string
from typing import List

# Adjacency rules
ADJACENT = [
    [-1, 1],  [0, 1],  [1, 1],
    [-1, 0],           [1, 0],
    [-1, -1], [0, -1], [1, -1],
]

def readNumber(grid: List[List[int]], x: int, y: int):
    # Bounds checking
    if not 0 <= y < len(grid):
        return 0
    if not 0 <= x < len(grid[y]):
        return 0
    
    # Is this even a number?
    if chr(grid[y][x]) not in string.digits:
        return 0
    
    # OK, we have a number, we have to scan left and right to find the bounds on this line
    line = grid[y]
    start = end = x

    # Scan left
    for start in range(x, -1, -1):
        if chr(line[start]) not in string.digits:
            # Char at start is grabbed so we have to add 1
            start = start + 1
            break
    
    # Scan right
    for end in range(x, len(line) + 1):
        if end >= len(line) or chr(line[end]) not in string.digits:
            break
    
    value = int(''.join(chr(c) for c in line[start:end]))

    # Now we can patch out the value in our grid
    for i in range(start, end):
        line[i] = ord('.')

    return value


def parseGrid(file: TextIOWrapper) -> List[List[int]]:
    # Converts the file contents into a grid of character codes.
    # We use character codes instead of strings because we want to mutate
    # the grid later to "patch" out numbers so they aren't detected multiple times.
    return [[ord(c) for c in s.strip()] for s in file.readlines()]

def main():
    total = 0

    with open("../input.txt", "r") as file:
        grid = parseGrid(file)
        
        # Iterate over the grid looking for any non-digits and non-periods
        for y, line in enumerate(grid):
            for x, symbol in enumerate(line):
                if chr(symbol) not in '.' + string.digits:
                    # Found a valid symbol, try to read any adjacent numbers
                    for deltaX, deltaY in ADJACENT:
                        total += readNumber(grid, x + deltaX, y + deltaY)

    print(f"Part number total = {total}")

main()
