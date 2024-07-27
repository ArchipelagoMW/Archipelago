if __name__ == '__main__':
    import ModuleUpdate
    ModuleUpdate.update()

    import Utils
    Utils.init_logging("KH1Client", exception_logger="Client")

    from worlds.kh1.Client import launch
    launch()
