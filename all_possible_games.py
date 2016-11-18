import copy
import dominoes
import multiprocessing
import tqdm

FIXED_MOVES = 6
SERIAL_DEPTH = 7
NUM_PROCESSES = 8
CHUNK_SIZE = 10

class GameNode:
    def __init__(self, game):
        self.game = game
        self.children = {}

    def leaf_nodes(self):
        if not self.children:
            yield self

        for child in self.children.values():
            yield from child.leaf_nodes()

    def expand(self):
        if self.game is None:
            return

        moves = self.game.valid_moves()
        for move in moves:
            if move == move[-1]:
                new_game = self.game
            else:
                new_game = copy.deepcopy(self.game)

            new_game.make_move(*move)
            self.children[move] = GameNode(new_game)

        self.game = None

    def bfs(self, max_depth=None):
        nodes = [self]
        depth = 0
        while nodes and (max_depth is None or depth < max_depth):
            new_nodes = []
            for node in nodes:
                node.expand()
                new_nodes.extend(node.children.values())

            nodes = new_nodes
            depth += 1

    def minimax(self):
        if self.game.result is not None:
            return pow(-1, self.game.result.player) * self.game.result.points

        turn = self.game.turn

        self.expand()

        if turn % 2:
            return min(child.minimax() for child in self.children.values())
        else:
            return max(child.minimax() for child in self.children.values())

# initializing random game
game = dominoes.Game()

# played moves at random
for _ in range(FIXED_MOVES):
    game.make_move(*game.valid_moves()[0])

# changing to skinny board representation
game.skinny_board()

# initializing game tree
root = GameNode(game)

## running serial BFS
#root.bfs(SERIAL_DEPTH)
#
## leaf nodes after serial BFS
#leaf_nodes = list(root.leaf_nodes())
#
## running parallel BFS
#def bfs(node):
#    node.bfs()
#    return node
#
#with multiprocessing.Pool(NUM_PROCESSES) as pool:
#    searched_nodes = list(
#        tqdm.tqdm(pool.imap_unordered(bfs, leaf_nodes, CHUNK_SIZE),
#                  total=len(leaf_nodes))
#    )
#
## counting total games
#print(
#    'Total games:',
#    sum(len(list(node.leaf_nodes())) for node in searched_nodes)
#)

# running minimax
print(root.minimax())
print(root.minimax())
