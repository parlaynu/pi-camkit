import os
import time
import cv2

# Mimic the opration of the Pi camera but read images from a directory

def fs_reader(idir, *, sort=False, recursive=False, extensions={'.png', '.jpg', '.jpeg'}):

    # make sure the extensions are in the correct format
    exts = list(extensions)
    extensions = set()
    for ext in exts:
        if not ext.startswith('.'):
            ext = '.'+ext
        extensions.add(ext)

    # the logging
    print(f"Building picamkit.ops.sources.fs_reader")
    print(f"- idir: {idir}")
    print(f"- sort: {sort}")
    print(f"- recursive: {recursive}")
    print(f"- extensions: {extensions}")


    def gen():
        
        for idx, item in enumerate(_fs_reader(idir, sort=sort, recursive=recursive, extensions=extensions)):
            item['idx'] = idx
            yield item

    return gen()


def _fs_reader(idir, *, sort, recursive, extensions={'.png', '.jpg', '.jpeg'}):
    
    idir = os.path.expanduser(idir)
    images = os.scandir(idir)
    if sort:
        images = list(images)
        images.sort(key=lambda x: x.name)
    
    for entry in images:
        if entry.is_dir() and recursive:
            yield from _fs_reader(entry.path, sort=sort, recursive=recursive, extensions=extensions)
            continue
        
        if not entry.is_file():
            continue
        
        _, ext = os.path.splitext(entry.name)
        if not ext in extensions:
            continue
    
        img = cv2.imread(entry.path, cv2.IMREAD_COLOR)
    
        item = {
            'stamp': time.monotonic_ns(),
            'metadata': {
                'name': entry.path,
            },
            'main': {
                'format': 'RGB888',
                'image': img
            }
        }
        yield item
    