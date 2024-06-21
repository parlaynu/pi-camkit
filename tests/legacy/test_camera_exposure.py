import pytest
import time
import picamkit.camera as ckcam


def test_default():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)


def test_wait():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_spot():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, metering_mode=ckcam.MeteringModeEnum.SPOT, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_matrix():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, metering_mode=ckcam.MeteringModeEnum.MATRIX, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_short():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, exposure_mode=ckcam.ExposureModeEnum.SHORT, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_long():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, exposure_mode=ckcam.ExposureModeEnum.LONG, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_highlight():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, constraint_mode=ckcam.ConstraintModeEnum.HIGHLIGHT, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_shadow():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, constraint_mode=ckcam.ConstraintModeEnum.SHADOWS, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True

def test_manual():
    analogue_gain = 1.0
    exposure_time = 1000
    
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam, metering_mode=ckcam.MeteringModeEnum.MANUAL, analogue_gain=analogue_gain, exposure_time=exposure_time, wait=True)
        mdata = picam.capture_metadata()
        assert mdata['AeLocked'] == True
        assert mdata['AnalogueGain'] == pytest.approx(analogue_gain, rel=0.15)
        assert mdata['ExposureTime'] == pytest.approx(exposure_time, rel=0.05)

