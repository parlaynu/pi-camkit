from typing import Generator, Iterable
import collections
import threading
import time


# based on itertools.tee with the following differences:
# - add a copy of the item to each deque rather than the same item
# - return the generators in a list so the builder can mutate it
# - safe for generators to be called from different threads

def tee(pipe: Generator[dict, None, None], *, count: int, threaded: bool = False) -> Iterable[Generator[dict, None, None]]:
    print("Building picamkit.ops.utils.tee")
    print(f"- count: {count}")

    barrier = threading.Barrier(count)
    lock = threading.Lock()
    deques = [collections.deque() for i in range(count)]

    def gen(mydeque):
        tid = threading.get_ident()
    
        while True:
            # using a barrier to ensure that all threads get a chance to
            # execute the code that follows before any one thread can 
            # loop through again.
            if threaded:
                barrier.wait()
            
            with lock:
                if len(mydeque) == 0:
                    try:
                        item = next(pipe)
                    except StopIteration:
                        return
                    
                    for d in deques:
                        d.append(item.copy())

            yield mydeque.popleft()

    return [gen(d) for d in deques]

