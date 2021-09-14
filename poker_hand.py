from collections import Counter


class PokerHand(object):
    RESULT = ["Loss", "Win", "Tie"]

    CD_RANK = "23456789TJQKA"
    HD_RANK = ["Highcard",
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
        hand_cards = hand.split(" ")
        self.hand_values = sorted([v[0] for v in hand_cards], key=lambda v: self.CD_RANK.index(v))
        self.values_counter = Counter([c[0] for c in hand_cards]).most_common()
        self.suits_counter = Counter([c[1] for c in hand_cards]).most_common()
        self.hand_rank = self.define_hand_rank_data()

    def define_hand_rank_data(self):
        rank_val = self.rank_of(self.hand_values)
        if all(self.CD_RANK.index(self.hand_values[i]) + 1 == self.CD_RANK.index(self.hand_values[i + 1]) for i
               in range(4)):
            # straight
            return self.handle_straight(), rank_val

        if len(self.suits_counter) == 1:
            return "Flush", rank_val

        if len(self.values_counter) < 5:
            return self.handle_pairs(), rank_val

        return "Highcard", rank_val

    def handle_straight(self):
        if len(self.suits_counter) == 1:
            return "Royal flush" if self.rank_of(self.hand_values) == 50 else "Straight flush"
        return "Straight"

    def handle_pairs(self):
        min_cnt = min(vc[1] for vc in self.values_counter)
        max_cnt = max(vc[1] for vc in self.values_counter)
        rank = "Pair"
        if max_cnt == 4:
            rank = "Four of a kind"
        elif max_cnt == 3 and min_cnt == 2:
            rank = "Full house"
        elif max_cnt == 3:
            rank = "Three of a kind"
        elif max_cnt == 2 and len(self.values_counter) == 3:
            rank = "Two pairs"
        return rank

    def rank_of(self, hand_values):
        return sum(self.CD_RANK.index(v) for v in hand_values)

    def compare_with(self, other):
        if self.hand_rank == other.hand_rank:
            return self.RESULT[2]
        if self.hand_rank[0] == other.hand_rank[0]:
            return self.RESULT[0] if self.hand_rank[1] < other.hand_rank[1] else self.RESULT[1]
        return self.RESULT[1] if self.HD_RANK.index(self.hand_rank[0]) > self.HD_RANK.index(
            other.hand_rank[0]) else self.RESULT[0]


ph1 = PokerHand('KC 4H KS 2H 8D')
ph2 = PokerHand('8C 4S KH JS 4D')
print(ph1.hand_rank)
print(ph2.hand_rank)
print(ph1.compare_with(ph2))
