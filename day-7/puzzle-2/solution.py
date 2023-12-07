from __future__ import annotations

from collections import Counter
from enum import IntEnum, unique
from typing import List


class Hand:

    # Strength rating of each card suit
    __SUITS_LIST = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    SUITS = {s: i for i, s in enumerate(__SUITS_LIST)}
    del __SUITS_LIST

    @unique
    class Rank(IntEnum):
        HIGH_CARD = 0
        ONE_PAIR = 1
        TWO_PAIR = 2
        THREE_OF_A_KIND = 3
        FULL_HOUSE = 4
        FOUR_OF_A_KIND = 5
        FIVE_OF_A_KIND = 6

    def __init__(self, hand: str, bet: int) -> None:
        assert len(hand) == 5
        self.__hand = hand
        self.__adjustedHand = self.__resolveJokers()
        self.__bet = bet
        self.__type = self.__determineType()

    def getHand(self) -> str:
        return self.__hand

    def getBet(self) -> int:
        return self.__bet

    def __resolveJokers(self):
        # The presence of jokers should be able to promote up
        # to pretty much any type (well except TWO_PAIR -- we'd just go to THREE_OF_A_KIND),
        # including rarely to full house for a hand like 23J32, I think
        cards = list(self.__hand)
        nonJokers = [card for card in cards if card != 'J']
        numJokers = len(cards) - len(nonJokers)
        nonJokerCount = Counter(nonJokers)
        nonJokerCountValues = nonJokerCount.values()

        # No jokers or all jokers (which is FIVE_OF_A_KIND in itself)
        if numJokers in (0, 5):
            return self.__hand

        # NOTE: The actual values of the cards don't matter when determining
        # hand type, so we can fudge the hand we check later.
        # Can we promote to FIVE_OF_A_KIND?
        if (5 - numJokers) in nonJokerCountValues:
            return '22222'

        # FOUR_OF_A_KIND?
        if (4 - numJokers) in nonJokerCountValues:
            return '22223'

        # FULL_HOUSE (specifically should only be TWO_PAIR (non-joker) with 1 joker)
        if list(nonJokerCountValues).count(2) == 2 and numJokers == 1:
            return '22233'

        # THREE_OF_A_KIND
        if (3 - numJokers) in nonJokerCountValues:
            return '22234'

        # ONE_PAIR
        # If we have *ANY* jokers and can't promote to any of the other
        # case then we must be able to make one pair.
        return '22345'

    def __determineType(self) -> Hand.Rank:
        cardCount = Counter(self.__adjustedHand)
        counts = list(cardCount.values())
        cardType = None

        if 5 in counts:
            cardType = Hand.Rank.FIVE_OF_A_KIND
        elif 4 in counts:
            cardType = Hand.Rank.FOUR_OF_A_KIND
        elif 3 in counts:
            if 2 in counts:
                cardType = Hand.Rank.FULL_HOUSE
            else:
                cardType = Hand.Rank.THREE_OF_A_KIND
        elif counts.count(2) == 2:
            cardType = Hand.Rank.TWO_PAIR
        elif counts.count(2) == 1:
            cardType = Hand.Rank.ONE_PAIR
        else:
            cardType = Hand.Rank.HIGH_CARD

        assert cardType is not None
        return cardType

    # For list.sort()
    def __lt__(self, other) -> bool:
        if not isinstance(other, Hand):
            return TypeError(f"< not supported for {self.__class__.__name__} and {other.__class__.__name__}.")

        if self.__type < other.__type:
            return True
        if self.__type > other.__type:
            return False

        # Both hands are the same type so we have to compare the strength of
        # individual cards in the hands
        for i in range(len(self.__hand)):
            if Hand.SUITS[self.__hand[i]] < Hand.SUITS[other.__hand[i]]:
                return True
            elif Hand.SUITS[self.__hand[i]] > Hand.SUITS[other.__hand[i]]:
                return False

        # Both hands are equal I guess
        return False



def main() -> None:
    lines = []
    with open("../input.txt", "r") as file:
        lines = file.readlines()

    hands: List[Hand] = []
    for line in lines:
        tokens = line.split(' ')
        hand = tokens[0]
        bet = int(tokens[1])
        hands.append(Hand(hand, bet))

    hands.sort()
    total = 0
    for rank, hand in enumerate(hands):
        total += (hand.getBet() * (rank + 1))

    print(f"Total winnings = {total}")

main()
