from typing import Generator
import time


def warmup(
    pipe: Generator[dict, None, None], 
    *, 
    frames: int = 0, 
    seconds: float = 0
) -> Generator[dict, None, None]:

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
