def print_palette(path):
    from ...graphics.palette_file import PaletteFile
    palette = PaletteFile(path)

    print(str(palette))

    palette.write_ppm("out.pal")

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help = "Path to pal file to print")

    args = parser.parse_args()
    print_palette(args.path)
