import multiprocessing

from . import generator
from . import website

def run_generator_worker(config, task_queue, start_event):
    start_event.set()
    generator.run(config, task_queue)


class ServerConfig:
    def __init__(self):
        self.rom = None
        self.local = False
        self.password = None
        self.beta = False
        self.port = 8080
        self.db_url = "mongodb://127.0.0.1:27017"

    @property
    def db_name(self):
        return ('ff4fe-beta' if self.beta else 'ff4fe')


class Server:
    def __init__(self):
        self._config = ServerConfig()

    @property
    def config(self):
        return self._config
    
    def run(self):
        start_event = multiprocessing.Event()
        task_queue = multiprocessing.Queue()

        generator_process = multiprocessing.Process(
            target = run_generator_worker,
            args = (self.config, task_queue, start_event)
            )
        generator_process.start()
        start_event.wait()

        try:
            website.run(self.config, task_queue)
        except KeyboardInterrupt as e:
            pass

        generator_process.kill()
