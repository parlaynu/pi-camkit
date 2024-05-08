# RaspberryPi Camera Capture Toolkit

This repository contains a toolkit for building custom camera capture tools for the RaspberryPi using a 
configuration file to compose capture and processing pipelines. I built it because I got tired of
writing very similar capture tools for slightly different situations.

It uses Python's 'importlib' to build the objects as defined in a configuration file. It means a lot
of boilerplate code can be written just once, such as:

* parsing command line and processing flags
* saving expanded configuration file to the output location
* saving camera configurations to the output location

## Configuration

The configuration file is where the capture and processing application is defined. There are a number of 
examples in the [configs](configs) directory. For detailed examples of how the configurations are converted
to code, two configurations are explained in detail in these documents:

* [simple capture](docs/simple-capture.md)
* [simple capture dual](docs/simple-capture-dual.md)

After reading these you should have enough knowledge to read and understand all the example configurations
and to write your own.

## Quickstart

Once you have your RaspberryPi built and the camera(s) attached (see the RaspberryPi documentation), you
first install all the necessary dependencies:

    $ sudo ./requirements.sh

Once that is done, you can run the two convenience scripts from the top level directory, for example:

    $ ./ck-run configs/simple-capture.yaml

This runs a simple capture of 10 images.

To install the library and console scripts, you can use `pip`:

    $ pip install --break-system-packages --user . 

Once this is done, the scripts `ck-run` and `ck-caminfo` should be in your executable path and the
`picamkit` library in your python library path.

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

There are four special configuration keys that the system knows about - `__target__`, `__enum__`, `__instance__` and any top level
key that begins with `pipeline`.

The `__target__` key is used to define an object to instantiate, or more generally, a function to call. This could
be a constructor for a class, or simply a function that returns the correct type. The class or function needs
to be accessible to the python interpreter in your runtime environment - it's up to you to make sure this is
setup correctly.

The `__enum__` key is similar to `__target__` but instead of creating the object with a callable, it has the
logic to create an enum.

The `__instance__` key is used to reference previously instantiated `__target__`'s. The objects are instantiated in the
order in which they appear in the configuration file. For example, in the [simple-capture.yaml](configs/simple-capture.yaml),
the camera is created first and is stored as an instance with the key 'camera'. This object is then passed
as a parameter to several other objects later in the configuration.

Any top level item that starts with `pipeline` is special in how it is built. Each function/constructor in the list needs to 
return a generator and this generator is passed in to the next function as a parameter called `pipe`.

The item with the key that is just `pipeline` is the pipeline that `ck-run` runs. It does this just by iterating over
the generator until it ends.

