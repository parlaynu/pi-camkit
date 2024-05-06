from itertools import chain
import pytest
import time
import numpy as np
import picamkit.ops.utils as utils


def test_tee():
    
    tags = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def gen():
        for idx, tag in enumerate(tags):
            item = {
                'idx': idx,
                'tag': tag
            }
            yield item
    
    pipe = gen()
    pipes = utils.tee(pipe, count=2)
    
    assert len(pipes) == 2
    
    for item1, item2 in zip(*pipes):
        assert item1['idx'] == item2['idx']
        assert item1['tag'] == item2['tag']


def test_tee_threaded():
    
    tags = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def gen():
        for idx, tag in enumerate(tags):
            item = {
                'idx': idx,
                'tag': tag
            }
            yield item
    
    pipe = gen()
    pipes = utils.tee(pipe, count=2, threaded=True)
    
    assert len(pipes) == 2
    
    pipes[0] = utils.worker(pipes[0])
    pipes[1] = utils.worker(pipes[1])
    
    for item1, item2 in zip(*pipes):
        assert item1['idx'] == item2['idx']
        assert item1['tag'] == item2['tag']

