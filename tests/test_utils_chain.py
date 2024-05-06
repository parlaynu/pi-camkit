from itertools import chain
import pytest
import time
import numpy as np
import picamkit.ops.utils as utils


def test_chain():
    
    tags1 = ['a', 'b', 'c']
    tags2 = ['d', 'e', 'f']
    
    def gen1():
        for idx, tag in enumerate(tags1):
            item = {
                'idx': idx,
                'tag': tag
            }
            yield item
    
    def gen2():
        for idx, tag in enumerate(tags2):
            item = {
                'idx': idx,
                'tag': tag
            }
            yield item

    pipe1 = gen1()
    pipe2 = gen2()
    
    pipe = utils.chain(pipe1, 'pipe1', pipe2, 'pipe2')
    
    for item, tag in zip(pipe, chain(tags1, tags2)):
        assert item['tag'] == tag

