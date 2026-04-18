from flask import Flask


class CLI:
    def __init__(self, app: Flask) -> None:
        from .stats import stats_cli

        app.cli.add_command(stats_cli)
