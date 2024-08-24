import argparse

class CLICommand:
    def add_parser_arguments(self, parser):
        raise Exception("add_parser_arguments() not implemented")

    def execute(self, args):
        raise Exception("execute() not implemented")

    def run_as_main(self):
        parser = argparse.ArgumentParser()
        self.add_parser_arguments(parser)
        args = parser.parse_args()
        self.execute(args)
