import copy
import dominoes
import lib

FIXED_MOVES = 6
SERIAL_DEPTH = 4

print('FIXED_MOVES:', FIXED_MOVES)
print('SERIAL_DEPTH:', SERIAL_DEPTH)

# initializing random game
game = dominoes.Game.new()

# play moves at random
for _ in range(FIXED_MOVES):
    game.make_move(*game.valid_moves[0])

# switch to SkinnyBoard representation
game.skinny_board()

# run minimax
with lib.utils.timer() as t_minimax:
    moves, score = lib.search.minimax(copy.deepcopy(game))
print('minimax took', t_minimax.elapsed, 'seconds and produced a score of', score, 'with moves:')
print(moves)

# run parallel minimax
with lib.utils.timer() as t_parallel_minimax:
    moves, score = lib.search.parallel_minimax(copy.deepcopy(game), SERIAL_DEPTH)
print('parallel minimax took', t_parallel_minimax.elapsed, 'seconds and produced a score of', score, 'with moves:')
print(moves)

# run alphabeta
with lib.utils.timer() as t_alphabeta:
    moves, score = lib.search.alphabeta(copy.deepcopy(game))
print('alphabeta took', t_alphabeta.elapsed, 'seconds and produced a score of', score, 'with moves:')
print(moves)

# run parallel alphabeta
with lib.utils.timer() as t_parallel_alphabeta:
    moves, score = lib.search.parallel_alphabeta(copy.deepcopy(game), SERIAL_DEPTH)
print('parallel alphabeta took', t_parallel_alphabeta.elapsed, 'seconds and produced a score of', score, 'with moves:')
print(moves)

# run double-sorted alphabeta
with lib.utils.timer() as t_double_sorted_alphabeta:
    moves, score = lib.search.alphabeta(copy.deepcopy(game), key=lambda m: m[0].first != m[0].second)
print('double-sorted alphabeta took', t_double_sorted_alphabeta.elapsed, 'seconds and produced a score of', score, 'with moves:')
print(moves)

print('parallel minimax / minimax:', t_parallel_minimax.elapsed / t_minimax.elapsed)
print('alphabeta / parallel minimax:', t_alphabeta.elapsed / t_parallel_minimax.elapsed)
print('parallel alphabeta / alphabeta:', t_parallel_alphabeta.elapsed / t_alphabeta.elapsed)
print('double-sorted alphabeta / alphabeta:', t_double_sorted_alphabeta.elapsed / t_alphabeta.elapsed)
