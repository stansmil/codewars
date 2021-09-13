class PokerHand(object):

    RESULT = ["Loss", "Win", "Tie"]

    card_values = "23456789AJKQT"
    hand_values = ["Highcard",
                   "Pair",
                   "Two pairs",
                   "Three of a kind",
                   "Straight",
                   "Flush",
                   "Full house",
                   "Four of a kind",
                   "Straight flush",
                   "Royal flush"]

    def __init__(self, hand):
        self.hand_value = self.define_hand_value(hand)

    def define_hand_value(self, hand):
        values_seq = sorted(item[0] for item in hand.split(" "))

    def compare_with(self, other):
        pass
