from typing import List, Tuple

# NOTE: This solution doesn't work yet, may revisit

def main() -> None:

    with open("../input.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]
        # The first line contains seed info, so we can just pull that out easily enough
        seeds = [int(seed) for seed in lines[0][len('seeds: '):].split(' ')]

        # Now for part 2 we have to transform the seeds into ranges
        rangeSeeds = []
        for i in range(0, len(seeds), 2):
            rangeSeeds.append(range(seeds[i], seeds[i] + seeds[i+1]))
        seeds: List[range] = rangeSeeds

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

        # Now we're gonna do something similar to solution 1, but keep everything as a range instead of worrying about
        # each individual seed.
        # e.g. for seeds: 100 200 and seed-to-location map: 500 100 50 we'd end up with two ranges (500, 550) and (150, 300)
        # and then we could just take the lowest start from each range we make.
        values = seeds.copy()
        for map in maps:
            newValues = []

            for destRange, sourceRange in map:
                # Custom iteration because we may have to splice in/out split seed ranges
                seedIndex = 0
                while seedIndex < len(values):
                    seedRange = values[seedIndex]

                    # Check for overlap points
                    overlapLow = None
                    overlapHigh = None
                    if seedRange.start in sourceRange:
                        overlapLow = seedRange.start
                    elif sourceRange.start in seedRange:
                        overlapLow = sourceRange.start
                    if seedRange.stop - 1 in sourceRange:
                        overlapHigh = seedRange.stop
                    elif sourceRange.stop - 1 in seedRange:
                        overlapHigh = sourceRange.stop

                    if overlapLow is not None:
                        # both low and high shouldn't be None
                        deltaLow = overlapLow - sourceRange.start
                        deltaHigh = sourceRange.stop - overlapHigh
                        newValues.append(range(destRange.start + deltaLow, destRange.stop - deltaHigh))

                        if overlapLow == seedRange.start and overlapHigh == seedRange.stop:
                            # Complete overlap
                            values[seedIndex:seedIndex + 1] = []
                            seedIndex -= 1
                        elif overlapLow == seedRange.start and overlapHigh == sourceRange.stop:
                            # Overlap over start of seedRange
                            values[seedIndex] = range(sourceRange.stop, seedRange.stop)
                        elif overlapLow == sourceRange.start and overlapHigh == seedRange.stop:
                            # Overlap over end of seedRange
                            values[seedIndex] = range(seedRange.start, sourceRange.start)
                        elif overlapLow == seedRange.start and overlapHigh == seedRange.stop:
                            # Source range contained within seed range
                            range1 = range(sourceRange.start, seedRange.start)
                            range2 = range(seedRange.stop, sourceRange.stop)
                            values[seedIndex:seedIndex + 1] = [range1, range2]
                            seedIndex += 1

                    seedIndex += 1

            newValues.extend(values)
            values = newValues

        print(f"Lowest location = {min(values, key=lambda x: x.start).start}")

main()
