import pytest
import os
import time
import shutil
from pprint import pprint
from PIL import Image

import picamkit.camera as ckcam
import picamkit.ops.control as control
import picamkit.ops.camera as cap
import picamkit.ops.sink as sink


def test_save_rgb(tmp_path):
    # capture some images
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 5
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture(pipe, picam)
        pipe = sink.save_rgb(pipe, tmp_path)
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        
    # load them back with a different library
    for item in os.scandir(tmp_path):
        if not item.name.endswith('png'):
            continue
        
        print(f"Loading {item.path}")
        img = Image.open(item.path)
        img.load()

    # cleanup
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_save_raw(tmp_path):
    # capture some images
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 5
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture(pipe, picam, arrays=["main", "raw"])
        pipe = sink.save_raw(pipe, tmp_path)
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        
    # load them back with a different library
    for item in os.scandir(tmp_path):
        if not item.name.endswith('png'):
            continue
        
        print(f"Loading {item.path}")
        img = Image.open(item.path)
        img.load()

    # cleanup
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_save_raw8(tmp_path):
    # capture some images
    with ckcam.Camera(camera_id=0, mode=1) as picam:
        ckcam.set_exposure(picam)
        ckcam.set_focus(picam, not_available_ok=True, wait=True)
        
        fps = 10
        max_frames = 5
        pipe = control.simple(fps=fps, max_frames=max_frames)
        pipe = cap.capture(pipe, picam, arrays=["main", "raw"])
        pipe = sink.save_raw8(pipe, tmp_path)
        
        start = time.monotonic()
        for idx, item in enumerate(pipe):
            pass
        duration = time.monotonic() - start

        assert max_frames == idx+1
        
    # load them back with a different library
    for item in os.scandir(tmp_path):
        if not item.name.endswith('png'):
            continue
        
        print(f"Loading {item.path}")
        img = Image.open(item.path)
        img.load()

    # cleanup
    shutil.rmtree(tmp_path, ignore_errors=True)
