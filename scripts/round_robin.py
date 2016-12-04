import dominoes
import itertools
import lib.players

STARTS_PER_PLAYER = 1000

PLAYERS = (
    lib.players.random,
    lib.players.bota_gorda
)

TEAMS = tuple(itertools.combinations_with_replacement(PLAYERS, 2))

PAIRINGS = tuple(itertools.combinations(TEAMS, 2))

# print config info
print('STARTS_PER_PLAYER:', STARTS_PER_PLAYER)
print('PLAYERS:')
for player in PLAYERS:
    print('    {}'.format(player.__name__))
print()

def play(team0, team1, starts_per_player):
    # set playing order
    players = (
        team0[0],
        team1[0],
        team0[1],
        team1[1]
    )

    # print teams
    print('Team 0:', [players[0].__name__, players[2].__name__])
    print('Team 1:', [players[1].__name__, players[3].__name__])

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
                continue

            # compute winning team and points won
            winning_team = game.result.player % 2
            pts = game.result.points
            if pts < 0:
                winning_team = (winning_team + 1) % 2
                pts = -pts

            # record the result
            wins[winning_team] += 1
            points[winning_team] += pts

    print('Wins:', wins)
    print('Points:', points)

for team0, team1 in PAIRINGS:
    play(team0, team1, STARTS_PER_PLAYER)
    print()
