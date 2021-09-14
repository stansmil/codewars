from collections import Counter


class PokerHand(object):

    RESULT = ["Loss", "Win", "Tie"]

    card_rank = "23456789TJQKA"
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
        self.hand_cards = hand.split(" ")
        self.values_counter = Counter([c[0] for c in self.hand_cards]).most_common()
        self.suits_counter = Counter([c[1] for c in self.hand_cards]).most_common()
        self.hand_score = sum(self.card_rank.index(vc[0]) * vc[1] for vc in self.values_counter)
        self.hand_value = self.define_hand_value()

    def define_hand_value(self):
        score = sum(self.card_rank.index(vc[0]) * vc[1] for vc in self.values_counter)
        hand_sorted = sorted(self.hand_cards, key=lambda c: self.card_rank.index(c[0]))
        if all(self.card_rank.index(hand_sorted[i][0]) + 1 == self.card_rank.index(hand_sorted[i + 1][0]) for i in range(4)):
            # straight
            return self.handle_straight(score), score

        if len(self.suits_counter) == 1:
            return "Flush", score

        if len(self.values_counter) < 5:
            return self.handle_pairs()

        return "Highcard", self.card_rank.index(hand_sorted[-1][0])

    def handle_straight(self, score):
        if len(self.suits_counter) == 1:
            return "Royal flush" if score == 50 else "Straight flush"
        return "Straight"

    def handle_pairs(self):
        min_cnt = min(vc[1] for vc in self.values_counter)
        max_cnt = max(vc[1] for vc in self.values_counter)

        if max_cnt == 4:
            return "Four of a kind", self.card_rank.index(self.values_counter[0][0]) * 4

        if max_cnt == 3 and min_cnt == 2:
            return "Full house", self.card_rank.index(self.values_counter[0][0]) * 3 + self.card_rank.index(self.values_counter[1][0]) * 2

        if max_cnt == 3:
            return "Three of a kind", self.card_rank.index(self.values_counter[0][0]) * 3

        if max_cnt == 2 and len(self.values_counter) == 3:
            return "Two pairs", self.card_rank.index(self.values_counter[0][0]) * 2 + self.card_rank.index(self.values_counter[1][0]) * 2

        return "Pair", self.card_rank.index(self.values_counter[0][0]) * 2

    def compare_with(self, other):
        if self.hand_values.index(self.hand_value[0]) == self.hand_values.index(other.hand_value[0]):
            if self.hand_value[0] == other.hand_value[0] and self.hand_value[1] == other.hand_value[1]:
                return self.RESULT[2]
            return self.RESULT[1] if self.hand_score > other.hand_score else self.RESULT[0]
        return self.RESULT[1] if self.hand_values.index(self.hand_value[0]) > self.hand_values.index(other.hand_value[0]) else self.RESULT[0]


ph1 = PokerHand('KC 4H KS 2H 8D')
ph2 = PokerHand('QH 8H KD JH 8S')
print(ph1.hand_value, ph1.hand_score)
print(ph2.hand_value, ph2.hand_score)
print(ph1.compare_with(ph2))
