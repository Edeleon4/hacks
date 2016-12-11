import dominoes
import lib.utils as utils

FIXED_MOVES = 10

print('FIXED_MOVES:', FIXED_MOVES)

def all_possible_hands(game):
    other_hands = tuple(h for p, h in enumerate(game.hands) if p != game.turn)
    other_dominoes = tuple(d for h in other_hands for d in h)
    other_hand_sizes = tuple(len(h) for h in other_hands)

    for hands in utils.partitions(other_dominoes, other_hand_sizes):
        yield tuple(dominoes.Hand(h) for h in hands)

# initialize random game
game = dominoes.Game.new()

# play moves at random
for _ in range(FIXED_MOVES):
    game.make_move(*game.valid_moves[0])

# calculate expected amount of possible hands
other_hand_lengths = [len(h) for p, h in enumerate(game.hands) if p != game.turn]
expected_count = utils.nCk(sum(other_hand_lengths), other_hand_lengths[0]) * \
    utils.nCk(other_hand_lengths[1] + other_hand_lengths[2], other_hand_lengths[1])

# count all possible hands
with utils.timer() as t:
    count = 0
    for _ in all_possible_hands(game):
        count += 1

assert count == expected_count, \
    'Counted {}, expected {}'.format(count, expected_count)

print('Found', count, 'possible hands in', t.elapsed, 'seconds')
