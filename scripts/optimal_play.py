import copy
import dominoes
import lib

FIXED_MOVES = 5

print('FIXED_MOVES:', FIXED_MOVES)

# initializing random game
game = dominoes.Game.new()

# play moves at random
for _ in range(FIXED_MOVES):
    game.make_move(*game.valid_moves[0])

# switch to SkinnyBoard representation
game.skinny_board()

# run minimax
with lib.utils.timer() as t_minimax:
    _, score = lib.search.minimax(copy.deepcopy(game))
print('minimax took', t_minimax.elapsed, 'seconds and produced a score of', score)

# run alphabeta
with lib.utils.timer() as t_alphabeta:
    _, score = lib.search.alphabeta(copy.deepcopy(game))
print('alphabeta took', t_alphabeta.elapsed, 'seconds and produced a score of', score)
