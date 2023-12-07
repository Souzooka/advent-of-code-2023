from __future__ import annotations

from collections import Counter
from enum import IntEnum, unique
from typing import List


class Hand:

    # Strength rating of each card suit
    __SUITS_LIST = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
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
        self.__bet = bet
        self.__type = self.__determineType()

    def getHand(self) -> str:
        return self.__hand

    def getBet(self) -> int:
        return self.__bet

    def __determineType(self) -> Hand.Rank:
        cardCount = Counter(self.__hand)
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
