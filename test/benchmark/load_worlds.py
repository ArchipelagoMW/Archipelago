def run_load_worlds_benchmark():
    """List worlds and their load time.
    Note that any first-time imports will be attributed to that world, as it is cached afterwards.
    Likely best used with isolated worlds to measure their time alone."""
    import logging

    from Utils import init_logging

    # get some general imports cached, to prevent it from being attributed to one world.
    import orjson
    orjson.loads("{}")  # orjson runs initialization on first use

    import BaseClasses, Launcher, Fill

    from worlds import world_sources, ensure_all_worlds_loaded

    init_logging("Benchmark Runner")
    logger = logging.getLogger("Benchmark")

    ensure_all_worlds_loaded()

    for module in world_sources:
        logger.info(f"{module} took {module.time_taken:.4f} seconds.")


if __name__ == "__main__":
    from path_change import change_home
    change_home()
    run_load_worlds_benchmark()
