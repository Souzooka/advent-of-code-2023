
def main():
    total = 0

    with open("../input.txt", "r") as file:
        for line in file.readlines():
            # Remove card info
            colonIndex = line.find(':')
            line = line[colonIndex + 1:]

            # Split up the line and parse
            winningNumbers, haveNumbers = line.split(' | ')
            winningNumbers = set(int(s) for s in winningNumbers.split(' ') if s != '')
            haveNumbers = set(int(s) for s in haveNumbers.split(' ') if s != '')

            # Now just have to do a set intersection and take the length of that intersection
            intersection = winningNumbers & haveNumbers
            if len(intersection) != 0:
                total += pow(2, len(intersection) - 1)

    print(f"Total points = {total}")

main()
