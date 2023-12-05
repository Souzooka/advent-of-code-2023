from typing import List, Optional, Tuple


def main() -> None:
    lowest: Optional[int] = None

    with open("../input.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]
        # The first line contains seed info, so we can just pull that out easily enough
        seeds = [int(seed) for seed in lines[0][len('seeds: '):].split(' ')]

        # Now we need to parse the other maps;
        # we don't need to know what the mapping actually *is*, i.e. soil-to-fertilizer
        # or whatever, since they just feed into eachother. I suppose this wouldn't work
        # if they were out of order in the input, but so be it.

        # What I'm going to try and do here is have lists of a list of (destination range, source range)
        # and we'll see how that goes.
        # First we have to find where the maps begin in the input.
        # I figure we can just start from the beginning of one map, read lines until we find a blank one,
        # then skip 2 lines, and repeat until EOF.

        # First mapping always begins on line 4
        lineIndex = 3
        mapIndex = 0
        maps: List[List[Tuple[range, range]]] = []
        while lineIndex < len(lines):
            # Create the empty mapping if it doesn't exist
            if mapIndex >= len(maps):
                maps.append([])

            if lines[lineIndex] == '':
                # We're on an empty line so we've exhausted a map
                mapIndex += 1
                lineIndex += 2
                continue

            # Non-empty line so we should have 3 numbers here
            destStart, sourceStart, rangeLen = (int(n) for n in lines[lineIndex].split(' '))
            maps[mapIndex].append((range(destStart, destStart + rangeLen), range(sourceStart, sourceStart + rangeLen)))
            lineIndex += 1

        # Now that we have the mappings, we should be able to iterate through each map with each seed and find the lowest location
        for seed in seeds:
            value = seed
            for map in maps:
                for destRange, sourceRange in map:
                    if value in sourceRange:
                        # The value is in the mapping, so we just need to take the diff from the source start
                        # and add that to the dest start.
                        # If we didn't find the value in any of the mappings, we don't need to do anything else,
                        # since it'll just remain the same value.
                        delta = value - sourceRange.start
                        value = destRange.start + delta
                        break

            # value here is now our location plot
            if lowest is None:
                lowest = value
            else:
                lowest = min(lowest, value)

    print(f"Lowest location = {lowest}")

main()
