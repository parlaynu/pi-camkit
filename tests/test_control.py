import pytest
import time
import picamkit.ops.control as control


def test_control_simple():
    fps = 10
    max_frames = 25
    
    pipe = control.simple(fps=fps, max_frames=max_frames)
    
    start = time.monotonic()
    for idx, item in enumerate(pipe):
        pass
    duration = time.monotonic() - start
    
    assert max_frames == idx+1
    assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)


def test_control_flirc_exit():
    fps = 10
    max_frames = 25

    pipe = control.flirc_exit(fps=fps, max_frames=max_frames)
    
    start = time.monotonic()
    for idx, item in enumerate(pipe):
        pass
    duration = time.monotonic() - start
    
    assert max_frames == idx+1
    assert duration == pytest.approx(max_frames/fps, abs=1.0/fps)

