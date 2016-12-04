import dominoes
import lib.players

STARTS_PER_PLAYER = 25

players = [
    lib.players.random,
    lib.players.random,
    lib.players.random,
    lib.players.random
]

for p in range(len(players)):
    for _ in range(STARTS_PER_PLAYER):
        print('Player {} starting:'.format(p))
        game = dominoes.Game.new(starting_player=p)
        while game.result is None:
            game.make_move(*players[game.turn](game)[0])
        print(game.result)
