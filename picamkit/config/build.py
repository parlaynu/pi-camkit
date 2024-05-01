import copy
import importlib


def build(config: dict) -> dict:
    config = copy.deepcopy(config)
    instances = {}
    if isinstance(config, (list, tuple)):
        return _build_list(config, instances)
    else:
        return _build_dict("root", config, instances)


def _build_dict(key: str, config: dict, instances: dict):
    # build nested objects first
    for k, v in config.items():
        if k.startswith('pipeline'):
            subkey = k if key == "root" else None
            config[k] = _build_pipeline(subkey, v, instances)
        elif isinstance(v, (list, tuple)):
            config[k] = _build_list(v, instances)
        elif isinstance(v, dict):
            subkey = k if key == "root" else None
            config[k] = _build_dict(subkey, v, instances)
    
    # if the __instance__ key exists, get the value from the instances
    #   dictionary
    if iname := config.get('__instance__', None):
        instance = instances[iname]
        if isinstance(instance, list):
            return instance.pop()
        else:
            return instance
    
    # if the __target__ key exists, instantiate the object...
    if enum := config.get('__enum__', None):
        return _build_enum(enum, config)

    # if the __target__ key exists, instantiate the object...
    if target := config.get('__target__', None):
        target = _build_target(target, config)
        if key:
            instances[key] = target
        return target

    # nothing else to do... return the config
    return config

    
def _build_list(config: list, instances: dict):
    for idx, v in enumerate(config):
        if isinstance(v, (list, tuple)):
            config[idx] = _build_list(v, instances)
        elif isinstance(v, dict):
            config[idx] = _build_dict(None, v, instances)
            
    return config


def _build_enum(target: str, config: dict):
    del config['__enum__']

    tgt_class_path = target.split('.')
    tgt_enum_value = tgt_class_path[-1]
    tgt_class_name = tgt_class_path[-2]
    tgt_module_path = '.'.join(tgt_class_path[0:-2])
    
    tgt_module = importlib.import_module(tgt_module_path)
    tgt_class = getattr(tgt_module, tgt_class_name)
    
    return tgt_class(value=tgt_enum_value.lower())


def _build_target(target: str, config: dict):
    del config['__target__']
    
    tgt_class_path = target.split('.')
    tgt_class_name = tgt_class_path[-1]
    tgt_module_path = '.'.join(tgt_class_path[0:-1])
    
    tgt_module = importlib.import_module(tgt_module_path)
    tgt_class = getattr(tgt_module, tgt_class_name)

    return tgt_class(**config)


def _build_pipeline(key: str, config: dict, instances: dict):
    pipe = None
    for idx, v in enumerate(config):
        if pipe is not None and v.get('pipe', None) is None:
            v['pipe'] = pipe
        config[idx] = pipe = _build_dict(None, v, instances)
    
    if key:
        instances[key] = pipe

    return pipe

