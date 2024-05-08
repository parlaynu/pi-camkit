import io
import zmq
import cv2

import numpy as np
from PIL import Image

from .common import MessageTags


def viewer(pub_url):

    context = zmq.Context()
    sub_sock = context.socket(zmq.SUB)
    sub_sock.set_hwm(2)
    sub_sock.connect(pub_url)
    sub_sock.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        mask = sub_sock.poll(100)
        if mask != 0:
            tag, idx, data = sub_sock.recv_multipart()
            if tag == MessageTags.JPEGIMG:
                jpeg = io.BytesIO(data)
                image = np.array(Image.open(jpeg))
                cv2.imshow('window', image)

        key = cv2.pollKey()
        if key == ord('q') or key == ord('x'):
            break
