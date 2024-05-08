from typing import Generator
import threading
import socket
import psutil
import re
import io
import json

import zmq
from PIL import Image

from .common import MessageTags


def publisher(
    pipe: Generator[dict, None, None],
    *, 
    port: int = 8090,
    image_key: str = 'main.image', 
    local_listen: bool = False
) -> None:

    kwargs = {
        'pipe': pipe,
        'port': port,
        'image_key': image_key,
        'local_listen': local_listen
    }
    worker = threading.Thread(target=_publisher, kwargs=kwargs)
    worker.start()


def _publisher(pipe, port, image_key, local_listen):

    image_keys = image_key.split('.')
    
    if local_listen:
        pub_url = f"tcp://127.0.0.1:{port}"
    else:
        pub_url = f"tcp://0.0.0.0:{port}"
    
    all_urls = _connect_urls(pub_url)
    for u in all_urls:
        print(f"Publishing at {u}")

    context = zmq.Context()
    pub_sock = context.socket(zmq.PUB)
    pub_sock.set_hwm(2)
    pub_sock.bind(pub_url)

    for item in pipe:
        idx = item['idx']
        idx = f"{idx}".encode('utf-8')

        # create a clean copy of the metadata
        metadata = item['metadata'].copy()
        for k in list(metadata.keys()):
            if k.endswith('StatsOutput'):
                del metadata[k]
        
        # send the metadata
        metajs = json.dumps(metadata, separators=(',',':'))
        pub_sock.send_multipart([MessageTags.METADATA, idx, metajs.encode('utf-8')], copy=False)

        # send the jpeg image
        image = item
        for key in image_keys:
            image = image[key]
        
        image = Image.fromarray(image)
        
        jpeg = io.BytesIO()
        image.save(jpeg, format='jpeg', quality=95)
        jpeg.seek(0, io.SEEK_SET)
                
        pub_sock.send_multipart([MessageTags.JPEGIMG, idx, jpeg.getvalue()], copy=False)


def _connect_urls(listen_url):
    """Get all the URLs that can be used to connect to the listen URL."""

    # split the url
    tcp_re = re.compile("^tcp://(?P<address>.+?):(?P<port>\d+)$")
    mo = tcp_re.match(listen_url)
    if mo is None:
        raise ValueError(f"unable to parse {listen_url}")

    address = mo['address']
    port = mo['port']

    urls = []
    if address == "0.0.0.0":
        local_addresses = _local_ips()
        for address in local_addresses['ipv4']:
            urls.append(f'tcp://{address}:{port}')

    else:
        urls.append(url)

    return urls


def _local_ips():
    """Returns all the local IP addresses on the host."""
    
    ipv4s = []
    ipv6s = []
    
    interfaces = psutil.net_if_addrs()
    for interface, if_addresses in interfaces.items():
        for if_address in if_addresses:
            if if_address.family == socket.AF_INET:
                ipv4s.append(if_address.address)
            elif if_address.family == socket.AF_INET6:
                ipv6s.append(if_address.address)
    
    addresses = {
        'ipv4': ipv4s,
        'ipv6': ipv6s
    }

    return addresses


