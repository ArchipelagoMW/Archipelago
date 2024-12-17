import argparse
import sys
import dotenv

from .cmd_make import MakeCommand
from .rescript import RescriptCommand

dotenv.load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('rom')

subparsers = parser.add_subparsers()

subcommands = {
    'make'       : MakeCommand,
    'rescript'   : RescriptCommand,
}

for command_name in subcommands:
    subparser = subparsers.add_parser(command_name)
    command = subcommands[command_name]()
    command.add_parser_arguments(subparser)
    subparser.set_defaults(func=command.execute)

args = parser.parse_args()

try:
    getattr(args, 'func')
except AttributeError:
    parser.print_help()
    sys.exit(0)

args.func(args)
