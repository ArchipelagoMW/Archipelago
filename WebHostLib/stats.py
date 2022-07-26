from collections import Counter, defaultdict
from colorsys import hsv_to_rgb
from datetime import datetime, timedelta, date
from math import tau
import typing

from bokeh.embed import components
from bokeh.plotting import figure, ColumnDataSource
from bokeh.resources import INLINE
from bokeh.colors import RGB
from flask import render_template
from pony.orm import select

from . import app, cache
from .models import Room


def get_db_data() -> typing.Tuple[typing.Dict[str, int], typing.Dict[datetime.date, typing.Dict[str, int]]]:
    games_played = defaultdict(Counter)
    total_games = Counter()
    cutoff = date.today()-timedelta(days=30000)
    room: Room
    for room in select(room for room in Room if room.creation_time >= cutoff):
        for slot in room.seed.slots:
            total_games[slot.game] += 1
            games_played[room.creation_time.date()][slot.game] += 1
    return total_games, games_played


def get_color_palette(colors_needed: int) -> typing.List[RGB]:
    colors = []
    # colors_needed +1 to prevent first and last color being too close to each other
    colors_needed += 1

    for x in range(0, 361, 360//colors_needed):
        # a bit of noise on value to add some luminosity difference
        colors.append(RGB(*(val*255 for val in hsv_to_rgb(x/360, 0.8, 0.8+(x/1800)))))

    # splice colors for maximum hue contrast.
    colors = colors[::2] + colors[1::2]

    return colors


@app.route('/stats')
@cache.memoize(timeout=60*60)  # regen once per hour should be plenty
def stats():
    plot = figure(title="Games Played Per Day", x_axis_type='datetime', x_axis_label="Date",
                  y_axis_label="Games Played", sizing_mode="scale_both", width=500, height=500)

    total_games, games_played = get_db_data()
    days = sorted(games_played)

    color_palette = get_color_palette(len(total_games))

    for i, game in enumerate(sorted(total_games)):
        occurences = []
        for day in days:
            occurences.append(games_played[day][game])
        plot.line([datetime.combine(day, datetime.min.time()) for day in days],
                  occurences, legend_label=game, line_width=2, color=color_palette[i])

    total = sum(total_games.values())
    pie = figure(plot_height=350, title=f"Games Played in the Last 30 Days (Total: {total})", toolbar_location=None,
                 tools="hover", tooltips=[("Game:", "@games"), ("Played:", "@count")],
                 sizing_mode="scale_both", width=500, height=500, x_range=(-0.5, 1.5))
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

    data["colors"] = [element[1] for element in sorted((game, color) for game, color in
                                                       zip(data["games"], iter(color_palette)))]
    pie.wedge(x=0, y=0, radius=0.5,
              start_angle="start_angles", end_angle="end_angles", fill_color="colors",
              source=ColumnDataSource(data=data), legend_field="games")

    script, charts = components((plot, pie))
    return render_template("stats.html", js_resources=INLINE.render_js(), css_resources=INLINE.render_css(),
                           chart_data=script, charts=charts)
