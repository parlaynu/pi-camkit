import os
import json
import numpy as np


def save_item(pipe, outdir, *, prefix='img', mdata_key='metadata'):
    print("Building picamkit.ops.io.save_item")
    print(f"- outdir: {outdir}")
    print(f"- prefix: {prefix}")
    print(f"- mdata_key: {mdata_key}")
    
    os.makedirs(outdir, exist_ok=True)
    
    def gen():
        for items in pipe:
            if not isinstance(items, list):
                items = [items]
        
            for item in items:
                idx = item['idx']
        
                local_item = item.copy()
        
                # clean the metadata
                metadata = local_item[mdata_key]
                for k in list(metadata.keys()):
                    if k.endswith('StatsOutput'):
                        del metadata[k]
        
                # remove any images
                for kk, vv in local_item.items():
                    if not isinstance(vv, dict):
                        continue
            
                    local_item[kk] = vv = vv.copy()
                    for k in list(vv.keys()):
                        v = vv[k]
                        if isinstance(v, np.ndarray):
                            del vv[k]
        
                # save the item
                if name := item.get('name', None):
                    item_path = os.path.join(outdir, f"{prefix}-{idx:04d}-{name}.json")
                else:
                    item_path = os.path.join(outdir, f"{prefix}-{idx:04d}.json")

                print(f"Saving {item_path}")
    
                with open(item_path, "w") as f:
                    print(json.dumps(local_item, sort_keys=True, indent=2), file=f)
        
                yield item

    return gen()
