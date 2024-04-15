import time
from libcamera import controls


awb_modes = {
    'auto': controls.AwbModeEnum.Auto,
    'tungsten': controls.AwbModeEnum.Tungsten,
    'fluorescent': controls.AwbModeEnum.Fluorescent,
    'indoor': controls.AwbModeEnum.Indoor,
    'daylight': controls.AwbModeEnum.Daylight,
    'cloudy': controls.AwbModeEnum.Cloudy
}


def set_whitebalance(camera, *, auto=True, mode='auto', red_gain=0, blue_gain=0, wait=False):
    
    print("Setting white balance", flush=True)
    
    if auto:
        camera.set_controls({
            'AwbEnable': True,
            'AwbMode': awb_modes[mode.lower()]
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

