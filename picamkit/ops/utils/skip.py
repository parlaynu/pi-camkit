import time


def timeskip(pipe, *, seconds=1.0):
    print("Building picamkit.ops.utils.timeskip")
    print(f"- seconds: {seconds}")
    
    def gen():
        start = time.monotonic()
        for item in pipe:
            if time.monotonic() - start < seconds:
                continue
            start = time.monotonic()
            yield item

    return gen()


def frameskip(pipe, *, frames=24):
    print("Building picamkit.ops.utils.timeskip")
    print(f"- frames: {frames}")

    def gen():
        for idx, item in enumerate(pipe):
            if idx % frames != 0:
                continue
            yield item

    return gen()
