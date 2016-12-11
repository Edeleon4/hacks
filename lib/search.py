import copy
import dominoes
import lib.utils as utils
import multiprocessing
import operator

def all_possible_hands(game):
    other_hands = tuple(h for p, h in enumerate(game.hands) if p != game.turn)
    other_dominoes = tuple(d for h in other_hands for d in h)
    other_hand_sizes = tuple(len(h) for h in other_hands)

    for hands in utils.partitions(other_dominoes, other_hand_sizes):
        yield tuple(dominoes.Hand(h) for h in hands)

def make_moves(game, key=None):
    sorted_moves = sorted(game.valid_moves, key=key)
    for move in sorted_moves[:-1]:
        new_game = copy.deepcopy(game)
        new_game.make_move(*move)
        yield move, new_game

    move = sorted_moves[-1]
    game.make_move(*move)
    yield move, game

def minimax(game):
    if game.result is not None:
        return [], pow(-1, game.result.player) * game.result.points

    if game.turn % 2:
        best_value = float('inf')
        op = operator.lt
    else:
        best_value = -float('inf')
        op = operator.gt

    for move, new_game in make_moves(game):
        moves, value = minimax(new_game)
        if op(value, best_value):
            best_value = value
            best_moves = moves
            best_moves.insert(0, move)
    return best_moves, best_value

class Node:
    def __init__(self, game, moves):
        self.game = game
        self.turn = game.turn
        self.parent_moves = moves

def node_bfs(node, depth):
    nodes = [node]
    for _ in range(depth):
        new_nodes = []
        for node in nodes:
            node.children = []
            for move, game in make_moves(node.game):
                child = Node(game, node.parent_moves + [move])
                node.children.append(child)
                new_nodes.append(child)
            node.game = None

        nodes = new_nodes

    return nodes

def node_minimax(node):
    try:
        return node.parent_moves + node.child_moves, node.value
    except AttributeError:
        pass

    if node.turn % 2:
        op = min
    else:
        op = max

    return op(
        (node_minimax(child) for child in node.children),
        key=lambda moves_value: moves_value[1]
    )

def naive_parallel_search(search_f, game, serial_depth, num_processes, chunk_size):
    # first, BFS from the root game to a certain depth
    root = Node(game, [])
    nodes = node_bfs(root, serial_depth)

    # then, run the search function, in parallel,
    # on all the games in the BFS frontier.
    with multiprocessing.Pool(num_processes) as pool:
        imap = pool.imap(search_f, (n.game for n in nodes), chunk_size)
        for node, (best_moves, best_value) in zip(nodes, imap):
            node.game = None
            node.child_moves = best_moves
            node.value = best_value

    # finally, run serial minimax from the root to the BFS frontier
    return node_minimax(root)

def parallel_minimax(game, serial_depth, num_processes=None, chunk_size=1):
    return naive_parallel_search(
        minimax, game, serial_depth,
        num_processes=num_processes,
        chunk_size=chunk_size
    )

def alphabeta(game, alpha_beta=(-float('inf'), float('inf')), key=None):
    if game.result is not None:
        return [], pow(-1, game.result.player) * game.result.points

    if game.turn % 2:
        best_value = float('inf')
        op = operator.lt
        update = lambda ab, v: (ab[0], min(ab[1], v))
    else:
        best_value = -float('inf')
        op = operator.gt
        update = lambda ab, v: (max(ab[0], v), ab[1])

    for move, new_game in make_moves(game, key):
        moves, value = alphabeta(new_game, alpha_beta, key)
        if op(value, best_value):
            best_value = value
            best_moves = moves
            best_moves.insert(0, move)
            alpha_beta = update(alpha_beta, best_value)
            if alpha_beta[1] <= alpha_beta[0]:
                break
    return best_moves, best_value

def parallel_alphabeta(game, serial_depth, num_processes=None, chunk_size=1):
    return naive_parallel_search(
        alphabeta, game, serial_depth,
        num_processes=num_processes,
        chunk_size=chunk_size
    )
