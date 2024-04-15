import time
import sys


def limit(pipe, *, max_frames=sys.maxsize, max_seconds=sys.maxsize):
    print("Building picamkit.ops.utils.limit")
    if max_frames < sys.maxsize:
        print(f"- max_frames: {max_frames}")
    if max_seconds < sys.maxsize:
        print(f"- max_seconds: {max_seconds}")

    def gen():
        start = time.monotonic()
        for count, item in enumerate(pipe, start=1):
            runtime = time.monotonic() - start
            if count > max_frames or runtime > max_seconds:
                break
        
            yield item

    return gen
