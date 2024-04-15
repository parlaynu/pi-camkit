import time
from libcamera import controls


af_modes = {
    'manual': controls.AfModeEnum.Manual,
    'auto': controls.AfModeEnum.Auto,
    'continuous': controls.AfModeEnum.Continuous
}

af_speeds = {
    'normal': controls.AfSpeedEnum.Normal,
    'fast': controls.AfSpeedEnum.Fast
}


def set_focus(
    camera, *,
    mode='auto',
    speed='normal',
    lens_position=1.0,
    wait=False
):
    print("Setting focus", flush=True)
    
    mode = mode.lower()
    if mode == 'auto' or mode == 'continuous':
        ctrls = {
            'AfMode': af_modes[mode],
            'AfSpeed': af_speeds[speed.lower()],
        }
        if mode == 'auto':
            ctrls['AfTrigger'] = controls.AfTriggerEnum.Start
        
        camera.set_controls(ctrls)
    
    else:
        camera.set_controls({
            'AfMode': af_modes[mode],
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

