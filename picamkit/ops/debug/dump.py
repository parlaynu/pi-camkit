from typing import Iterable, Generator
import time
import numpy as np


def dump(
    pipe: Iterable[dict],
    *,
    key='all',
    interval=10,
    drop=False
) -> Generator[dict, None, None]:
    """Dump the item dict contents to stdout.
    
    If 'key' is all, dump the full dict, else just the sub dict.
    
    Only dump the dict every 'interval' loops.
    """
    
    print("Building picamkit.ops.debug.dump")

    def gen():
        start = time.monotonic()
        for idx, items in enumerate(pipe):
            if drop:
                time.sleep(interval)

            yield items
            
            duration = time.monotonic() - start
            if duration < interval:
                continue
            
            print(f"Item {idx:03d}")
            
            item = items[0] if isinstance(items, list) else items
            _dump_dict(item if key == 'all' else item[key])

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
