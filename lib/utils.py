import contextlib
import time

class Timer:
    pass

@contextlib.contextmanager
def timer():
    t = Timer()
    start = time.time()
    yield t
    t.elapsed = time.time() - start
