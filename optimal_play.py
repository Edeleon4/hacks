import contextlib
import copy
import dominoes
import operator
import time

FIXED_MOVES = 6

@contextlib.contextmanager
def timer(action):
    start = time.time()
    yield
    elapsed = time.time() - start
    print(action, 'took', int(elapsed), 'seconds')

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

def alphabeta(game, alpha_beta=(-float('inf'), float('inf'))):
    if game.result is not None:
        return pow(-1, game.result.player) * game.result.points

    if game.turn % 2:
        best_value = float('inf')
        op = operator.lt
        update = lambda ab, v: (ab[0], min(ab[1], v))
    else:
        best_value = -float('inf')
        op = operator.gt
        update = lambda ab, v: (max(ab[0], v), ab[1])

    for _, new_game in make_moves(game):
        value = alphabeta(new_game, alpha_beta)
        if op(value, best_value):
            best_value = value
            alpha_beta = update(alpha_beta, best_value)
            if alpha_beta[1] <= alpha_beta[0]:
                break
    return best_value

# initializing random game
game = dominoes.Game.new()

# play moves at random
for _ in range(FIXED_MOVES):
    game.make_move(*game.valid_moves[0])

# run minimax
with timer('minimax'):
    game_copy = copy.deepcopy(game)
    game_copy.skinny_board()
    print(minimax(game_copy))

# run alphabeta
with timer('alphabeta'):
    game_copy = copy.deepcopy(game)
    game_copy.skinny_board()
    print(alphabeta(game_copy))
