import pytest
import time
from pprint import pprint
import picamkit.camera as ckcam
import picamkit.ops.control as control
import picamkit.ops.camera as cap


def test_mainonly():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 25
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture(pipe, picam)
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)


def test_rawonly():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 25
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture(pipe, picam, arrays=['raw'])
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)


def test_mainandraw():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 25
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture(pipe, picam, arrays=['main', 'raw'])
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start
        
        img_m = item['main']['image']
        img_r = item['raw']['image']
        
        assert img_m.shape[0] == img_r.shape[0]
        # width can be differnt
        # assert img_m.shape[1] == img_r.shape[1]

        assert max_frames == idx+1
        assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)


def test_notimmediate():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 15
        
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture(pipe, picam, arrays=['main'], immediate=False)
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        assert duration > max_frames/fps


def test_mainonly_async():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 25
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture_async(pipe, picam)
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)


def test_rawonly_async():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 25
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture_async(pipe, picam, arrays=['raw'])
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)


def test_mainandraw_async():
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 25
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture_async(pipe, picam, arrays=['main', 'raw'])
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        img_m = item['main']['image']
        img_r = item['raw']['image']
        
        assert img_m.shape[0] == img_r.shape[0]
        # width can be differnt
        # assert img_m.shape[1] == img_r.shape[1]

        assert max_frames == idx+1
        assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)

