#!/usr/bin/env bash

# core packages
apt install -y python3-pip python3-numpy python3-opencv python3-jinja2 python3-ruamel.yaml

# for flirc controller
apt install -y python3-evdev

# for aws s3 as image source
apt install -y python3-boto3 awscli

# for the network operators
apt install -y python3-zmq python3-pil

# for testing
apt install -y python3-pytest
