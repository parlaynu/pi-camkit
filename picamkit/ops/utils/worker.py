import sys
import threading
import queue


def worker(pipe, *, qlen=1):
    print("Building picamkit.ops.utils.worker")
    print(f"- qlen: {qlen}")

    q = queue.Queue(maxsize=qlen)
    worker = Worker(pipe, q)
    worker.start()
    
    def gen():
        while True:
            item = q.get()
            if isinstance(item, Exception):
                raise item
            if item is None:
                break
            yield item
    
        worker.join()
    
    return gen()


class Worker(threading.Thread):
    def __init__(self, pipe, q):
        super().__init__(daemon=True)
        self.pipe = pipe
        self.queue = q
    
    def run(self):
        try:
            for item in self.pipe:
                self.queue.put(item)
            self.queue.put(None)
        except Exception as e:
            self.queue.put(e)