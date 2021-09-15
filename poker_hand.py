from collections import Counter


class PokerHand(object):
    RESULT = ["Loss", "Win", "Tie"]

    CD_VALUES = "23456789TJQKA"
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
        hand_cards = sorted(hand.split(" "), key=lambda c: self.CD_VALUES.index(c[0]))
        self.hand_values = [v[0] for v in hand_cards]
        self.kicker_vals = []
        self.win_vals = []
        self.same_vals_amount = []
        for val, amount in Counter([c[0] for c in hand_cards]).items():
            if amount == 1:
                self.kicker_vals.append(val)
            elif amount > 1:
                self.win_vals.append(val)
                self.same_vals_amount.append(amount)
        self.kicker_vals.sort(key=lambda v: self.CD_VALUES.index(v))
        self.win_vals.sort(key=lambda d: self.CD_VALUES.index(d[0]))
        self.same_suit = any(hand.count(suit) == 5 for suit in "CHDS")
        self.rank = self.parse_hand()

    def parse_hand(self):
        if len(self.kicker_vals) == 5 and ''.join(self.hand_values) in self.CD_VALUES:
            # straight
            return self.parse_straight()

        if self.same_suit:
            return "Flush"

        if len(self.kicker_vals) < 5:
            return self.parse_pairs()

        return "Highcard"

    def parse_straight(self):
        if self.same_suit:
            return "Royal flush" if self.kicker_vals[0] == "T" else "Straight flush"
        return "Straight"

    def parse_pairs(self):
        min_cnt = min(self.same_vals_amount)
        max_cnt = max(self.same_vals_amount)
        if max_cnt == 4:
            return "Four of a kind"
        if max_cnt == 3 and min_cnt == 2:
            return "Full house"
        if max_cnt == 3:
            return "Three of a kind"
        if max_cnt == 2 and len(self.win_vals) == 2:
            return "Two pairs"
        return "Pair"

    def rank_of(self, hand_values):
        return sum(self.CD_VALUES.index(v) for v in hand_values)

    def compare_with(self, other):
        if self.HD_RANK.index(self.rank) > self.HD_RANK.index(other.rank):
            return self.RESULT[1]
        if self.HD_RANK.index(self.rank) < self.HD_RANK.index(other.rank):
            return self.RESULT[0]
        # compare Tie
        for wval, other_wval in zip(self.win_vals, other.win_vals):
            if self.CD_VALUES.index(wval[0]) > self.CD_VALUES.index(other_wval[0]):
                return self.RESULT[1]
            if self.CD_VALUES.index(wval[0]) < self.CD_VALUES.index(other_wval[0]):
                return self.RESULT[0]
        else:
            # compare kicker values
            for kval, other_kval in list(zip(self.kicker_vals, other.kicker_vals))[::-1]:
                if self.CD_VALUES.index(kval) > self.CD_VALUES.index(other_kval):
                    return self.RESULT[1]
                if self.CD_VALUES.index(kval) < self.CD_VALUES.index(other_kval):
                    return self.RESULT[0]
            return self.RESULT[2]


ph1 = PokerHand('3D 2H 3H 2C 2D')
ph2 = PokerHand('2H 2C 3S 3H 3D')
print(ph1.rank, ph1.win_vals, ph1.kicker_vals)
print(ph2.rank, ph2.win_vals, ph2.kicker_vals)
print(ph1.compare_with(ph2))
