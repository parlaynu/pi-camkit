import os
import time
import cv2

# Mimic the opration of the Pi camera but read images from a directory

def fs_reader(idir, *, sort=False, extensions={'.png', '.jpg', '.jpeg'}):

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
    print(f"- extensions: {extensions}")

    idir = os.path.expanduser(idir)
    images = os.scandir(idir)
    if sort:
        images = list(images)
        images.sort(key=lambda x: x.name)

    def gen():
        for idx, entry in enumerate(images):
            if not entry.is_file():
                continue
            _, ext = os.path.splitext(entry.name)
            if not ext in extensions:
                continue
        
            img = cv2.imread(entry.path, cv2.IMREAD_COLOR)
        
            item = {
                'idx': idx,
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

    return gen()

