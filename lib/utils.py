import contextlib
import itertools
import math
import time

class Timer:
    pass

@contextlib.contextmanager
def timer():
    t = Timer()
    start = time.time()
    yield t
    t.elapsed = time.time() - start

def nCk(n, k):
    return math.factorial(n) // math.factorial(n - k) // math.factorial(k)

def partitions(elements, sizes):
    try:
        size = sizes[0]
    except IndexError:
        yield ()
        raise StopIteration

    remaining_sizes = sizes[1:]

    for partition in itertools.combinations(elements, size):
        remaining_elements = set(elements) - set(partition)
        for other_partitions in partitions(remaining_elements, remaining_sizes):
            yield (partition,) + other_partitions
