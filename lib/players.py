import random as rand

def random(game):
    moves = list(game.valid_moves)
    rand.shuffle(moves)
    return moves
