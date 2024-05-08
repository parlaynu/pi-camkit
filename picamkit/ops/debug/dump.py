from typing import Generator
import numpy as np


def dump(
    pipe: Generator[dict, None, None],
    *,
    key='all',
    interval=1,
) -> Generator[dict, None, None]:
    """Dump the item dict contents to stdout.
    
    If 'key' is all, dump the full dict, else just the sub dict.
    
    Only dump the dict every 'interval' loops.
    """
    
    print("Building picamkit.ops.debug.dump")

    def gen():
        for idx, items in enumerate(pipe):
            if idx % interval != 0:
                yield items
                continue
            
            print(f"Item {idx:03d}")
            
            if not isinstance(items, list):
                items = [items]
            
            for iidx, item in enumerate(items):
                if iidx > 0:
                    print("  -------")
                
                _dump_dict(item if key == 'all' else item[key])

            yield items

    return gen()


def _dump_dict(item: dict, indent: str = "  ") -> None:
    for k in sorted(item.keys()):
        if k.endswith('StatsOutput'):
            continue
        
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


def _dump_list(item: list, indent: str = "  ") -> None:
    for v in item:
        if isinstance(v, (str, int, float)):
            print(f"{indent}- {v}") 
        elif isinstance(v, np.ndarray):
            print(f"{indent}- {v.shape} {v.dtype}")
        else:
            print(f"{indent}- {type(v)}")
