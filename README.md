# RaspberryPi Camera Capture Toolkit

This repository contains a toolkit for building custom camera capture tools for the RaspberryPi using a 
configuration file to compose capture and processing pipelines. I built it because I got tired of
writing very similar capture tools for slightly different situations.

It uses Python's 'importlib' to create generators as defined in a configuration and chain
them together in pipelines.

Now, while it does work and works well, it's not entirely robust. It is possible to define configurations
that can't be built and the diagnostics can be a bit cryptic. Hopefully this will all improve as I
use it more.

## Quickstart

Once you have your RaspberryPi built and the cameras attached (see the RaspberryPi documentation), you
first install all the necessary dependencies:

    $ sudo ./requirements.sh

Then you need to `pip` install this project so the console scripts are created and you can access the
tools from anywhere on your system.

    $ pip install --break-system-packages --user . 

You can now run the example in the next section.

## Quick Example

There are some example configurations in the `configs` directory. Running the capture session defined in the
configuration called `simple-capture.yaml`, looks like this:

    $ ck-run configs/simple-capture.yaml 
    Loading config
    Building config
    Setting exposure
    Setting white balance
    Setting focus
    Waiting for 5 seconds
    Building picamkit.ops.control.simple
      max_frames: 10
    Building picamkit.ops.camera.capture
    - arrays: ['main', 'raw']
    - immediate: True
    Building picamkit.ops.imaging.resize
    - image_key: main.image
    - width: 1280
    - height: 720
    - preserve_aspect: True
    Building picamkit.ops.io.save_item
    - outdir: local/1713146422
    - prefix: img
    - mdata_key: metadata
    Building picamkit.ops.io.save_rgb
    - outdir: local/1713146422
    - file_format: png
    - image_key: main.image
    - format_key: main.format
    - prefix: img
    Building picamkit.ops.io.save_raw8
    - outdir: local/1713146422
    - image_key: raw.image
    - format_key: raw.format
    - prefix: img
    Running
    Saving local/1713146422/img-0000.json
    Saving local/1713146422/img-0000-rgb.png
    Saving local/1713146422/img-0000-raw8.png
    .
    .
    Saving local/1713146422/img-0009.json
    Saving local/1713146422/img-0009-rgb.png
    Saving local/1713146422/img-0009-raw8.png


## Operation Overview

The config file is key to the operation of the toolkit and the console script `ck-run` loads, parses and executes
the commands in it.

There are a few key phases:

* reading the file
* expanding the contents as a jinja2 template
* parsing the expanded contents as a yaml file
* processing the python dict and creating the processing pipeline
* running the pipeline

If you're familiar with [jinja2](https://palletsprojects.com/p/jinja/), you will recognise jinja2 
template expressions in the example config files. The template variables can either use defaults or can
be passed on the command line to `ck-run` as overrides. For example, the config file [simple-capture.yaml](configs/simple-capture.yaml)
has a template variable 'max_frames', which defaults to 10, which controls how many frames to capture. To override this and
instead capture 100 frames, you would run `ck-run` like this:

    ck-run configs/simple-capture.yaml max_frames=100

You can pass any template variable into the template expansion using this mechanism. The tool `ck-run` doesn't 
actually have any useful command line flags (other than a help flag), but relies soley on this mechanism to
customise a capture pipeline defined in a template configuration file.

There are three special configuration keys that the system knows about - `__target__`, `__instance__` and any top level
key that begins with `pipeline`.

The `__target__` key is used to define an object to instantiate, or more generally, a function to call. This could
be a constructor for a class, or simply a function that returns the correct type. The class or function needs
to be accessible to the python interpreter in your runtime environment - it's up to you to make sure this is
setup correctly.

The `__instance__` key is used to reference previously instantiated `__target__`'s. The objects are instantiated in the
order in which they appear in the configuration file. For example, in the [simple-capture.yaml](configs/simple-capture.yaml),
the camera is created first and is stored as an instance with the key 'camera'. This object is then passed
as a parameter to several other objects later in the configuration.

Any top level item that starts with `pipeline` is special in how it is built. Each function/constructor in the list needs to 
return a generator and this generator is passed in to the next function as a parameter called `pipe`.

The item with the key that is just `pipeline` is the pipeline that `ck-run` runs. It does this just by iterating over
the generator until it ends.

## Advanced Pipelines

Most of the sample configs are just single pipelines and simple to follow. The two pipelines 
[flirc-capture-dual.yaml](configs/flirc-capture-dual.yaml) and [timelapse-stills-dual.yaml](configs/timelapse-stills-dual.yaml)
show more advanced capabilities:

* splitting the pipeline into smaller sections and chaining them together
* capturing from two cameras on a RaspberryPi5
* running two branches of the pipeline in parallel in their own threads
* mergine the pipelines back together

Chaining pipeline segments together is achieved using the `__instance__` keyword as described earlier.
The other features are provided with some operators in the toolkit as shown in the table below:

| Feature                | Operator                  |
| ---------------------- | ------------------------- |
| Splitting the Pipeline | picamkit.ops.utils.tee    |
| Running in own Thread  | picamkit.ops.utils.worker |
| Merging the Pipelines  | picamkit.ops.utils.merge  |

