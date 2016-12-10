import copy
import dominoes
import multiprocessing
import time

FIXED_MOVES = 0
SERIAL_DEPTH = 8
CHUNK_SIZE = 2

def make_moves(game):
    for move in game.valid_moves[:-1]:
        new_game = copy.deepcopy(game)
        new_game.make_move(*move)
        yield new_game

    game.make_move(*game.valid_moves[-1])
    yield game

def bfs(game, depth):
    games = [game]
    for _ in range(depth):
        new_games = []
        for game in games:
            new_games.extend(make_moves(game))

        games = new_games

    return games

def num_outcomes(game):
    if game.result is not None:
        return 1

    return sum(num_outcomes(new_game) for new_game in make_moves(game))

# initializing random game
game = dominoes.Game.new()

# changing to skinny board representation
game.skinny_board()

# play moves at random
for _ in range(FIXED_MOVES):
    game.make_move(*game.valid_moves[0])

# BFS the first few moves serially
games = bfs(game, SERIAL_DEPTH)

# calculate number of outcomes in parallel
start = time.time()
with multiprocessing.Pool() as pool:
    total_outcomes = 0
    #for i, outcomes in enumerate(map(num_outcomes, games)):
    for i, outcomes in enumerate(pool.imap_unordered(num_outcomes, games, CHUNK_SIZE)):
        fraction_processed = (i + 1) / len(games)
        print('Processed {}/{} games ({}%)'.format(i + 1, len(games),
                                                   int(fraction_processed * 100)))

        total_outcomes += outcomes
        est_total_outcomes = int(total_outcomes / fraction_processed)
        print('Found {}/~{} outcomes'.format(total_outcomes, est_total_outcomes))

        elapsed = time.time() - start
        est_total_time = int(elapsed / fraction_processed)
        print('Elapsed {}/~{} seconds'.format(int(elapsed), est_total_time))

        rate = int(total_outcomes / elapsed)
        print('Finding {} outcomes/second'.format(rate))

        if i != len(games) - 1:
            print()
