# Simple Capture Dual Configuration

This configuration is for use on a RaspberryPi 5 with two cameras attached. It expands on the
`simple-capture.yaml` to demonstrate splitting the pipeline into two parallel paths running in 
their own threads to capture the images and joins the pipeline again to save the captured
images.

It assumes an RGB camera is `camera_id` 0, and an NOIR camera is `camera_id` 1.

## Camera Definitions

This expands on the simple-capture example to configure two cameras which can be referenced
later in the configuration as instances with names `camera_rgb` and `camera_noir`.

<table>
  <tr>
    <th>Configuration</th>
    <th>Equivalent Python Code</th>
  </tr>
  <tr>
    <td><pre>
camera_rgb:
  __target__: picamkit.camera.Camera
  camera_id: 0
  mode: {{ camera_mode | default(1) }}
  vflip: false
  hflip: false
  preview: false
    </pre></td>
    <td><pre>
camera_rgb = picamkit.camera.Camera(
  camera_id=0,
  mode=1,
  vflip=False,
  hflip=False,
  preview=False
)
    </pre></td>
  </tr>
  <tr>
    <td><pre>
camera_noir:
  __target__: picamkit.camera.Camera
  camera_id: 1
  mode: {{ camera_mode | default(1) }}
  vflip: false
  hflip: false
  preview: false
    </pre></td>
    <td><pre>
camera_noir = picamkit.camera.Camera(
  camera_id=1,
  mode=1,
  vflip=False,
  hflip=False,
  preview=False
)
    </pre></td>
  </tr>
</table>


## Configure the Cameras

This configures both cameras in a similar manner to simple-capture example.

<table>
  <tr>
    <th>Configuration</th>
    <th>Equivalent Python Code</th>
  </tr>
  <tr>
    <td><pre>
configure_rgb:
  - __target__: picamkit.camera.set_whitebalance
    camera:
      __instance__: camera_rgb
    mode:
      __enum__: picamkit.camera.AwbModeEnum.AUTO
  - __target__: picamkit.camera.set_exposure
    camera:
      __instance__: camera_rgb
    metering_mode:
      __enum__: picamkit.camera.MeteringModeEnum.SPOT
    wait: true
  - __target__: picamkit.camera.set_focus
    camera:
      __instance__: camera_rgb
    mode:
      __enum__: picamkit.camera.AfModeEnum.AUTO
    not_available_ok: true
    wait: true
  - __target__: picamkit.utils.save_camera_configs
    camera:
      __instance__: camera_rgb
    outdir: {{ output_dir }}
    </pre></td>
    <td><pre>
configure_rgb = [
  picamkit.camera.set_whitebalance(
    camera=camera_rgb,
    mode=picamkit.camera.AwbModeEnum.AUTO
  ),
  picamkit.camera.set_exposure(
    camera=camera_rgb,
    metering_mode=picamkit.camera.MeteringModeEnum.SPOT,
    wait=True
  ),
  picamkit.camera.set_focus(
    camera=camera_rgb,
    mode=picamkit.camera.AfModeEnum.AUTO,
    not_available_ok=True,
    wait=True
  ),
  picamkit.utils.save_camera_configs(
    camera=camera_rgb,
    outdir='local/1715125743'
  )
]
    </pre></td>
  </tr>
  <tr>
    <td><pre>
configure_noir:
  - __target__: picamkit.camera.set_whitebalance
    camera:
      __instance__: camera_noir
    mode:
      __enum__: picamkit.camera.AwbModeEnum.AUTO
  - __target__: picamkit.camera.set_exposure
    camera:
      __instance__: camera_noir
    metering_mode:
      __enum__: picamkit.camera.MeteringModeEnum.SPOT
    wait: true
  - __target__: picamkit.camera.set_focus
    camera:
      __instance__: camera_noir
    mode:
      __enum__: picamkit.camera.AfModeEnum.AUTO
    not_available_ok: true
    wait: true
  - __target__: picamkit.utils.save_camera_configs
    camera:
      __instance__: camera_noir
    outdir: {{ output_dir }}
    </pre></td>
    <td><pre>
configure_noir = [
  picamkit.camera.set_whitebalance(
    camera=camera_noir,
    mode=picamkit.camera.AwbModeEnum.AUTO
  ),
  picamkit.camera.set_exposure(
    camera=camera_noir,
    metering_mode=picamkit.camera.MeteringModeEnum.SPOT,
    wait=True
  ),
  picamkit.camera.set_focus(
    camera=camera_noir,
    mode=picamkit.camera.AfModeEnum.AUTO,
    not_available_ok=True,
    wait=True
  ),
  picamkit.utils.save_camera_configs(
    camera=camera_noir,
    outdir='local/1715125743'
  )
]
    </pre></td>
  </tr>
</table>


## Capture Pipeline

This pipeline section is substantially more complicated than the simple-capture example
as it needs to be split into several smaller pipelines and then linked together using the
`__instance__` keyword.

<table>
  <tr>
    <th>Configuration</th>
    <th>Equivalent Python Code</th>
  </tr>
  <tr>
    <td><pre>
pipeline_control:
  - __target__: picamkit.ops.control.simple
    max_frames: {{ max_frames | default(10) }}
  - __target__: picamkit.ops.utils.tee
    count: 2
    threaded: true
    </pre></td>
    <td><pre>
pipeline_control = picamkit.ops.control.simple(
  max_frames=10
)
pipeline_control = picamkit.ops.utils.tee(
  pipe=pipeline_control, 
  count=2,
  threaded=True
)
    </pre></td>
  </tr>
  <tr>
    <td><pre>
pipeline_rgb:
  - __instance__: pipeline_control
  - __target__: picamkit.ops.camera.capture
    camera:
      __instance__: camera_rgb
    arrays:
      - main
      - raw
  - __target__: picamkit.ops.utils.worker
    </pre></td>
    <td><pre>
pipeline_rgb = pipeline_control.pop()
pipeline_rgb = picamkit.ops.camera.capture(
  pipe=pipeline_rgb,
  camera=camera_rgb,
  arrays=['main', 'raw']
)
pipeline_rgb = picamkit.ops.utils.worker(
  pipe=pipeline_rgb
)
    </pre></td>
  </tr>
  <tr>
    <td><pre>
pipeline_noir:
  - __instance__: pipeline_control
  - __target__: picamkit.ops.camera.capture
    camera:
      __instance__: camera_noir
    arrays:
      - main
      - raw
  - __target__: picamkit.ops.utils.worker
    </pre></td>
    <td><pre>
pipeline_noir = pipeline_control.pop()
pipeline_noir = picamkit.ops.camera.capture(
  pipe=pipeline_noir,
  camera=camera_noir,
  arrays=['main', 'raw']
)
pipeline_noir = picamkit.ops.utils.worker(
  pipe=pipeline_noir
)
    </pre></td>
  </tr>
  <tr>
    <td><pre>
pipeline:
  - __target__: picamkit.ops.utils.zip
    pipe1:
      __instance__: pipeline_rgb
    name1: rgb
    pipe2:
      __instance__: pipeline_noir
    name2: noir
  - __target__: picamkit.ops.sink.save_item
    outdir: {{ output_dir }}
  - __target__: picamkit.ops.sink.save_rgb
    outdir: {{ output_dir }}
  - __target__: picamkit.ops.sink.save_raw
    outdir: {{ output_dir }}

    </pre></td>
    <td><pre>
pipeline = picamkit.ops.utils.zip(
  pipe1=pipeline_rgb,
  name1='rgb',
  pipe2=pipeline_noir,
  name2='noir'
)
pipeline = picamkit.ops.sink.save_item(
  pipe=pipeline,
  outdir='local/1715130814'
)
pipeline = picamkit.ops.sink.save_rgb(
  pipe=pipeline,
  outdir='local/1715130814'  
)
pipeline = picamkit.ops.sink.save_raw(
  pipe=pipeline,
  outdir='local/1715130814'  
)
    </pre></td>
  </tr>
</table>

## Running the Pipeline

Once the pipeline is built, `ck-run` runs the pipeline with code as simple as this:

    for item in pipeline:
      pass

The output from running this configuration looks like this:

    $ ./ck-run configs/simple-capture-dual.yaml 
    Loading config
    Building config
    Setting white balance
    Setting exposure
    Setting white balance
    Setting exposure
    Building picamkit.ops.control.simple
    - max_frames: 10
    Building picamkit.ops.utils.tee
    - count: 2
    Building picamkit.ops.camera.capture
    - arrays: ['main', 'raw']
    - immediate: True
    Building picamkit.ops.utils.worker
    - qlen: 1
    Building picamkit.ops.camera.capture
    - arrays: ['main', 'raw']
    - immediate: True
    Building picamkit.ops.utils.worker
    - qlen: 1
    Building picamkit.ops.utils.zip
    - name1: rgb
    - name2: noir
    - grouped: False
    Building picamkit.ops.sink.save_item
    - outdir: local/1715130814
    - prefix: img
    - mdata_key: metadata
    Building picamkit.ops.sink.save_rgb
    - outdir: local/1715130814
    - file_format: png
    - image_key: main.image
    - format_key: main.format
    - prefix: img
    Building picamkit.ops.sink.save_raw
    - outdir: local/1715130814
    - image_key: raw.image
    - format_key: raw.format
    - prefix: img
    Running
    Saving local/1715130814/img-0000-rgb.json
    Saving local/1715130814/img-0000-rgb.png
    Saving local/1715130814/img-0000-rgb-raw.png
    Saving local/1715130814/img-0000-noir.json
    Saving local/1715130814/img-0000-noir.png
    Saving local/1715130814/img-0000-noir-raw.png
    Saving local/1715130814/img-0001-rgb.json
    Saving local/1715130814/img-0001-rgb.png
    Saving local/1715130814/img-0001-rgb-raw.png
    Saving local/1715130814/img-0001-noir.json
    Saving local/1715130814/img-0001-noir.png
    Saving local/1715130814/img-0001-noir-raw.png
    Saving local/1715130814/img-0002-rgb.json
    Saving local/1715130814/img-0002-rgb.png
    Saving local/1715130814/img-0002-rgb-raw.png
    Saving local/1715130814/img-0002-noir.json
    Saving local/1715130814/img-0002-noir.png
    Saving local/1715130814/img-0002-noir-raw.png
    Saving local/1715130814/img-0003-rgb.json
    Saving local/1715130814/img-0003-rgb.png
    Saving local/1715130814/img-0003-rgb-raw.png
    Saving local/1715130814/img-0003-noir.json
    Saving local/1715130814/img-0003-noir.png
    Saving local/1715130814/img-0003-noir-raw.png
    Saving local/1715130814/img-0004-rgb.json
    Saving local/1715130814/img-0004-rgb.png
    Saving local/1715130814/img-0004-rgb-raw.png
    Saving local/1715130814/img-0004-noir.json
    Saving local/1715130814/img-0004-noir.png
    Saving local/1715130814/img-0004-noir-raw.png
    Saving local/1715130814/img-0005-rgb.json
    Saving local/1715130814/img-0005-rgb.png
    Saving local/1715130814/img-0005-rgb-raw.png
    Saving local/1715130814/img-0005-noir.json
    Saving local/1715130814/img-0005-noir.png
    Saving local/1715130814/img-0005-noir-raw.png
    Saving local/1715130814/img-0006-rgb.json
    Saving local/1715130814/img-0006-rgb.png
    Saving local/1715130814/img-0006-rgb-raw.png
    Saving local/1715130814/img-0006-noir.json
    Saving local/1715130814/img-0006-noir.png
    Saving local/1715130814/img-0006-noir-raw.png
    Saving local/1715130814/img-0007-rgb.json
    Saving local/1715130814/img-0007-rgb.png
    Saving local/1715130814/img-0007-rgb-raw.png
    Saving local/1715130814/img-0007-noir.json
    Saving local/1715130814/img-0007-noir.png
    Saving local/1715130814/img-0007-noir-raw.png
    Saving local/1715130814/img-0008-rgb.json
    Saving local/1715130814/img-0008-rgb.png
    Saving local/1715130814/img-0008-rgb-raw.png
    Saving local/1715130814/img-0008-noir.json
    Saving local/1715130814/img-0008-noir.png
    Saving local/1715130814/img-0008-noir-raw.png
    Saving local/1715130814/img-0009-rgb.json
    Saving local/1715130814/img-0009-rgb.png
    Saving local/1715130814/img-0009-rgb-raw.png
    Saving local/1715130814/img-0009-noir.json
    Saving local/1715130814/img-0009-noir.png
    Saving local/1715130814/img-0009-noir-raw.png

