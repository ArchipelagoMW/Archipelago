import struct
import zipfile
import io
import f4c
import re
import os

import pyaes

def _extract_script(romfile):
    infile = io.BytesIO(romfile)
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

    parts = [
        script[:start_index + len(start_delimiter)],
        substitution,
        script[end_index:]
        ]
    return '\n'.join(parts)

def rescript(vanilla_rom_data, source_rom_data, zSpriteScript=None, harpSongScript=None):
    script = _extract_script(source_rom_data)

    if zSpriteScript:
        script = _swap_block(script, 'ZEROMUS SPRITE', zSpriteScript)
    if harpSongScript:
        script = _swap_block(script, 'HARP', harpSongScript)

    # preserve bytespatches by reading the script and looking for annotations
    bytes_patches = []
    for m in re.finditer(r'// RAWPATCH:(?P<addr>[0-9A-F]+),(?P<length>[0-9A-F]+)', script):
        addr = int(m['addr'], 16)
        length = int(m['length'], 16)
        bytes_patches.append(f4c.BytesPatch(source_rom_data[addr:addr+length], unheadered_address=addr))

    # recreate the embedded report
    embedded_script_utf8 = script.encode('utf-8')
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

    vanilla_rom_stream = io.BytesIO(vanilla_rom_data)
    rescript_rom_stream = io.BytesIO()
    compile_report = f4c.compile(
        vanilla_rom_stream, 
        rescript_rom_stream,
        script,
        *bytes_patches
        )

    rescript_rom_stream.seek(0)
    return rescript_rom_stream.read()
