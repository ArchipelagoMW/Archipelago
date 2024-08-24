import multiprocessing

class Config:
    def __init__(self, args):
        self.args = args
        self.db_url = "mongodb://127.0.0.1:27017"
        self.db_name = ('ff4fe-beta' if args.beta else 'ff4fe')

def run_generator(config, task_queue, start_event):
    import generator
    start_event.set()
    generator.run(config, task_queue)

if __name__ == '__main__':
    import argparse
    import pymongo
    import website

    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true')
    parser.add_argument('--password')
    parser.add_argument('--beta', action='store_true')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    config = Config(args)

    start_event = multiprocessing.Event()
    task_queue = multiprocessing.Queue()

    generator_process = multiprocessing.Process(
        target = run_generator,
        args = (config, task_queue, start_event)
        )
    generator_process.start()
    start_event.wait()

    try:
        website.run(config, task_queue)
    except KeyboardInterrupt as e:
        pass

    generator_process.kill()
