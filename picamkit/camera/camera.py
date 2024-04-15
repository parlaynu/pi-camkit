import os
os.environ['LIBCAMERA_LOG_LEVELS'] = "*:ERROR"

import sys
import time
import types

# so we can import the wider package on non-raspberrypi machines
try:
    from picamera2 import Picamera2, Preview
    from libcamera import Transform, ColorSpace, controls
except:
    pass


def Camera(camera_id, mode, *, main_format='RGB888', vflip=False, hflip=False, preview=False, min_frameduration=0, initial_controls={}):

    cam = Picamera2(camera_id)
    
    cam.configured_mode = sensor_mode = cam.sensor_modes[mode]
    sensor_format = sensor_mode['unpacked']
    sensor_size = sensor_mode['size']
    sensor_bit_depth = sensor_mode['bit_depth']

    kwargs = {
        'buffer_count': 3,
        'colour_space': ColorSpace.Sycc(),
        'main': {
            'size': sensor_size,
            'format': main_format
        },
        'raw': {
            'size': sensor_size,
            'format': str(sensor_format)
        },
        'queue': False
    }

    # some older versions of the library don't support 'sensor'. if it's in
    #   the default configuration, it's ok to include it
    if hasattr(cam.still_configuration, 'sensor'):
        kwargs['sensor'] = {
            'output_size': sensor_size,
            'bit_depth': sensor_bit_depth
        }

    if preview:
        preview_size = (min(1920, sensor_size[0]), min(1080, sensor_size[1]))
        kwargs['lores'] = {
            'size': preview_size
        }
        kwargs['display'] = 'lores'

    if vflip or hflip:
        kwargs['transform'] = Transform(vflip=vflip, hflip=hflip)

    # default controls
    kwargs['controls'] = {
        'NoiseReductionMode': controls.draft.NoiseReductionModeEnum.HighQuality
    }
    
    # override/merge provided initial controls
    config = cam.create_still_configuration(**kwargs)
    cam.align_configuration(config)
    cam.configure(config)

    # start the camera
    if preview:
        cam.start_preview(Preview.DRM, width=preview_size[0], height=preview_sizep[1])
    cam.start()
    
    # set controls after the camera is started
    ctrls = initial_controls.copy()
    if min_frameduration > 0:
        minfd, maxfd, _ = cam.camera_controls['FrameDurationLimits']
        minfd = int(max(minfd, min_frameduration))
        ctrls.update({
            'FrameDurationLimits': (minfd, maxfd)
        })
    cam.set_controls(ctrls)
    
    return cam

