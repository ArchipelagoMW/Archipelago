if __name__ == "__main__":
    import path_change
    path_change.change_home()
    import load_worlds
    load_worlds.run_load_worlds_benchmark()
    import locations
    locations.run_locations_benchmark()
