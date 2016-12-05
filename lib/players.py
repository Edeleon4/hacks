import copy
import lib.search
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

def double_bota_gorda(game):
    bota_gorda(game)
    double(game)

def omniscient(game):
    game_copy = copy.deepcopy(game)
    game_copy.skinny_board()
    moves, _ = lib.search.alphabeta(game_copy, key=lambda m: m[0].first != m[0].second)
    game.valid_moves = (moves[0],) + tuple(m for m in game.valid_moves if m != moves[0])
