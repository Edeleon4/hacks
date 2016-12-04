import dominoes
import itertools
import lib.players

STARTS_PER_PLAYER = 1000

PLAYERS = (
    lib.players.random,
    lib.players.bota_gorda
)

INITIAL_ELO = 1500
K_FACTOR = .1
MAGNIFICATION_INTERVAL = 400
MAGNIFICATION_FACTOR = 10

TEAMS = tuple(itertools.combinations_with_replacement(PLAYERS, 2))

ELO = {team: INITIAL_ELO for team in TEAMS}

PAIRINGS = tuple(itertools.combinations(TEAMS, 2))

# print config info
print('STARTS_PER_PLAYER:', STARTS_PER_PLAYER)
print('PLAYERS:')
for player in PLAYERS:
    print('    {}'.format(player.__name__))
print()

def update_elo(elo0, elo1, actual_outcome0, actual_outcome1):
    relative_elo0 = pow(MAGNIFICATION_FACTOR, elo0 / MAGNIFICATION_INTERVAL)
    relative_elo1 = pow(MAGNIFICATION_FACTOR, elo1 / MAGNIFICATION_INTERVAL)

    elo_normalization_constant = relative_elo0 + relative_elo1

    expected_outcome_ratio0 = relative_elo0 / elo_normalization_constant
    expected_outcome_ratio1 = relative_elo1 / elo_normalization_constant

    total_score = actual_outcome0 + actual_outcome1

    expected_outcome0 = total_score * expected_outcome_ratio0
    expected_outcome1 = total_score * expected_outcome_ratio1

    updated_elo0 = elo0 + K_FACTOR * (actual_outcome0 - expected_outcome0)
    updated_elo1 = elo1 + K_FACTOR * (actual_outcome1 - expected_outcome1)

    return updated_elo0, updated_elo1

def play(team0, team1, starts_per_player):
    # set playing order
    players = (
        team0[0],
        team1[0],
        team0[1],
        team1[1]
    )

    # to keep track of how many times each team wins
    wins = [0, 0]

    # to keep track of how many points each team scores
    points = [0, 0]

    for p in range(len(players)):
        for _ in range(starts_per_player):
            game = dominoes.Game.new(starting_player=p)
            while game.result is None:
                game.make_move(*players[game.turn](game)[0])

            if not game.result.points:
                # tie
                wins[0] += .5
                wins[1] += .5
            else:
                # compute winning team and points won
                winning_team = game.result.player % 2
                pts = game.result.points
                if pts < 0:
                    winning_team = (winning_team + 1) % 2
                    pts = -pts

                # record the result
                wins[winning_team] += 1
                points[winning_team] += pts

    return wins, points

for team0, team1 in PAIRINGS:
    # print teams
    print('Team 0:', [team0[0].__name__, team0[1].__name__])
    print('Team 1:', [team1[0].__name__, team1[1].__name__])

    # play
    wins, points = play(team0, team1, STARTS_PER_PLAYER)

    # print outcome
    print('Wins:', wins)
    print('Points:', points)
    print()

    # update_elo
    ELO[team0], ELO[team1] = update_elo(ELO[team0], ELO[team1], wins[0], wins[1])

print('Elo ratings:')
for (player0, player1), elo in sorted(ELO.items(), key=lambda team_elo: -team_elo[1]):
    print('    {}: {}'.format((player0.__name__, player1.__name__), int(elo)))
