import time


def warmup(pipe, *, frames=0, seconds=0):
    print("Building picamkit.ops.utils.warmup")
    if frames > 0:
        print(f"- frames: {frames}")
    if seconds > 0:
        print(f"- seconds: {seconds}")

    def gen():
        print("Warmup running")
        warm = False
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            runtime = time.monotonic() - start
            if idx < frames or runtime < seconds:
                continue
        
            if warm == False:
                print("Warmup finished")
                warm = True
        
            yield item

    return gen()
