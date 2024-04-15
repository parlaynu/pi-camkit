import numpy as np


def fake_capture(pipe, *, width=640, height=480):
    print("Building picamkit.ops.debug.fake_capture")
    print(f"- width: {width}")
    print(f"- height: {height}")

    def gen():
        for item in pipe:
            item['metadata'] = {
                'fake': True
            }
            item['main'] = {
                'image': np.random.randint(0, 255, size=(height, width, 3), dtype=np.uint8),
                'format': 'RGB888'
            }
            yield item

    return gen()
