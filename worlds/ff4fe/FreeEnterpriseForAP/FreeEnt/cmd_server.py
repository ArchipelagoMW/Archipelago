
from .cli_command import CLICommand
from .server import Server

class ServerCommand(CLICommand):
    def add_parser_arguments(self, parser):
        parser.add_argument('--local', action='store_true')
        parser.add_argument('--password', default=None)
        parser.add_argument('--beta', action='store_true')
        parser.add_argument('--port', type=int, default=8080)

    def execute(self, args):
        server = Server()
        server.config.rom = args.rom
        server.config.local = args.local
        server.config.password = args.password
        server.config.beta = args.beta
        server.config.port = args.port

        server.run()

