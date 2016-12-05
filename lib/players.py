import random as rand

def random(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda _: rand.random()))

def bota_flaca(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first + m[0].second))

def bota_gorda(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: -m[0].first - m[0].second))

def double(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first != m[0].second))

def not_double(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first == m[0].second))
