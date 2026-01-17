import sys
import os
import zstandard as zstd

def decompress_zstd_file(input_path):
    if not input_path.endswith('.zstd'):
        print("Error: File must have a .zstd extension.")
        return

    output_path = input_path[:-5]  # Remove '.zstd'

    try:
        with open(input_path, 'rb') as compressed_file:
            dctx = zstd.ZstdDecompressor()
            with open(output_path, 'wb') as output_file:
                dctx.copy_stream(compressed_file, output_file)
        print(f"Decompressed to: {output_path}")
    except Exception as e:
        print(f"Failed to decompress {input_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decompress_zstd.py <filename.zstd>")
    else:
        decompress_zstd_file(sys.argv[1])