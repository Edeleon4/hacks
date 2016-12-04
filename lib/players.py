import random as rand

def random(game):
    moves = list(game.valid_moves)
    rand.shuffle(moves)
    return moves

def bota_gorda(game):
    return sorted(game.valid_moves, key=lambda m: m[0].first + m[0].second, reverse=True)
