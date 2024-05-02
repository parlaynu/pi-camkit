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
        cam.set_exposure(picam, metering_mode=cam.MeteringModeEnum.SPOT, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_matrix():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, metering_mode=cam.MeteringModeEnum.MATRIX, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_short():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, exposure_mode=cam.ExposureModeEnum.SHORT, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_long():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, exposure_mode=cam.ExposureModeEnum.LONG, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_highlight():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, constraint_mode=cam.ConstraintModeEnum.HIGHLIGHT, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_shadow():
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, constraint_mode=cam.ConstraintModeEnum.SHADOWS, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_manual():
    analogue_gain = 1.0
    exposure_time = 1000
    
    with cam.Camera(camera_id=0, mode=1) as picam:
        cam.set_exposure(picam, auto=False, analogue_gain=analogue_gain, exposure_time=exposure_time, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True
        assert mdata['AnalogueGain'] == pytest.approx(analogue_gain, rel=0.15)
        assert mdata['ExposureTime'] == pytest.approx(exposure_time, rel=0.05)

