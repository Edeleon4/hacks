import dominoes
import itertools
import lib.elo
import lib.players
import multiprocessing
import tqdm

# each pair of teams will play each other
# STARTS_PER_PLAYER times for each of the four players
STARTS_PER_PLAYER = 250

# number of moves to play at random, at the start of each game
FIXED_MOVES = 0

# number of processes to use for the round robin.
# if None, uses as many processes as there are processors.
NUM_PROCESSES = 1

# playing strateges to play in the round robin
PLAYERS = (
    lib.players.random,
    lib.players.bota_gorda,
    lib.players.double,
    lib.players.attack,
    lib.players.monte_carlo_random,
    lib.players.compose(
        'double_attack_bota_gorda',
        lib.players.bota_gorda,
        lib.players.attack,
        lib.players.double
    ),
    lib.players.compose(
        'botagorda_attack_double',
        lib.players.bota_gorda,
        lib.players.attack,
        lib.players.double,
    )
)

# Elo rating of each team at the start of the round robin
INITIAL_ELO = 1500

# players on the same team are the same
TEAMS = tuple((player, player) for player in PLAYERS)

# keep track of each team's Elo rating
ELO = {team: INITIAL_ELO for team in TEAMS}

# all pairs of teams
PAIRINGS = tuple(itertools.combinations(TEAMS, 2))

# win-loss records between each team
RECORDS = {pairing: [0, 0] for pairing in PAIRINGS}

# print config info
print('STARTS_PER_PLAYER:', STARTS_PER_PLAYER)
print('FIXED_MOVES:', FIXED_MOVES)
print('NUM_PROCESSES:', NUM_PROCESSES)
print('PLAYERS:')
for player in PLAYERS:
    print('    {}'.format(player.__name__))
print()
print('TEAMS:')
for (player0, player1) in TEAMS:
    print('    ({}, {})'.format(player0.__name__, player1.__name__))
print()

def new_game(*args, **kwargs):
    while True:
        # initialize random game
        game = dominoes.Game.new(*args, **kwargs)

        # play moves at random
        for _ in range(FIXED_MOVES):
            game.make_move(*game.valid_moves[0])

            # make sure that the moves played at random did not end the game
            if game.result is not None:
                break

        # make sure that the moves played at random did not end the game
        if game.result is None:
            return game

# play a single game subject to each player's
# strategy and a given starting player
def play_game(args):
    team0, team1, starting_player = args

    # playing order
    players = (
        team0[0],
        team1[0],
        team0[1],
        team1[1]
    )

    game = new_game(starting_player=starting_player)

    # play the rest of the game
    while game.result is None:
        # each player's strategy function reorders
        # game.valid_moves in order of preference
        players[game.turn](game)
        game.make_move(*game.valid_moves[0])

    if not game.result.points:
        # tie - half a point for each team
        return [.5, .5]
    else:
        # win/loss - 1 point for the winning team,
        #            and 0 points for the losing team
        winning_team_offset = int(game.result.points < 0)
        winning_team = (game.result.player + winning_team_offset) % 2

        outcome = [0, 0]
        outcome[winning_team] = 1

        return outcome

def play_game_args():
    for _ in range(STARTS_PER_PLAYER):
        for starting_player in range(4):
            for team0, team1 in PAIRINGS:
                yield team0, team1, starting_player

with multiprocessing.Pool(NUM_PROCESSES) as pool:
    for (team0, team1, _), (score0, score1) in tqdm.tqdm(zip(play_game_args(),
                                                             pool.imap(play_game, play_game_args())),
                                                         total=len(list(play_game_args()))):
        # update win/loss records
        RECORDS[(team0, team1)][0] += score0
        RECORDS[(team0, team1)][1] += score1

        # update Elo ratings
        ELO[team0], ELO[team1] = lib.elo.update(ELO[team0], ELO[team1],
                                                score0, score1)

# print out win/loss records
print('Records:')
for pairing in PAIRINGS:
    (player0, player2), (player1, player3) = pairing
    record = RECORDS[pairing]
    print('   ({}, {}) vs ({}, {}): {}'.format(player0.__name__, player2.__name__,
                                               player1.__name__, player3.__name__, record))

# print out Elo ratings
print('Elo ratings:')
ratings = sorted(ELO.items(), key=lambda team_elo: -team_elo[1])
for (player0, player1), elo in ratings:
    print('    {}: {}'.format((player0.__name__, player1.__name__), int(elo)))
