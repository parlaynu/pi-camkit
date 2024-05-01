import os
os.environ['LIBCAMERA_LOG_LEVELS'] = "*:ERROR"

from picamera2 import Picamera2, Preview
from libcamera import Transform, ColorSpace, controls


def Camera(
    camera_id: int, 
    mode: int, 
    *, 
    main_format: str = 'RGB888', # NOTE: the OpenCV format
    vflip: bool = False, 
    hflip: bool = False, 
    preview: bool = False, 
    min_frameduration: int = 0, 
    initial_controls: dict = {}
) -> Picamera2:

    # create the camera object
    cam = Picamera2(camera_id)

    # the sensor format information
    sensor_mode = cam.sensor_modes[mode]
    sensor_format = sensor_mode['unpacked']
    sensor_size = sensor_mode['size']
    sensor_bit_depth = sensor_mode['bit_depth']

    # keep track of the configured mode on the object
    cam.configured_mode = sensor_mode

    # the base camera configuration
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

    # if preview is requested, configure the lores stream for display
    if preview:
        preview_size = (min(1920, sensor_size[0]), min(1080, sensor_size[1]))
        kwargs['lores'] = {
            'size': preview_size
        }
        kwargs['display'] = 'lores'

    # configure transforms
    if vflip or hflip:
        kwargs['transform'] = Transform(vflip=vflip, hflip=hflip)

    # set noise recudtion control
    kwargs['controls'] = {
        'NoiseReductionMode': controls.draft.NoiseReductionModeEnum.HighQuality
    }
    
    # create the full configuration
    config = cam.create_still_configuration(**kwargs)
    cam.align_configuration(config)
    
    # apply the configuration
    cam.configure(config)

    # start the camera
    if preview:
        cam.start_preview(Preview.DRM, width=preview_size[0], height=preview_sizep[1])
    cam.start()
    
    # apply any additional controls to the camera
    ctrls = initial_controls.copy()
    if min_frameduration > 0:
        minfd, maxfd, _ = cam.camera_controls['FrameDurationLimits']
        minfd = int(max(minfd, min_frameduration))
        ctrls.update({
            'FrameDurationLimits': (minfd, maxfd)
        })
    cam.set_controls(ctrls)
    
    return cam

