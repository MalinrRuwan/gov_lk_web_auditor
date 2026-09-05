import time


class RateLimiter:
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.next_request: dict[str, float] = {}

    def wait(self, host: str):
        delay = self.next_request.get(host, 0.0) - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        self.next_request[host] = time.monotonic() + self.interval
