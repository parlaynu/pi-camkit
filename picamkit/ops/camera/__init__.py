"""Capture images from the camera.

Define the arrays to capture from with the 'arrays' parameter. Valid values
are 'main' and 'raw'.

When 'immediate' is True, the capture takes the first available image from 
the camera. When False, it only takes an image that started it's exposure 
after the time this was called.

When 'blocking' is True, call the camera capture with 'wait' as True; when
False, call with 'wait' set to False to overlap the capture with the rest
of the processing.
"""
from typing import Generator
from picamera2 import Picamera2


def capture(
    pipe: Generator[dict, None, None], 
    camera: Picamera2, 
    *, 
    arrays: list = ['main'],
    immediate: bool = True,
    blocking: bool = True
) -> Generator[dict, None, None]:

    from .capture_blocking import capture_blocking
    from .capture_nonblocking import capture_nonblocking

    if blocking:
        return capture_blocking(pipe, camera, arrays=arrays, immediate=immediate)
    else:
        return capture_nonblocking(pipe, camera, arrays=arrays)


