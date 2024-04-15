import argparse
import time
import json
import os

from pprint import pprint

from picamkit.utils import stringify_dict
import picamkit.config as config


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='output some trace', action='store_true')
    parser.add_argument('config', help='the configuration file to load', type=str)
    parser.add_argument('overrides', help='key=value configuration overrides', nargs='*', type=str)
    args = parser.parse_args()

    # config defaults
    timestamp = str(int(time.time())) 
    config_vars = {
        'timestamp': timestamp,
        'output_dir': os.path.join('local', timestamp)
    }

    # update config any overrides provided on the command line
    for override in args.overrides:
        key, value = override.split('=', 1)
        config_vars[key] = value
    
    # load the config file
    print("Loading config", flush=True)
    cfg = config.load(args.config, **config_vars)
    if args.debug:
        print("Expanded config:")
        print(json.dumps(stringify_dict(config), sort_keys=False, indent=2))
    
    # save the config file into the output dir
    os.makedirs(config_vars['output_dir'], exist_ok=True)
    config.save(cfg, config_vars['output_dir'], 'config')
        
    # build the configured system
    print("Building config", flush=True)
    built = config.build(cfg)
    if args.debug:
        print("Built config:")
        print(json.dumps(stringify_dict(built), sort_keys=False, indent=2))

    # run the pipeline
    print("Running")
    pipe = built['pipeline']
    for item in pipe:
        pass

