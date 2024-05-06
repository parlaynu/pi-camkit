from typing import Generator
import time
import numpy as np

from picamera2 import Picamera2


image_dtypes = {
    'RGB888': np.uint8,
    'BGR888': np.uint8,
    'SBGGR16': np.uint16,
    'SGRBG16': np.uint16,
    'SGBRG16': np.uint16,
    'SRGGB16': np.uint16,
}


def capture(
    pipe: Generator[dict, None, None], 
    camera: Picamera2, 
    *, 
    arrays: list = ['main'],
    immediate: bool = True
) -> Generator[dict, None, None]:

    
    print(f"Building picamkit.ops.camera.capture")
    print(f"- arrays: {arrays}")
    print(f"- immediate: {immediate}")
    
    def gen():
    
        for idx, item in enumerate(pipe):
            # make sure 'idx' is in item
            item['idx'] = item.get('idx', idx)
        
            # capture the image
            item['stamp'] = stamp = item.get('stamp', time.monotonic_ns())
            while True:
                images, metadata = camera.capture_arrays(arrays, wait=True)
                start = metadata['SensorTimestamp'] - 1000 * metadata['ExposureTime']
                if immediate or start >= stamp:
                    break

            # assemble the item
            item['metadata'] = metadata
            for idx, array in enumerate(arrays):
                item[array] = camera.camera_config[array].copy()

                image_format = item[array]['format']
                image_dtype = image_dtypes[image_format]
            
                item[array]['image'] = images[idx].view(image_dtype)

            yield item

    return gen()
