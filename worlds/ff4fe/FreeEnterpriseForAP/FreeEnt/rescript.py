import struct
import zipfile
import io
import argparse
import subprocess
import os
import platform
import re

import pyaes

import f4c
from .cli_command import CLICommand

def extract_script(romfile):
    if type(romfile) is bytes:
        infile = io.BytesIO(romfile)
    else:
        if os.path.splitext(romfile)[1].lower() == '.zip':
            rom_zip = zipfile.ZipFile(romfile, mode='r', compression=zipfile.ZIP_DEFLATED)
            rom_data = rom_zip.read(os.path.splitext(os.path.basename(romfile))[0] + '.smc')
            infile = io.BytesIO(rom_data)
        else:
            infile = open(romfile, 'rb')

    source_rom_data = infile.read()
    infile.seek(0x1FF000 - 4)
    report_length = struct.unpack('<L', infile.read(4))[0]
    infile.seek(0x1FF000 - 4 - report_length)
    encrypted_data = infile.read(report_length)
    infile.close()

    key = os.getenv('FE_EMBEDDED_REPORT_KEY').encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)
    data = aes.decrypt(encrypted_data)

    try:
        report_zip = zipfile.ZipFile(io.BytesIO(data), mode='r', compression=zipfile.ZIP_LZMA)
    except zipfile.BadZipFile:
        raise Exception("Error loading embedded report; could not read zip data. This may occur due to an incorrect encryption key.")

    script = report_zip.read('script.f4c')
    report_zip.close()

    return script.decode('utf-8')

def _swap_block(script, block_name, substitution):
    start_delimiter = f'// [[[ {block_name} START ]]]'
    end_delimiter = f'// [[[ {block_name} END ]]]'
    try:
        start_index = script.index(start_delimiter)
        end_index = script.index(end_delimiter)
    except ValueError:
        print(f'WARNING: missing delimiters for block {block_name}, skipping swap')
        return script

    if os.path.isfile(substitution):
        with open(substitution, 'r') as infile:
            substitution = infile.read()

    parts = [
        script[:start_index + len(start_delimiter)],
        substitution,
        script[end_index:]
        ]
    return '\n'.join(parts)


class RescriptCommand(CLICommand):
    def add_parser_arguments(self, parser):
        parser.add_argument('fe_rom')
        parser.add_argument('-s', '--script')
        parser.add_argument('-x', '--extract', action='store_true')
        parser.add_argument('-o', '--output', nargs='?')
        parser.add_argument('-z', '--zeromus')
        parser.add_argument('-r', '--harp')
        parser.add_argument('-n', '--names')
        parser.add_argument('-i', '--interactive', action='store_true')

    def execute(self, args):
        only_apply_if_changed = True
        force_interactive_mode = False

        with open(args.fe_rom, 'rb') as infile:
            source_rom_data = infile.read()

        if args.script:
            print(f'Loading script from {args.script}')
            with open(args.script, 'r') as infile:
                script = infile.read()
            only_apply_if_changed = False
        else:
            print(f'Extracting script from {args.fe_rom}')
            script = extract_script(source_rom_data)
            force_interactive_mode = True

        if args.zeromus:
            print(f'Substituting Zeromus sprite with {args.zeromus}')
            script = _swap_block(script, 'ZEROMUS SPRITE', args.zeromus)
            only_apply_if_changed = False
            force_interactive_mode = False
        if args.harp:
            print(f'Substituting harp song with {args.harp}')
            script = _swap_block(script, 'HARP', args.harp)
            only_apply_if_changed = False
            force_interactive_mode = False
        if args.names:
            print(f'Substituting default names with {args.names}')
            with open(args.names, 'r') as infile:
                names = [f'{l.strip():6}' for l in infile if l.strip()]
            names_script = 'text($0fa710 bus) {' + ''.join(names) + '}'
            script = _swap_block(script, 'NAMES', names_script)
            only_apply_if_changed = False
            force_interactive_mode = False

        if args.extract:
            extract_filename = args.fe_rom + '.script.f4c'
            with open(extract_filename, 'w') as outfile:
                outfile.write(script)
        else:
            with open('.tmp.rescript.f4c', 'w') as outfile:
                outfile.write(script)

            should_apply = True
            if args.interactive or force_interactive_mode:
                old_time = os.path.getmtime('.tmp.rescript.f4c')
                if platform.system() == 'Windows':
                    editor = 'notepad.exe'
                else:
                    editor = 'vi'
                subprocess.call([editor, ".tmp.rescript.f4c"])
                new_time = os.path.getmtime('.tmp.rescript.f4c')
                if only_apply_if_changed and new_time <= old_time:
                    should_apply = False

            if should_apply:
                print('Applying new script')

                # preserve bytespatches by reading the script and looking for annotations
                bytes_patches = []
                with open('.tmp.rescript.f4c', 'r') as infile:
                    rescript = infile.read()
                    for m in re.finditer(r'// RAWPATCH:(?P<addr>[0-9A-F]+),(?P<length>[0-9A-F]+)', rescript):
                        addr = int(m['addr'], 16)
                        length = int(m['length'], 16)
                        bytes_patches.append(f4c.BytesPatch(source_rom_data[addr:addr+length], unheadered_address=addr))

                # recreate the embedded report
                embedded_script_utf8 = rescript.encode('utf-8')
                zip_info = zipfile.ZipInfo(filename='script.f4c', date_time=(2000,1,1,0,0,0))
                zip_info.compress_type = zipfile.ZIP_LZMA
                zip_buffer = io.BytesIO()
                report_zip = zipfile.ZipFile(zip_buffer, mode='w')
                report_zip.writestr(zip_info, embedded_script_utf8)
                report_zip.close()

                zip_buffer.seek(0)
                embedded_report = zip_buffer.read()

                key = os.getenv('FE_EMBEDDED_REPORT_KEY').encode('utf-8')
                aes = pyaes.AESModeOfOperationCTR(key)
                encrypted_report = aes.encrypt(embedded_report)

                report_addr = 0x1FF000 - len(encrypted_report) - 4
                bytes_patches.append(f4c.BytesPatch(
                    encrypted_report + struct.pack('<L', len(encrypted_report)), 
                    unheadered_address=report_addr
                    ))

                # apply compile
                if args.output:
                    output_filename = args.output
                else:
                    split_parts = os.path.splitext(args.fe_rom)
                    output_filename = split_parts[0] + '.rescript' + split_parts[1]

                print(f'Generating {output_filename}')
                compile_report = f4c.compile(
                    args.rom, 
                    output_filename,
                    '.tmp.rescript.f4c',
                    *bytes_patches
                    )

                print(compile_report.metrics)
            else:
                print("Rescript file not changed, aborting")
            os.unlink('.tmp.rescript.f4c')

