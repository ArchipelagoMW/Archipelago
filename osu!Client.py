from worlds.osu.Client import main
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("osu!Client", exception_logger="Client")
    main()
