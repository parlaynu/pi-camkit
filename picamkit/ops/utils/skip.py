from typing import Generator
import time


def timeskip(pipe: Generator[dict, None, None], *, seconds: float=1.0) -> Generator[dict, None, None]:
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


def frameskip(pipe: Generator[dict, None, None], *, frames: int = 24) -> Generator[dict, None, None]:
    print("Building picamkit.ops.utils.timeskip")
    print(f"- frames: {frames}")

    def gen():
        for idx, item in enumerate(pipe):
            if idx % frames != 0:
                continue
            yield item

    return gen()
