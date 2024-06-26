# Simple Capture Configuration

This configuration defines a camera, configures the camera, and then captures some images. It's 
the minimum needed to do something useful.

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
    <th>Equivalent Python Code</th>
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

This can be overridded in either of two ways. In the first example, the ouput directory
will be `../capture/<timestamp>`:

    $ ./ck-run -o ../capture configs/simple-capture.yaml

In this example, the ouput directory will be `../capture`:

    $ ./ck-run configs/simple-capture.yaml output_dir=../capture


<table>
  <tr>
    <th>Configuration</th>
    <th>Equivalent Python Code</th>
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


## Capture Pipeline

This final section builds the capture pipeline. This is a number of generators that are linked 
to each other in the order specified in the configuration.

<table>
  <tr>
    <th>Configuration</th>
    <th>Equivalent Python Code</th>
  </tr>
  <tr>
    <td><pre>
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
    outdir: {{ output_dir }}
    </pre></td>
    <td><pre>
pipeline = picamkit.ops.control.simple(
  max_frames=10
)
pipeline = picamkit.ops.camera.capture(
  pipe=pipeline, 
  camera=camera, 
  arrays=['main], 
  immediate=True
)
pipeline = picamkit.ops.imaging.resize(
  pipe=pipeline,
  width=1280,
  height=720,
  preserve_aspect=True
)
pipeline = picamkit.ops.sink.save_item(
  pipe=pipeline,
  outdir='local/1715125743'
)
pipeline = picamkit.ops.sink.save_rgb(
  pipe=pipeline,
  outdir='local/1715125743'
)
    </pre></td>
  </tr>
</table>

## Running the Pipeline

Once the pipeline is built, `ck-run` runs the pipeline with code as simple as this:

    for item in pipeline:
      pass

The output from running this configuration looks like this:

    $ ./ck-run configs/simple-capture.yaml 
    Loading config
    Building config
    Setting white balance
    Setting exposure
    Building picamkit.ops.control.simple
    - max_frames: 10
    Building picamkit.ops.camera.capture
    - arrays: ['main']
    - immediate: True
    Building picamkit.ops.imaging.resize
    - image_key: main.image
    - width: 1280
    - height: 720
    - preserve_aspect: True
    Building picamkit.ops.sink.save_item
    - outdir: local/1715125743
    - prefix: img
    - mdata_key: metadata
    Building picamkit.ops.sink.save_rgb
    - outdir: local/1715125743
    - file_format: png
    - image_key: main.image
    - format_key: main.format
    - prefix: img
    Running
    Saving local/1715125743/img-0000.json
    Saving local/1715125743/img-0000-rgb.png
    Saving local/1715125743/img-0001.json
    Saving local/1715125743/img-0001-rgb.png
    Saving local/1715125743/img-0002.json
    Saving local/1715125743/img-0002-rgb.png
    Saving local/1715125743/img-0003.json
    Saving local/1715125743/img-0003-rgb.png
    Saving local/1715125743/img-0004.json
    Saving local/1715125743/img-0004-rgb.png
    Saving local/1715125743/img-0005.json
    Saving local/1715125743/img-0005-rgb.png
    Saving local/1715125743/img-0006.json
    Saving local/1715125743/img-0006-rgb.png
    Saving local/1715125743/img-0007.json
    Saving local/1715125743/img-0007-rgb.png
    Saving local/1715125743/img-0008.json
    Saving local/1715125743/img-0008-rgb.png
    Saving local/1715125743/img-0009.json
    Saving local/1715125743/img-0009-rgb.png


The `json` files that are saved contain all the metadata from the image capture. These are saved
by the operator `picamkit.ops.sink.save_item` included in the pipeline.
An example is like this:

    {
      "idx": 0,
      "main": {
        "format": "RGB888",
        "framesize": 8957952,
        "size": [
          2304,
          1296
        ],
        "stride": 6912
      },
      "metadata": {
        "AeLocked": true,
        "AfPauseState": 0,
        "AfState": 0,
        "AnalogueGain": 3.029585838317871,
        "ColourCorrectionMatrix": [
          1.5383427143096924,
          -0.3521742522716522,
          -0.18616284430027008,
          -0.3317224383354187,
          1.6765234470367432,
          -0.3447909653186798,
          0.0037013564724475145,
          -0.5590126514434814,
          1.5553213357925415
        ],
        "ColourGains": [
          1.7750877141952515,
          2.0837767124176025
        ],
        "ColourTemperature": 4058,
        "DigitalGain": 1.0024760961532593,
        "ExposureTime": 59989,
        "FocusFoM": 878,
        "FrameDuration": 199995,
        "LensPosition": 1.0,
        "Lux": 179.4264373779297,
        "ScalerCrop": [
          0,
          0,
          4608,
          2592
        ],
        "SensorBlackLevels": [
          4096,
          4096,
          4096,
          4096
        ],
        "SensorTemperature": 26.0,
        "SensorTimestamp": 83126207467000
      },
      "stamp": 83126151379817
    }

