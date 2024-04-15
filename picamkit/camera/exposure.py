import time
from libcamera import controls


metering_modes = {
    'centre_weighted': controls.AeMeteringModeEnum.CentreWeighted,
    'spot': controls.AeMeteringModeEnum.Spot,
    'matrix': controls.AeMeteringModeEnum.Matrix
}

exposure_modes = {
    'normal': controls.AeExposureModeEnum.Normal,
    'short': controls.AeExposureModeEnum.Short,
    'long': controls.AeExposureModeEnum.Long
}

constraint_modes = {
    'normal': controls.AeConstraintModeEnum.Normal,
    'highlight': controls.AeConstraintModeEnum.Highlight,
    'shadows': controls.AeConstraintModeEnum.Shadows
}


def set_exposure(
    camera, *, 
    auto=True, 
    metering_mode='centre_weighted', 
    exposure_mode='normal', 
    constraint_mode='normal',
    analogue_gain=0, 
    exposure_time=0, 
    wait=False
):
    print("Setting exposure", flush=True)
    
    # set the camera exposure and wait for it to settle
    if auto or analogue_gain==0 or exposure_time==0:
        camera.set_controls({
            'AeEnable': True,
            'AeMeteringMode': metering_modes[metering_mode.lower()],
            'AeExposureMode': exposure_modes[exposure_mode.lower()],
            'AeConstraintMode': constraint_modes[constraint_mode.lower()]
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

