# Simple Configuration


## Camera Definition

This block creates the camera with the specified parameters. It shows the use of the `__target__` tag
to specify a python class to instantiate. 

The configuration is jinja2, which is expanded to yaml and then imported into the application as 
a dict. The jinja2 defaults can be overridded by passing a `key=value` argument to`ck-run`. For example:

    ck-run configs/simple-capture.yaml camera_mode=0

The variable `camera` can be referenced later in the configuration file with the `__instance__` tag.

<table>
  <tr>
    <th>Configuration</th>
    <th>Python Code</th>
  </tr>
  <tr>
    <td><pre>
camera:
  __target__: picamkit.camera.Camera
  camera_id: {{ camera_id | default(0) }}
  mode: {{ camera_mode | default(1) }}
  vflip: false
  hflip: false
  preview: false
    </pre></td>
    <td><pre>
camera = picamkit.camera.Camera(
  camera_id=0,
  mode=1,
  vflip=False,
  hflip=False,
  preview=False
)
    </pre></td>
  </tr>
</table>


## Configure the Camera

This block simply calls several functions that perform specific configurations on the
camera itself. 

It finishes by saving all the camera configuration settings to files in the output directory 
so you have a record of all the settings the images were captured with. The variable
`output_dir` is automatically set by the `ck-run` application, defaulting to `local/<timestamp>`. 
The top level location can be overridden with a a commandline flag to `ck-run` and as with other 
variables, it can also be overridden on the command line with a `output_dir=value`.

<table>
  <tr>
    <th>Configuration</th>
    <th>Python Code</th>
  </tr>
  <tr>
    <td><pre>
configure_cam:
  - __target__: picamkit.camera.set_whitebalance
    camera:
      __instance__: camera
    mode:
      __enum__: picamkit.camera.AwbModeEnum.AUTO
  - __target__: picamkit.camera.set_exposure
    camera:
      __instance__: camera
    metering_mode:
      __enum__: picamkit.camera.MeteringModeEnum.SPOT
    wait: true
  - __target__: picamkit.camera.set_focus
    camera:
      __instance__: camera
    mode:
      __enum__: picamkit.camera.AfModeEnum.AUTO
    not_available_ok: true
    wait: true
  - __target__: picamkit.utils.save_camera_configs
    camera:
      __instance__: camera
    outdir: {{ output_dir }}
    </pre></td>
    <td><pre>
configure_cam = [
  picamkit.camera.set_whitebalance(
    camera=camera,
    mode=picamkit.camera.AwbModeEnum.AUTO
  ),
  picamkit.camera.set_exposure(
    camera=camera,
    metering_mode=picamkit.camera.MeteringModeEnum.SPOT,
    wait=True
  ),
  picamkit.camera.set_focus(
    camera=camera,
    mode=picamkit.camera.AfModeEnum.AUTO,
    not_available_ok=True,
    wait=True
  ),
  picamkit.utils.save_camera_configs(
    camera=camera,
    outdir='local/1715125743'
  )
]
    </pre></td>
  </tr>
</table>


<!-- # the pipeline of generators
pipeline:
  - __target__: picamkit.ops.control.simple
    max_frames: {{ max_frames | default(10) }}
  - __target__: picamkit.ops.camera.capture
    camera:
      __instance__: camera
    arrays:
      - main
    immediate: true
  - __target__: picamkit.ops.imaging.resize
    width: 1280
    height: 720
    preserve_aspect: true
  - __target__: picamkit.ops.sink.save_item
    outdir: {{ output_dir }}
  - __target__: picamkit.ops.sink.save_rgb
    outdir: {{ output_dir }} -->
