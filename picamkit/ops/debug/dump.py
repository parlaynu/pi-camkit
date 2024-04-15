import numpy as np


def dump(pipe):
    print("Building picamkit.ops.debug.dump")

    def gen():
        for idx, item in enumerate(pipe):
            print(f"Item {idx:03d}")
        
            if isinstance(item, dict):
                _dump_dict(item)
            else:
                for i in item:
                    print("  -------")
                    _dump_dict(i)

            yield item

    return gen()


def _dump_dict(item, indent="  "):
    for k in sorted(item.keys()):
        v = item[k]
        
        if isinstance(v, (str, int, float)):
            print(f"{indent}{k}: {v}") 
        elif isinstance(v, dict):
            print(f"{indent}{k}:")
            _dump_dict(v, indent+"  ")
        elif isinstance(v, (list, tuple)):
            print(f"{indent}{k}:")
            _dump_list(v, indent+"  ")
        elif isinstance(v, np.ndarray):
            print(f"{indent}{k}: {v.shape} {v.dtype}")
        else:
            print(f"{indent}{k}: {type(v)}")


def _dump_list(item, indent="  "):
    for v in item:
        if isinstance(v, (str, int, float)):
            print(f"{indent}- {v}") 
        elif isinstance(v, np.ndarray):
            print(f"{indent}- {v.shape} {v.dtype}")
        else:
            print(f"{indent}- {type(v)}")
