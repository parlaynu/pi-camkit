import time
from enum import IntEnum

from libcamera import controls
from picamera2 import Picamera2


AfModeEnum = IntEnum('AfModeEnum', ['MANUAL', 'AUTO', 'CONTINUOUS'])
AfSpeedEnum = IntEnum('AfSpeedEnum', ['NORMAL', 'FAST'])

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
    speed: AfSpeedEnum = AfSpeedEnum.NORMAL,
    lens_position: float = 1.0,
    not_available_ok: bool = False,
    wait: bool = False
) -> bool:

    # check to make sure the camera supports autofocus
    if not_available_ok:
        mdata = camera.capture_metadata()
        if 'AfMode' not in mdata:
            return True

    # now try and focus
    print("Setting focus", flush=True)
    
    # build the controls
    if mode == AfModeEnum.AUTO or mode == AfModeEnum.CONTINUOUS:
        ctrls = {
            'AfMode': _af_modes[mode],
            'AfSpeed': _af_speeds[speed],
        }
        if mode == AfModeEnum.AUTO:
            ctrls['AfTrigger'] = controls.AfTriggerEnum.Start
        
    else:
        ctrls = {
            'AfMode': _af_modes[mode],
            'LensPosition': lens_position
        }

    # set the controls
    camera.set_controls(ctrls)
    
    # wait for focus
    if wait:
        if mode == AfModeEnum.MANUAL:
            time.sleep(0.5)
        else:
            for i in range(10):
                mdata = camera.capture_metadata()
                if mdata['AfState'] == 2:
                    print(f"- Lens Position: {mdata['LensPosition']}")
                    print(f"- Focus FoM: {mdata['FocusFoM']}")
                    break
                time.sleep(0.1)


    return True

