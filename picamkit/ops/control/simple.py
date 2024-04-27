import time
from functools import partial
from itertools import count, islice


def simple(fps=0, max_frames=0):
    print(f"Building picamkit.ops.control.simple")
    if fps > 0:
        print(f"- fps: {fps}")
    if max_frames > 0:
        print(f"- max_frames: {max_frames}")
    
    def gen():
        loop = count
        if max_frames > 0:
            loop = partial(range, max_frames)
    
        loop_time = 1.0/fps if fps > 0 else 0
    
        start = time.monotonic()
        for idx in loop():
            item = {
                'stamp': time.monotonic_ns(),
                'idx': idx
            }
            yield item

            delay = loop_time - (time.monotonic() - start)
            if delay > 0:
                time.sleep(delay)
            start = time.monotonic()

    return gen()
