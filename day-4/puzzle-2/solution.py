from typing import Dict


def main():
    # Holds the number of instances we have of each card
    cardCounts: Dict[int, int] = {}

    with open("../input.txt", "r") as file:
        for line in file.readlines():
            # Remove card info (though parse the card ID this time)
            colonIndex = line.find(':')
            cardID = int(line[4:colonIndex].strip())
            line = line[colonIndex + 1:]

            # Account for this original instance of the card
            cardCounts.setdefault(cardID, 0)
            cardCounts[cardID] += 1

            # Figure out how many instances of this card we have
            numInstances = cardCounts[cardID]

            # Split up the line and parse
            winningNumbers, haveNumbers = line.split(' | ')
            winningNumbers = set(int(s) for s in winningNumbers.split(' ') if s != '')
            haveNumbers = set(int(s) for s in haveNumbers.split(' ') if s != '')

            # Now just have to do a set intersection and take the length of that intersection
            intersection = winningNumbers & haveNumbers
            for i in range(cardID + 1, cardID + 1 + len(intersection)):
                # We get another instance of the following card, multiplied by the number of instances of this current card
                cardCounts.setdefault(i, 0)
                cardCounts[i] += numInstances

    print(f"Total cards = {sum(cardCounts.values())}")

main()
