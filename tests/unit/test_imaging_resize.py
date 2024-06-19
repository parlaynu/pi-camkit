import numpy as np
import picamkit.ops.imaging as imaging

import pytest


@pytest.fixture(params=[(1024, 768, 3), (1920, 1080, 3)])
def Images(request):
    shape = (request.param[1], request.param[0], request.param[2])
    items = []
    for i in range(4):
        items.append(
            {
                'id': i,
                'main': {
                    'image': np.random.randint(0, 255, shape, np.uint8),
                    'orig_size': request.param
                }
            }
        )
    return items


@pytest.mark.parametrize('width,height', [(640,480), (720,640)])
def test_ImagesAreResized(Images, width, height):
    pipe = imaging.resize(Images, width=width, height=height)
    for item in pipe:
        img = item['main']['image']
        
        assert img.shape == (height, width, 3)
        assert img.dtype == np.uint8


@pytest.mark.parametrize('width,height', [(640,480), (720,640)])
def test_ImagesAreResizedWithAspectPreserved(Images, width, height):
    pipe = imaging.resize(Images, width=width, height=height, preserve_aspect=True, pad=False)
    for item in pipe:
        img = item['main']['image']
        size = item['main']['orig_size']
        orig_aspect = round(size[0]/size[1], 5)
        img_aspect = round(img.shape[1]/img.shape[0], 5)
        
        assert img_aspect == orig_aspect
        assert img.dtype == np.uint8


@pytest.mark.parametrize('factor', [(0.25), (0.33333333), (0.5), (0.666666667), (1.0)])
def test_ImagesAreScaled(Images, factor):
    pipe = imaging.scale(Images, factor=factor)
    for item in pipe:
        img = item['main']['image']
        size = item['main']['orig_size']
        shape = (round(size[1]*factor), round(size[0]*factor), size[2])
        
        assert img.shape == shape
        assert img.dtype == np.uint8


