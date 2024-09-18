import os
import json
import tempfile

from .. import FreeEnt
from .cli_command import CLICommand

class MakeCommand(CLICommand):
    def add_parser_arguments(self, parser):
        parser.add_argument('-d', '--debug', action='store_true')
        parser.add_argument('-q', '--quickstart', action='store_true')
        parser.add_argument('-s', '--seed')
        parser.add_argument('-f', '--flags')
        parser.add_argument('--hideflags', action='store_true')
        parser.add_argument('-t', '--test')
        parser.add_argument('rom')
        parser.add_argument('-o', '--output')
        parser.add_argument('-a', '--ap_data')
        parser.add_argument('-m', '--metrics', action='store_true')
        parser.add_argument('-r', '--recompile', action='store_true')
        parser.add_argument('-l', '--lastseed', action='store_true')
        parser.add_argument('-b', '--beta', action='store_true')
        parser.add_argument('--spoileronly', action='store_true')

    def execute(self, args):
        generator = FreeEnt.Generator()
        options = generator.options
        options.debug = args.debug
        options.quickstart = args.quickstart
        options.ap_data = json.loads(args.ap_data)

        #if args.lastseed:
        #    if os.path.exists('.lastseed'):
        #        with open('.lastseed', 'r') as infile:
        #            options.seed = infile.read().strip()

        if args.seed:
            options.seed = args.seed

        if args.flags:
            options.flags.load(args.flags)

        options.hide_flags = args.hideflags
        options.beta = args.beta
        options.spoiler_only = args.spoileronly

        #if args.test:
        #    if os.path.isfile(args.test):
        #        with open(args.test, 'r') as infile:
        #            options.test_settings = json.load(infile)
        #    else:
        #        try:
        #            options.test_settings = json.loads(args.test)
        #        except json.decoder.JSONDecodeError as e:
        #            options.test_settings = {}
        #            for pair in args.test.split(';'):
        #                if pair.strip():
        #                    parts = pair.split(':')
        #                    key = parts[0].strip()
        #                    if len(parts) == 1:
        #                        val = True
        #                    else:
        #                        val = parts[1].strip()

        #                    options.test_settings[key] = val

        options.cache_path = os.path.join(tempfile.TemporaryDirectory().name, '.build')

        build_output = generator.generate(args.rom, force_recompile=args.recompile)
        seed = build_output.seed
        report = build_output.report
        output_filename = args.output
        if output_filename is None:
            build_label = f'v{FreeEnt.VERSION_STR}.{build_output.seed}.{build_output.binary_flags}'
            output_filename = f'FreeEnterprise.{build_label}.smc'

        if len(build_output.rom):
            with open(output_filename, 'wb') as outfile:
                outfile.write(build_output.rom)

        #with open('.lastseed', 'w') as outfile:
        #    outfile.write('{}\n'.format(seed))

        #if report is not None:
        #    with open(output_filename + '.symbols', 'w') as outfile:
        #        symbol_names = [pair[1] for pair in sorted([[report.symbols[name], name] for name in report.symbols])]
        #        for n in symbol_names:
        #            outfile.write(f'{report.symbols[n]:6X}  {n}\n')

        #with open(output_filename + '.script', 'w') as outfile:
        #    outfile.write(build_output.script)

        if (build_output.public_spoiler is not None):
            with open(output_filename + '.spoiler.public', 'w') as outfile:
                outfile.write(build_output.public_spoiler)

        #with open(output_filename + '.spoiler.private', 'w') as outfile:
        #    outfile.write(build_output.private_spoiler)

        #if args.metrics and report is not None:
        #    print(report.metrics)
        #    print(', '.join(build_output.verification))

if __name__ == '__main__':
    MakeCommand().run_as_main()
