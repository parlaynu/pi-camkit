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
    pipes = utils.tee(pipe, count=2, threaded=False)
    
    assert len(pipes) == 2
    
    pipes[0] = utils.worker(pipes[0])
    pipes[1] = utils.worker(pipes[1])
    
    pipe = utils.zip(pipes[0], 'pipe0', pipes[1], 'pipe1')
    
    prev_idx = None
    prev_tag = None
    for item in pipe:
        if prev_idx is None:
            prev_idx = item['idx']
            prev_tag = item['tag']
            continue

        assert item['idx'] == prev_idx
        assert item['tag'] == prev_tag
        
        prev_idx = None
        prev_tag = None



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
    
    pipe = utils.zip(pipes[0], 'pipe0', pipes[1], 'pipe1')
    
    prev_idx = None
    prev_tag = None
    for item in pipe:
        if prev_idx is None:
            prev_idx = item['idx']
            prev_tag = item['tag']
            continue

        assert item['idx'] == prev_idx
        assert item['tag'] == prev_tag
        
        prev_idx = None
        prev_tag = None


def test_tee_grouped():
    
    tags = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def gen():
        for idx, tag in enumerate(tags):
            item = {
                'idx': idx,
                'tag': tag
            }
            yield item
    
    pipe = gen()
    pipes = utils.tee(pipe, count=2, threaded=False)
    
    assert len(pipes) == 2
    
    pipes[0] = utils.worker(pipes[0])
    pipes[1] = utils.worker(pipes[1])
    
    pipe = utils.zip(pipes[0], 'pipe0', pipes[1], 'pipe1', grouped=True)
    
    for items in pipe:
        assert items[0]['idx'] == items[1]['idx']
        assert items[0]['tag'] == items[1]['tag']


def test_tee_threaded_grouped():
    
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
    
    pipe = utils.zip(pipes[0], 'pipe0', pipes[1], 'pipe1', grouped=True)
    
    for items in pipe:
        assert items[0]['idx'] == items[1]['idx']
        assert items[0]['tag'] == items[1]['tag']

