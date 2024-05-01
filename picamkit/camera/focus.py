import time
from enum import StrEnum

from libcamera import controls
from picamera2 import Picamera2


AfModeEnum = StrEnum('AfModeEnum', ['MANUAL', 'AUTO', 'CONTINUOUS'])
AfSpeedEnum = StrEnum('AfSpeedEnum', ['NORMAL', 'FAST'])

_af_modes = {
    AfModeEnum.MANUAL: controls.AfModeEnum.Manual,
    AfModeEnum.AUTO: controls.AfModeEnum.Auto,
    AfModeEnum.CONTINUOUS: controls.AfModeEnum.Continuous
}

_af_speeds = {
    AfSpeedEnum.NORMAL: controls.AfSpeedEnum.Normal,
    AfSpeedEnum.FAST: controls.AfSpeedEnum.Fast
}


def set_focus(
    camera: Picamera2, 
    *,
    mode: AfModeEnum = AfModeEnum.AUTO,
    speed: str = AfSpeedEnum.NORMAL,
    lens_position: float = 1.0,
    wait: bool = False
) -> bool:

    print("Setting focus", flush=True)
    
    mode = mode.lower()
    if mode == 'auto' or mode == 'continuous':
        ctrls = {
            'AfMode': _af_modes[mode],
            'AfSpeed': _af_speeds[speed],
        }
        if mode == 'auto':
            ctrls['AfTrigger'] = controls.AfTriggerEnum.Start
        
        camera.set_controls(ctrls)
    
    else:
        camera.set_controls({
            'AfMode': _af_modes[mode],
            'LensPosition': lens_position
        })
    
    if wait:
        time.sleep(1.0)
        if mode == 'auto':
            while True:
                mdata = camera.capture_metadata()
                if mdata['AfState'] == 2:
                    print(f"- Focus FoM: {mdata['FocusFoM']}")
                    break

    return True

