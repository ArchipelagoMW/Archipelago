from collections import Counter, defaultdict
from colorsys import hsv_to_rgb
from datetime import datetime, timedelta, date
from math import tau

from bokeh.colors import RGB
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.plotting import figure, ColumnDataSource
from bokeh.resources import INLINE
from flask import render_template
from pony.orm import select

from . import app, cache
from .models import Room

PLOT_WIDTH = 600


def get_db_data(known_games: set[str]) -> tuple[Counter[str], defaultdict[date, dict[str, int]]]:
    games_played: defaultdict[date, dict[str, int]] = defaultdict(Counter)
    total_games: Counter[str] = Counter()
    cutoff = date.today() - timedelta(days=30)
    room: Room
    for room in select(room for room in Room if room.creation_time >= cutoff):
        for slot in room.seed.slots:
            if slot.game in known_games:
                current_game = slot.game
            else:
                current_game = "Other"
            total_games[current_game] += 1
            games_played[room.creation_time.date()][current_game] += 1
    return total_games, games_played


def get_color_palette(colors_needed: int) -> list[RGB]:
    colors = []
    # colors_needed +1 to prevent first and last color being too close to each other
    colors_needed += 1

    for x in range(0, 361, 360 // colors_needed):
        # a bit of noise on value to add some luminosity difference
        colors.append(RGB(*(val * 255 for val in hsv_to_rgb(x / 360, 0.8, 0.8 + (x / 1800)))))

    # splice colors for maximum hue contrast.
    colors = colors[::2] + colors[1::2]

    return colors


def create_game_played_figure(all_games_data: dict[date, dict[str, int]], game: str, color: RGB) -> figure:
    occurences = []
    days = [day for day, game_data in all_games_data.items() if game_data[game]]
    for day in days:
        occurences.append(all_games_data[day][game])
    data = {
        "days": [datetime.combine(day, datetime.min.time()) for day in days],
        "played": occurences
    }

    plot = figure(
        title=f"{game} Played Per Day", x_axis_type='datetime', x_axis_label="Date",
        y_axis_label="Games Played", sizing_mode="scale_both", width=PLOT_WIDTH, height=500,
        toolbar_location=None, tools="",
        # setting legend to False seems broken in bokeh currently?
        # legend=False
    )

    hover = HoverTool(tooltips=[("Date:", "@days{%F}"), ("Played:", "@played")], formatters={"@days": "datetime"})
    plot.add_tools(hover)
    plot.vbar(x="days", top="played", legend_label=game, color=color, source=ColumnDataSource(data=data), width=1)
    return plot


@app.route('/stats')
@cache.memoize(timeout=60 * 60)  # regen once per hour should be plenty
def stats():
    from worlds import network_data_package
    known_games = set(network_data_package["games"])
    plot = figure(title="Games Played Per Day", x_axis_type='datetime', x_axis_label="Date",
                  y_axis_label="Games Played", sizing_mode="scale_both", width=PLOT_WIDTH, height=500)

    total_games, games_played = get_db_data(known_games)
    days = sorted(games_played)

    color_palette = get_color_palette(len(total_games))
    game_to_color: dict[str, RGB] = {game: color for game, color in zip(total_games, color_palette)}

    for game in sorted(total_games):
        occurences = []
        for day in days:
            occurences.append(games_played[day][game])
        plot.line([datetime.combine(day, datetime.min.time()) for day in days],
                  occurences, legend_label=game, line_width=2, color=game_to_color[game])

    total = sum(total_games.values())
    pie = figure(title=f"Games Played in the Last 30 Days (Total: {total})", toolbar_location=None,
                 tools="hover", tooltips=[("Game:", "@games"), ("Played:", "@count")],
                 sizing_mode="scale_both", width=PLOT_WIDTH, height=500, x_range=(-0.5, 1.2))
    pie.axis.visible = False
    pie.xgrid.visible = False
    pie.ygrid.visible = False

    data = {
        "games": [],
        "count": [],
        "start_angles": [],
        "end_angles": [],
    }
    current_angle = 0
    for i, (game, count) in enumerate(total_games.most_common()):
        data["games"].append(game)
        data["count"].append(count)
        data["start_angles"].append(current_angle)
        angle = count / total * tau
        current_angle += angle
        data["end_angles"].append(current_angle)

    data["colors"] = [game_to_color[game] for game in data["games"]]

    pie.wedge(x=0, y=0, radius=0.5,
              start_angle="start_angles", end_angle="end_angles", fill_color="colors",
              source=ColumnDataSource(data=data), legend_field="games")

    per_game_charts = [create_game_played_figure(games_played, game, game_to_color[game]) for game in
                       sorted(total_games, key=lambda game: total_games[game])
                       if total_games[game] > 1]

    script, charts = components((plot, pie, *per_game_charts))
    return render_template("stats.html", js_resources=INLINE.render_js(), css_resources=INLINE.render_css(),
                           chart_data=script, charts=charts)
