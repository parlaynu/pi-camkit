import time


def rate_limit(pipe, fps):
    print("Building picamkit.ops.utils.rate_limit")
    print(f"- fps: {fps}")
    
    loop_time = 1.0/fps if fps > 0 else 0

    def gen():
        start = time.monotonic()
        for item in pipe:
            yield item
        
            delay = loop_time - (time.monotonic() - start)
            if delay > 0:
                time.sleep(delay)
            start = time.monotonic()

    return gen()
