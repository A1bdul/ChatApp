import threading


class CloudinaryUpload(threading.Thread):
    def __init__(self, data):
        self.data = data
        threading.Thread.__init__(self)

    def start(self) -> None:
        for img in self.data:
            pass