from multiprocessing import Queue
import twitter


class TwitterPool:
    def __init__(self):
        self.ready_queue = Queue()
        self.revive_queue = Queue()

    def get_api(self):
        if not self.ready_queue.empty():
            return self.ready_queue.get()

        if not self.revive_queue.empty():
            api = self.revive_queue.get()

    def release_api(self, api):
        pass
