import time
from enum import StrEnum

from libcamera import controls
from picamera2 import Picamera2


AwbModeEnum = StrEnum('AwbMode', ['AUTO', 'TUNGSTEN', 'FLUORESCENT', 'INDOOR', 'DAYLIGHT', 'CLOUDY'])

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
            'AwbMode': _awb_modes[mode]
        })
    else:
        if red_gain == 0 or blue_gain == 0:
            mdata = camera.capture_metadata()
            red_cur, blue_cur = mdata['ColourGains']
            
            red_gain = red_cur if red_gain == 0 else red_gain
            blue_gain = blue_cur if blue_gain == 0 else blue_gain
        
        camera.set_controls({
            'AwbEnable': False,
            'ColourGains': (red_gain, blue_gain)
        })
        
    if wait:
        time.sleep(0.5)

    return True

