import time
from enum import StrEnum

from libcamera import controls
from picamera2 import Picamera2


MeteringModeEnum = StrEnum('MeteringModeEnum', ['CENTRE_WEIGHTED', 'SPOT', 'MATRIX'])
ExposureModeEnum = StrEnum('ExposureModeEnum', ['NORMAL', 'SHORT', 'LONG'])
ConstraintModeEnum = StrEnum('ConstraintModeEnum', ['NORMAL', 'HIGHLIGHT', 'SHADOWS'])

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
    metering_mode: str = MeteringModeEnum.CENTRE_WEIGHTED, 
    exposure_mode: str = ExposureModeEnum.NORMAL,
    constraint_mode: str = ConstraintModeEnum.NORMAL,
    analogue_gain: int = 0, 
    exposure_time: int = 0, 
    wait: bool = False
) -> bool:

    print("Setting exposure", flush=True)
    
    # set the camera exposure and wait for it to settle
    if auto or analogue_gain==0 or exposure_time==0:
        camera.set_controls({
            'AeEnable': True,
            'AeMeteringMode': _metering_modes[metering_mode],
            'AeExposureMode': _exposure_modes[exposure_mode],
            'AeConstraintMode': _constraint_modes[constraint_mode]
        })
        if wait:
            while True:
                mdata = camera.capture_metadata()
                if mdata['AeLocked'] == True:
                    break
    
    else:
        camera.set_controls({
            'AeEnable': False,
            'AnalogueGain': analogue_gain,
            'ExposureTime': exposure_time
        })
        if wait:
            time.sleep(0.5)
    
    return True

