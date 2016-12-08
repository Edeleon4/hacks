import dominoes
import itertools
import lib.elo
import lib.players
import tqdm

STARTS_PER_PLAYER = 1000

PLAYERS = (
    lib.players.random,
    lib.players.bota_gorda,
    lib.players.double,
    lib.players.double_bota_gorda
)

INITIAL_ELO = 1500

#TEAMS = tuple(itertools.combinations_with_replacement(PLAYERS, 2))
TEAMS = tuple((player, player) for player in PLAYERS)

ELO = {team: INITIAL_ELO for team in TEAMS}

PAIRINGS = tuple(itertools.combinations(TEAMS, 2))

RECORDS = {pairing: [0, 0] for pairing in PAIRINGS}

# print config info
print('STARTS_PER_PLAYER:', STARTS_PER_PLAYER)
print('PLAYERS:')
for player in PLAYERS:
    print('    {}'.format(player.__name__))
print()
print('TEAMS:')
for (player0, player1) in TEAMS:
    print('    ({}, {})'.format(player0.__name__, player1.__name__))
print()

def play_game(team0, team1, starting_player):
    # set playing order
    players = (
        team0[0],
        team1[0],
        team0[1],
        team1[1]
    )

    game = dominoes.Game.new(starting_player=starting_player)
    while game.result is None:
        players[game.turn](game)
        game.make_move(*game.valid_moves[0])

    if not game.result.points:
        # tie
        return [.5, .5]
    else:
        # win/loss
        winning_team_offset = int(game.result.points < 0)
        winning_team = (game.result.player + winning_team_offset) % 2

        outcome = [0, 0]
        outcome[winning_team] = 1

        return outcome

for _ in tqdm.trange(STARTS_PER_PLAYER, leave=False):
    for starting_player in range(4):
        for team0, team1 in PAIRINGS:
            # play game
            score0, score1 = play_game(team0, team1, starting_player)

            # update records
            RECORDS[(team0, team1)][0] += score0
            RECORDS[(team0, team1)][1] += score1

            # update_elo
            ELO[team0], ELO[team1] = lib.elo.update(ELO[team0], ELO[team1], score0, score1)

print('Records:')
for ((player0, player2), (player1, player3)), record in sorted(RECORDS.items(), key=lambda pairing_record: pairing_record[1][1]):
    print('   ({}, {}) vs ({}, {}): {}'.format(player0.__name__, player2.__name__, player1.__name__, player3.__name__, record))

print('Elo ratings:')
for (player0, player1), elo in sorted(ELO.items(), key=lambda team_elo: -team_elo[1]):
    print('    {}: {}'.format((player0.__name__, player1.__name__), int(elo)))
