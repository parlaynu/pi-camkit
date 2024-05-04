import time

from libcamera import controls
from picamera2 import Picamera2


# from enum import StrEnum
# MeteringModeEnum = StrEnum('MeteringModeEnum', ['CENTRE_WEIGHTED', 'SPOT', 'MATRIX'])
# ExposureModeEnum = StrEnum('ExposureModeEnum', ['NORMAL', 'SHORT', 'LONG'])
# ConstraintModeEnum = StrEnum('ConstraintModeEnum', ['NORMAL', 'HIGHLIGHT', 'SHADOWS'])

# building Enums this way for compatibility with python versions before 3.11 and StrEnum
class MeteringModeEnum:
    def __init__(self, value):
        self.value = value
        assert value in { MeteringModeEnum.CENTRE_WEIGHTED, MeteringModeEnum.SPOT, MeteringModeEnum.MATRIX }
    
    def __str__(self):
        return self.value
    
    CENTRE_WEIGHTED = "centre_weighted"
    SPOT = "spot"
    MATRIX = "matrix"

class ExposureModeEnum:
    def __init__(self, value):
        self.value = value
        assert value in { ExposureModeEnum.NORMAL, ExposureModeEnum.SHORT, ExposureModeEnum.LONG }
    
    def __str__(self):
        return self.value
    
    NORMAL = "normal"
    SHORT = "short"
    LONG = "long"

class ConstraintModeEnum:
    def __init__(self, value):
        self.value = value
        assert value in { ConstraintModeEnum.NORMAL, ConstraintModeEnum.HIGHLIGHT, ConstraintModeEnum.SHADOWS }
    
    def __str__(self):
        return self.value
    
    NORMAL = "normal"
    HIGHLIGHT = "highlight"
    SHADOWS = "shadows"


_metering_modes = {
    MeteringModeEnum.CENTRE_WEIGHTED: controls.AeMeteringModeEnum.CentreWeighted,
    MeteringModeEnum.SPOT: controls.AeMeteringModeEnum.Spot,
    MeteringModeEnum.MATRIX: controls.AeMeteringModeEnum.Matrix
}

_exposure_modes = {
    ExposureModeEnum.NORMAL: controls.AeExposureModeEnum.Normal,
    ExposureModeEnum.SHORT: controls.AeExposureModeEnum.Short,
    ExposureModeEnum.LONG: controls.AeExposureModeEnum.Long
}

_constraint_modes = {
    ConstraintModeEnum.NORMAL: controls.AeConstraintModeEnum.Normal,
    ConstraintModeEnum.HIGHLIGHT: controls.AeConstraintModeEnum.Highlight,
    ConstraintModeEnum.SHADOWS: controls.AeConstraintModeEnum.Shadows
}
    

def set_exposure(
    camera: Picamera2, 
    *, 
    auto: bool = True, 
    metering_mode: MeteringModeEnum = MeteringModeEnum.CENTRE_WEIGHTED, 
    exposure_mode: ExposureModeEnum = ExposureModeEnum.NORMAL,
    constraint_mode: ConstraintModeEnum = ConstraintModeEnum.NORMAL,
    analogue_gain: int = 0, 
    exposure_time: int = 0, 
    wait: bool = False
) -> bool:

    print("Setting exposure", flush=True)
    
    # set the camera exposure and wait for it to settle
    if auto:
        camera.set_controls({
            'AeEnable': True,
            'AeMeteringMode': _metering_modes[str(metering_mode)],
            'AeExposureMode': _exposure_modes[str(exposure_mode)],
            'AeConstraintMode': _constraint_modes[str(constraint_mode)]
        })
        if wait:
            while True:
                mdata = camera.capture_metadata()
                if mdata['AeLocked'] == True:
                    break
    
    else:
        mdata = camera.capture_metadata()
        if analogue_gain == 0:
            analogue_gain = mdata['AnalogueGain']
        if exposure_time == 0:
            exposure_time = mdata['ExposureTime']

        camera.set_controls({
            'AeEnable': False,
            'AnalogueGain': analogue_gain,
            'ExposureTime': exposure_time
        })
        if wait:
            time.sleep(0.5)
    
    return True

