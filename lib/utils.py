import contextlib
import time

@contextlib.contextmanager
def timer(action):
    start = time.time()
    yield
    elapsed = time.time() - start
    print(action, 'took', elapsed, 'seconds')
