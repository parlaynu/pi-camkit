import io
import zmq
import cv2

import numpy as np
from PIL import Image


def viewer(publish_url):

    context = zmq.Context()
    sub_sock = context.socket(zmq.SUB)
    sub_sock.set_hwm(2)

    def gen():
        
        sub_sock.connect(publish_url)
        sub_sock.setsockopt(zmq.SUBSCRIBE, b'')
        
        while True:
            mask = sub_sock.poll(100)
            if mask != 0:
                idx, data = sub_sock.recv_multipart()
                jpeg = io.BytesIO(data)
                image = np.array(Image.open(jpeg))
                cv2.imshow('window', image)
                
                item = {
                    'idx': idx,
                    'main': {
                        'image': image
                    }
                }
                yield item

            key = cv2.pollKey()
            if key == ord('q') or key == ord('x'):
                break

    return gen()
