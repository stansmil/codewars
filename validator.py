"""
Ships
1 - 4 cell
2 - 3 cell
3 - 2 cell
4 - 1 cell
"""

"""
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
*  *  *  *  *  *  *  *  *  *
"""


def validate(battle_field: list) -> bool:
    # calculate total reserved cells on a field
    if sum(sum(row) for row in battle_field) != 20:
        return False

    for r in range(8):
        row, next_row = battle_field[r:r + 2]
        for i in range(8):
            if sum(row[i:i + 2]) + sum(next_row[i:i + 2]) > 2 or row[i] + next_row[i+1] > 1 or row[i+1] + next_row[i] > 1:
                # adjacent ships
                print("adjacent ships at coords", (r, i), (r + 1, i + 1))
                return False

    deck_4 = 0
    deck_3 = 0
    deck_2 = 0

    for row in battle_field:
        srow = ''.join([str(r) for r in row])
        for deck in srow.split('0'):
            if not deck:
                continue
            if len(deck) == 4:
                deck_4 += 1
            elif len(deck) == 3:
                deck_3 += 1
            elif len(deck) == 2:
                deck_2 += 1

    for column in zip(*battle_field):
        scol = ''.join([str(c) for c in column])
        for deck in scol.split('0'):
            if not deck:
                continue
            if len(deck) == 4:
                deck_4 += 1
            elif len(deck) == 3:
                deck_3 += 1
            elif len(deck) == 2:
                deck_2 += 1
    deck_1 = 20 - 4*deck_4 - 3*deck_3 - 2*deck_2
    print(deck_1, deck_2, deck_3, deck_4)
    return deck_1 == 4 and deck_2 == 3 and deck_3 == 2 and deck_4 == 1


bf = [
    [1,1,1,1,0,0,1,0,0,1],
    [0,0,0,0,0,0,1,0,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,1,1,1,0,0],
    [1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,1],
    [0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0],
    [0,0,0,1,0,0,0,0,0,0],
]

print(validate(bf))
