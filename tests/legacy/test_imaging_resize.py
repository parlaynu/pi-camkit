import pytest
import time
import numpy as np
import picamkit.ops.imaging as imaging


def test_resize():
    
    sizes = [(1024, 1024, 3), (512, 512, 3), (2048, 2048, 3)]
    
    def gen():
        for idx, size in enumerate(sizes):
            image = np.random.randint(0, 255, size, np.uint8)
            item = {
                'idx': idx,
                'main': {
                    'image': image
                }
            }
            yield item
    
    pipe = gen()
    pipe = imaging.resize(pipe, width=720, height=480)
    
    for item in pipe:
        img = item['main']['image']
        assert img.shape == (480, 720, 3)
        assert img.dtype == np.uint8


def test_scale():
    
    sizes = [(1024, 1024, 3), (512, 512, 3), (2048, 2048, 3)]
    
    def gen():
        for idx, size in enumerate(sizes):
            image = np.random.randint(0, 255, size, np.uint8)
            item = {
                'idx': idx,
                'main': {
                    'image': image
                }
            }
            yield item
        
    factors = [0.5, 2.0, 0.25, 0.1]
    for factor in factors:
        pipe = gen()
        pipe = imaging.scale(pipe, factor=factor)
        
        for size, item in zip(sizes, pipe):
            image = item['main']['image']
            assert image.shape[0] == round(size[1] * factor)
            assert image.shape[1] == round(size[0] * factor)
            assert image.dtype == np.uint8

