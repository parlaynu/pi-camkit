import time

from libcamera import controls
from picamera2 import Picamera2


# from enum import StrEnum
# AfModeEnum = StrEnum('AfModeEnum', ['MANUAL', 'AUTO', 'CONTINUOUS'])
# AfSpeedEnum = StrEnum('AfSpeedEnum', ['NORMAL', 'FAST'])

# building Enums this way for compatibility with python versions before 3.11 and StrEnum
class AfModeEnum:
    def __init__(self, value):
        self.value = value
        assert value in { AfModeEnum.MANUAL, AfModeEnum.AUTO, AfModeEnum.CONTINUOUS }
    
    def __str__(self):
        return self.value
    
    MANUAL = "manual"
    AUTO = "auto"
    CONTINUOUS = "continuous"

class AfSpeedEnum:
    def __init__(self, value):
        self.value = value
        assert value in { AfSpeedEnum.NORMAL, AfSpeedEnum.FAST }
    
    def __str__(self):
        return self.value
    
    NORMAL = "normal"
    FAST = "fast"



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
    wait: bool = False
) -> bool:

    print("Setting focus", flush=True)
    
    if str(mode) == AfModeEnum.AUTO or str(mode) == AfModeEnum.CONTINUOUS:
        ctrls = {
            'AfMode': _af_modes[str(mode)],
            'AfSpeed': _af_speeds[str(speed)],
        }
        if mode == 'auto':
            ctrls['AfTrigger'] = controls.AfTriggerEnum.Start
        
        camera.set_controls(ctrls)
    
    else:
        camera.set_controls({
            'AfMode': _af_modes[str(mode)],
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

