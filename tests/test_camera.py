import pytest
import time
import picamkit.camera as cam


def test_default():
    with cam.Camera(camera_id=0, mode=1) as picam:
        array = picam.capture_array('main')
        assert len(array.shape) == 3
        assert array.shape[-1] == 3


def test_bgr888():
    with cam.Camera(camera_id=0, mode=1, main_format='BGR888') as picam:
        array = picam.capture_array('main')
        assert len(array.shape) == 3
        assert array.shape[-1] == 3


def test_options():
    with cam.Camera(camera_id=0, mode=1, vflip=True, hflip=True) as picam:
        array = picam.capture_array('main')
        assert len(array.shape) == 3
        assert array.shape[-1] == 3

