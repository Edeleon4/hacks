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

def run(game, function):
    game_copy = copy.deepcopy(game)
    game_copy.skinny_board()
    print(function(game_copy))

# run minimax
with lib.utils.timer('minimax'):
    run(game, lib.search.minimax)

# run alphabeta
with lib.utils.timer('alphabeta'):
    run(game, lib.search.alphabeta)
