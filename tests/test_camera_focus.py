import pytest
import time
import picamkit.camera as cam


def can_focus(picam):
    mdata = picam.capture_metadata()
    return 'AfState' in mdata


def test_default():
    with cam.Camera(camera_id=0, mode=1) as picam:
        if can_focus(picam) == False:
            return
        cam.set_focus(picam, wait=False)
        
        for i in range(10):
            mdata = picam.capture_metadata()
            if mdata['AfState'] == 2:
                break
            time.sleep(0.1)
        assert mdata['AfState'] == 2


def test_wait():
    with cam.Camera(camera_id=0, mode=1) as picam:
        if can_focus(picam) == False:
            return
        cam.set_focus(picam, wait=True)
        
        mdata = picam.capture_metadata()
        assert mdata['AfState'] == 2
        

def test_manual():
    with cam.Camera(camera_id=0, mode=1) as picam:
        if can_focus(picam) == False:
            return

        lens_position = 1.5
        cam.set_focus(picam, mode=cam.AfModeEnum.MANUAL, lens_position=lens_position)
        
        for i in range(10):
            mdata = picam.capture_metadata()
            if mdata['LensPosition'] == pytest.approx(lens_position, rel=0.05):
                break
            time.sleep(0.1)
            
        assert mdata['LensPosition'] == pytest.approx(lens_position, rel=0.05)
        

def test_continuous():
    with cam.Camera(camera_id=0, mode=1) as picam:
        if can_focus(picam) == False:
            return

        cam.set_focus(picam, mode=cam.AfModeEnum.CONTINUOUS, wait=True)
        
        mdata = picam.capture_metadata()
        assert mdata['AfState'] == 2
        

