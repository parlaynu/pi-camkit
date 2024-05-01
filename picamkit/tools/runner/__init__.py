import argparse
import time
import json
import os

from pprint import pprint

from picamkit.utils import stringify_dict
import picamkit.config as config


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='the root of the output directory', type=str, default='local')
    parser.add_argument('config', help='the configuration file to load', type=str)
    parser.add_argument('overrides', help='key=value configuration overrides', nargs='*', type=str)
    args = parser.parse_args()

    # config defaults
    timestamp = str(int(time.time())) 
    config_vars = {
        'timestamp': timestamp,
        'output_dir': os.path.join(args.output, timestamp)
    }

    # update config any overrides provided on the command line
    for override in args.overrides:
        key, value = override.split('=', 1)
        config_vars[key] = value
    
    # load the config file
    print("Loading config", flush=True)
    cfg = config.load(args.config, config_vars)
    
    # save the config file into the output dir
    os.makedirs(config_vars['output_dir'], exist_ok=True)
    config.save(cfg, config_vars['output_dir'], 'config')
        
    # build the configured system
    print("Building config", flush=True)
    built = config.build(cfg)

    # run the pipeline
    print("Running")
    pipe = built['pipeline']
    for item in pipe:
        pass

