import copy
import dominoes
import operator
import time

FIXED_MOVES = 5

def make_moves(game):
    for move in game.valid_moves[:-1]:
        new_game = copy.deepcopy(game)
        new_game.make_move(*move)
        yield move, new_game

    move = game.valid_moves[-1]
    game.make_move(*move)
    yield move, game

def minimax(game):
    if game.result is not None:
        return [], pow(-1, game.result.player) * game.result.points

    if game.turn % 2:
        best_value = float('inf')
        op = operator.lt
    else:
        best_value = -float('inf')
        op = operator.gt

    best_moves = None
    for move, new_game in make_moves(game):
        moves, value = minimax(new_game)
        if op(value, best_value):
            best_value = value
            best_moves = moves
            best_moves.insert(0, move)
    return best_moves, best_value

# initializing random game
game = dominoes.Game.new()

# play moves at random
for _ in range(FIXED_MOVES):
    game.make_move(*game.valid_moves[0])

# copy the game before computing optimal play
orig_game = copy.deepcopy(game)

# changing to skinny board representation
game.skinny_board()

# compute optimal play
start = time.time()
best_moves, _ = minimax(game)
elapsed = time.time() - start
print('Computing optimal play took {} seconds.'.format(int(elapsed)))

# print optimal play
print(orig_game)
for move in best_moves:
    orig_game.make_move(*move)
    print(orig_game)
