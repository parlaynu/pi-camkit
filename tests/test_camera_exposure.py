import pytest
import time
import picamkit.camera as cam


def test_default():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam)


def test_wait():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_spot():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, wait=True, metering_mode=cam.MeteringModeEnum.SPOT)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_matrix():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, wait=True, metering_mode=cam.MeteringModeEnum.MATRIX)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_short():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, wait=True, exposure_mode=cam.ExposureModeEnum.SHORT)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_long():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, wait=True, exposure_mode=cam.ExposureModeEnum.LONG)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_highlight():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, wait=True, constraint_mode=cam.ConstraintModeEnum.HIGHLIGHT)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_shadow():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, wait=True, constraint_mode=cam.ConstraintModeEnum.SHADOWS)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

