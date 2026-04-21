import click
from flask.cli import AppGroup
from pony.orm import raw_sql

from Utils import format_SI_prefix

stats_cli = AppGroup("stats")


@stats_cli.command("show")
def show() -> None:
    from pony.orm import db_session, select

    from WebHostLib.models import GameDataPackage

    total_games_package_count: int = 0
    total_games_package_size: int
    top_10_package_sizes: list[tuple[int, str]] = []

    with db_session:
        data_length = raw_sql("LENGTH(data)")
        data_length_desc = raw_sql("LENGTH(data) DESC")
        data_length_sum = raw_sql("SUM(LENGTH(data))")
        total_games_package_count = GameDataPackage.select().count()
        total_games_package_size = select(data_length_sum for _ in GameDataPackage).first()  # type: ignore
        top_10_package_sizes = list(
            select((data_length, dp.checksum) for dp in GameDataPackage)  # type: ignore
            .order_by(lambda _, _2: data_length_desc)
            .limit(10)
        )

    click.echo(f"Total number of games packages: {total_games_package_count}")
    click.echo(f"Total size of games packages:   {format_SI_prefix(total_games_package_size, power=1024)}B")
    click.echo(f"Top {len(top_10_package_sizes)} biggest games packages:")
    for size, checksum in top_10_package_sizes:
        click.echo(f"    {checksum}: {size:>8d}")
