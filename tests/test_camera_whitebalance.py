import pytest
import time
import picamkit.camera as ckcam


def test_default():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_whitebalance(picam)


def test_wait():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_whitebalance(picam, wait=True)


def test_presets():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_whitebalance(picam, mode=ckcam.AwbModeEnum.TUNGSTEN, wait=True)
        md = picam.capture_metadata()
        t_rgain, t_bgain = md['ColourGains']

        ckcam.set_whitebalance(picam, mode=ckcam.AwbModeEnum.FLUORESCENT, wait=True)
        md = picam.capture_metadata()
        f_rgain, f_bgain = md['ColourGains']
        
        assert t_rgain != f_rgain
        assert t_bgain != f_bgain

        ckcam.set_whitebalance(picam, mode=ckcam.AwbModeEnum.INDOOR, wait=True)
        md = picam.capture_metadata()
        i_rgain, i_bgain = md['ColourGains']
        
        assert f_rgain != i_rgain
        assert f_bgain != i_bgain

        ckcam.set_whitebalance(picam, mode=ckcam.AwbModeEnum.DAYLIGHT, wait=True)
        md = picam.capture_metadata()
        d_rgain, d_bgain = md['ColourGains']
        
        assert i_rgain != d_rgain
        assert i_bgain != d_bgain
        
        ckcam.set_whitebalance(picam, mode=ckcam.AwbModeEnum.CLOUDY, wait=True)
        md = picam.capture_metadata()
        c_rgain, c_bgain = md['ColourGains']
        
        assert d_rgain != c_rgain
        assert d_bgain != c_bgain


def test_manual():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        
        red_gain = 1.221
        blue_gain = 0.879
        
        ckcam.set_whitebalance(picam, mode=ckcam.AwbModeEnum.MANUAL, red_gain=red_gain, blue_gain=blue_gain, wait=True)
        
        md = picam.capture_metadata()
        assert md['ColourGains'][0] == pytest.approx(red_gain, rel=0.01)
        assert md['ColourGains'][1] == pytest.approx(blue_gain, rel=0.01)

