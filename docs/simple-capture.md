# Simple Configuration


## Camera Definition


| Configuration | Equivalent Code |

<table>
  <tr>
    <th>Configuration</th>
    <th>Python Code</th>
  </tr>
  <tr>
    <td>
      camera:
        __target__: picamkit.camera.Camera
        camera_id: {{ camera_id | default(0) }}
        mode: {{ camera_mode | default(1) }}
        vflip: false
        hflip: false
        preview: false
    </td>
    <td>
      camera = picamkit.camera.Camera)
        camera_id=0,
        mode=1,
        vflip=False,
        hflip=False,
        preview=False
      )
    </td>
  </tr>
</table>


<!-- # configure the camera
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


# the pipeline of generators
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
