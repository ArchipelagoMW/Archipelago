def main():
    from . import args
    from metadata.flag_metadata_writer import FlagMetadataWriter
    FlagMetadataWriter(args).write()

if __name__ == '__main__':
    main()
