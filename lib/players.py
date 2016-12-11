import collections
import copy
import dominoes
import itertools
import lib.search
import multiprocessing
import random as rand

def _players(starting_player):
    player = starting_player
    while True:
        yield player
        player = (player + 1) % 4

def _missing(game):
    missing = [set() for player in range(4)]
    board = dominoes.SkinnyBoard()
    for player, move in zip(_players(game.starting_player), game.moves):
        if move is None:
            missing[player].update([board.left_end(), board.right_end()])
        elif move[1]:
            board.add_left(move[0])
        else:
            board.add_right(move[0])

    return missing

def random(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda _: rand.random()))

def bota_flaca(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first + m[0].second))

def bota_gorda(game):
    bota_flaca(game)
    game.valid_moves = tuple(reversed(game.valid_moves))

def double(game):
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first != m[0].second))

def not_double(game):
    double(game)
    game.valid_moves = tuple(reversed(game.valid_moves))

def match(game):
    try:
        left_end = game.board.left_end()
        right_end = game.board.right_end()
    except dominoes.EmptyBoardException:
        return

    not_move_matches = lambda m: tuple(m[0]) not in [(left_end, right_end), (right_end, left_end)]
    game.valid_moves = tuple(sorted(game.valid_moves, key=not_move_matches))

def not_match(game):
    match(game)
    game.valid_moves = tuple(reversed(game.valid_moves))

def attack(game):
    missing = _missing(game)
    next_player_maybe_has = set(range(7)) - missing[(game.turn + 1) % 4]
    def num_options(move):
        board_copy = dominoes.SkinnyBoard.from_board(game.board)

        if move[1]:
            board_copy.add_left(move[0])
        else:
            board_copy.add_right(move[0])

        ends = set([board_copy.left_end(), board_copy.right_end()])
        return len(next_player_maybe_has & ends)

    game.valid_moves = tuple(sorted(game.valid_moves, key=num_options))

def not_attack(game):
     attack(game)
     game.valid_moves = tuple(reversed(game.valid_moves))

def hands_alphabeta(args):
    game, hands = args
    other_players = [p for p in range(len(game.hands)) if p != game.turn]
    for player, hand in zip(other_players, hands):
        game.hands[player] = hand

    game.skinny_board()

    return lib.search.alphabeta(game, key=lambda m: m[0].first != m[0].second)[0][0]

def all_possible_hands_player(min_board_length, num_processes=None):
    def all_possible_hands(game):
        if len(game.board) >= min_board_length and len(game.valid_moves) > 1:
            counter = collections.Counter()
            hands = list(lib.search.all_possible_hands(game, _missing(game)))
            try:
                hands = rand.sample(hands, 100)
            except ValueError:
                pass

            with multiprocessing.Pool(num_processes) as pool:
                for move in pool.imap_unordered(hands_alphabeta, ((game, h) for h in hands)):
                    counter.update([move])

            game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: -counter[m]))

    return all_possible_hands

def double_attack_bota_gorda(game):
    bota_gorda(game)
    attack(game)
    double(game)

def all_possible_hands_double_attack_bota_gorda_player(min_board_length, num_processes=None):
    _all_possible_hands = all_possible_hands_player(min_board_length, num_processes=num_processes)
    def all_possible_hands_double_attack_bota_gorda(game):
        double_attack_bota_gorda(game)
        _all_possible_hands(game)

    return all_possible_hands_double_attack_bota_gorda

def omniscient(game):
    game_copy = copy.deepcopy(game)
    game_copy.skinny_board()
    moves, _ = lib.search.alphabeta(game_copy, key=lambda m: m[0].first != m[0].second)
    game.valid_moves = (moves[0],) + tuple(m for m in game.valid_moves if m != moves[0])
