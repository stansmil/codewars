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
        hand_cards = sorted(hand.split(" "), key=lambda c: self.CD_RANK.index(c[0]))
        self.hand_values = [v[0] for v in hand_cards]
        self.kicker_vals = []
        self.win_vals = []
        for val, amount in Counter([c[0] for c in hand_cards]).items():
            if amount == 1:
                self.kicker_vals.append(val)
            elif amount > 1:
                self.win_vals.append((val, amount))
        # sort by card rank
        self.kicker_vals.sort(key=lambda v: self.CD_RANK.index(v), reverse=True)
        # sort by amount
        self.win_vals.sort(key=lambda d: d[1], reverse=True)
        self.same_suit = any(hand.count(suit) == 5 for suit in "CHDS")
        self.rank = self.parse_hand()

    def parse_hand(self):
        if len(self.kicker_vals) == 5 and ''.join(self.hand_values) in self.CD_RANK:
            # straight
            return self.parse_straight()

        if self.same_suit:
            return "Flush"

        if len(self.kicker_vals) < 5:
            return self.parse_pairs()

        return "Highcard"

    def parse_straight(self):
        if self.same_suit:
            return "Royal flush" if self.kicker_vals[0] == "A" else "Straight flush"
        return "Straight"

    def parse_pairs(self):
        wv_amounts = [wv[1] for wv in self.win_vals]
        min_amt, max_amt = min(wv_amounts), max(wv_amounts)
        if max_amt == 4:
            return "Four of a kind"
        if max_amt == 3 and min_amt == 2:
            return "Full house"
        if max_amt == 3:
            return "Three of a kind"
        if max_amt == 2 and len(self.win_vals) == 2:
            return "Two pairs"
        return "Pair"

    def compare_with(self, other):
        if self.HD_RANK.index(self.rank) > self.HD_RANK.index(other.rank):
            return "Win"
        if self.HD_RANK.index(self.rank) < self.HD_RANK.index(other.rank):
            return "Loss"
        # compare Tie
        for wval, other_wval in zip(self.win_vals, other.win_vals):
            if self.CD_RANK.index(wval[0]) > self.CD_RANK.index(other_wval[0]):
                return "Win"
            if self.CD_RANK.index(wval[0]) < self.CD_RANK.index(other_wval[0]):
                return "Loss"
        else:
            # compare kicker values
            for kval, other_kval in zip(self.kicker_vals, other.kicker_vals):
                if self.CD_RANK.index(kval) > self.CD_RANK.index(other_kval):
                    return "Win"
                if self.CD_RANK.index(kval) < self.CD_RANK.index(other_kval):
                    return "Loss"
            return "Tie"


ph1 = PokerHand('2H 2C 3S 3H 3D')
ph2 = PokerHand('3D 2H 3H 2C 2D')
print(ph1.rank, ph1.win_vals, ph1.kicker_vals)
print(ph2.rank, ph2.win_vals, ph2.kicker_vals)
print(ph1.compare_with(ph2))
