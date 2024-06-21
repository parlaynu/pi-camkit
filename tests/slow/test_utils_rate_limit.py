import time
import pytest
import picamkit.ops.utils as utils


@pytest.mark.parametrize('fps', [(1), (5), (20)])
def test_RateLimitIsEnforced(fps):
    
    seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def gen():
        for idx, value in enumerate(seq):
            item = {
                'idx': idx,
                'value': value
            }
            yield item
    
    pipe = gen()
    pipe = utils.rate_limit(pipe, fps=fps)
    
    start = time.monotonic()
    for idx, item in enumerate(pipe):
        pass
    duration = time.monotonic() - start
    
    target_duration = len(seq) / fps
    
    assert pytest.approx(duration, abs=0.05) == target_duration
