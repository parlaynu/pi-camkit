import time

from libcamera import controls
from picamera2 import Picamera2


# from enum import StrEnum
# AwbModeEnum = StrEnum('AwbMode', ['AUTO', 'TUNGSTEN', 'FLUORESCENT', 'INDOOR', 'DAYLIGHT', 'CLOUDY'])

# building Enums this way for compatibility with python versions before 3.11 and StrEnum
class AwbModeEnum:
    def __init__(self, value):
        self.value = value
        assert value in { AwbModeEnum.AUTO, AwbModeEnum.TUNGSTEN, AwbModeEnum.FLUORESCENT, AwbModeEnum.INDOOR,  AwbModeEnum.DAYLIGHT, AwbModeEnum.CLOUDY }
    
    def __str__(self):
        return self.value
    
    AUTO = "auto"
    TUNGSTEN = "tungsten"
    FLUORESCENT = "fluorescent"
    INDOOR = "indoor"
    DAYLIGHT = "daylight"
    CLOUDY = "cloudy"

_awb_modes = {
    AwbModeEnum.AUTO: controls.AwbModeEnum.Auto,
    AwbModeEnum.TUNGSTEN: controls.AwbModeEnum.Tungsten,
    AwbModeEnum.FLUORESCENT: controls.AwbModeEnum.Fluorescent,
    AwbModeEnum.INDOOR: controls.AwbModeEnum.Indoor,
    AwbModeEnum.DAYLIGHT: controls.AwbModeEnum.Daylight,
    AwbModeEnum.CLOUDY: controls.AwbModeEnum.Cloudy
}


def set_whitebalance(
    camera: Picamera2, 
    *, 
    auto: bool = True, 
    mode: AwbModeEnum = AwbModeEnum.AUTO, 
    red_gain: float = 0, 
    blue_gain: float = 0, 
    wait: bool = False
) -> bool:

    print("Setting white balance", flush=True)
    
    if auto:
        camera.set_controls({
            'AwbEnable': True,
            'AwbMode': _awb_modes[str(mode)]
        })
    else:
        mdata = camera.capture_metadata()
        if red_gain == 0:
            red_gain = mdata['ColourGains'][0]
        if blue_gain == 0:
            blue_gain = mdata['ColourGains'][1]
        
        camera.set_controls({
            'AwbEnable': False,
            'ColourGains': (red_gain, blue_gain)
        })
        
    if wait:
        time.sleep(0.5)

    return True

