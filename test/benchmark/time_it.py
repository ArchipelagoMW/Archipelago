import time


class TimeIt:
    def __init__(self, name: str, time_logger=None):
        self.name = name
        self.logger = time_logger
        self.timer = None
        self.end_timer = None

    def __enter__(self):
        self.timer = time.perf_counter()
        return self

    @property
    def dif(self):
        return self.end_timer - self.timer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.end_timer:
            self.end_timer = time.perf_counter()
        if self.logger:
            self.logger.info(f"{self.dif:.4f} seconds in {self.name}.")
