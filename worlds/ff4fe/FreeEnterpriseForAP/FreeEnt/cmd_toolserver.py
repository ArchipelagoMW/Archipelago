from .cli_command import CLICommand
from .tool_server import ToolServer

class ToolServerCommand(CLICommand):
    def add_parser_arguments(self, parser):
        pass

    def execute(self, args):
        server = ToolServer(args.rom)
        server.run()
