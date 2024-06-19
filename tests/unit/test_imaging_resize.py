import numpy as np
import picamkit.ops.imaging as imaging

import pytest


@pytest.fixture(params=[(768, 1024, 3), (1080, 1920, 3)])
def Images(request):
    items = []
    for i in range(4):
        items.append(
            {
                'id': i,
                'main': {
                    'image': np.random.randint(0, 255, request.param, np.uint8),
                    'orig_shape': request.param
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


@pytest.mark.parametrize('factor', [(0.25), (0.33333333), (0.5), (0.666666667), (1.0)])
def test_ImagesAreScaled(Images, factor):
    pipe = imaging.scale(Images, factor=factor)
    for item in pipe:
        img = item['main']['image']
        shape = item['main']['orig_shape']
        shape = (round(shape[0]*factor), round(shape[1]*factor), shape[2])
        assert img.shape == shape
        assert img.dtype == np.uint8


