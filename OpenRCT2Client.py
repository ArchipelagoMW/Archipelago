from worlds.openrct2.Client import main
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("OpenRCT2Client", exception_logger="Client")
    main()
