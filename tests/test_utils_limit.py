from itertools import chain
import pytest
import time
import numpy as np
import picamkit.ops.utils as utils


def test_limit():
    
    tags = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def gen():
        for idx, tag in enumerate(tags):
            item = {
                'idx': idx,
                'tag': tag
            }
            yield item
    
    max_frames = 5

    pipe = gen()
    pipe = utils.limit(pipe, max_frames=max_frames)
    
    for idx, item in enumerate(pipe):
        pass
    
    assert idx == max_frames-1
    assert item['tag'] == tags[idx]

