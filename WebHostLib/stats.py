from collections import Counter, defaultdict
from itertools import cycle
from datetime import datetime, timedelta, date
from math import pi

from bokeh.embed import components
from bokeh.palettes import Dark2_8 as palette
from bokeh.plotting import figure, ColumnDataSource
from bokeh.resources import INLINE
from flask import render_template
from pony.orm import select

from . import app, cache
from .models import Room

pi2 = 2 * pi


@app.route('/stats')
@cache.memoize(timeout=60*60)  # regen once per hour should be plenty
def stats():
    plot = figure(title="Games played per day", x_axis_type='datetime', x_axis_label="Date", y_axis_label="Played",
                  sizing_mode="scale_both")
    games_played = defaultdict(Counter)
    total_games = Counter()
    room: Room
    games = set()
    cutoff = date.today()-timedelta(days=30000)
    for room in select(room for room in Room if room.creation_time >= cutoff):
        for slot in room.seed.slots:
            total_games[slot.game] += 1
            games.add(slot.game)
            games_played[room.creation_time.date()][slot.game] += 1
    days = sorted(games_played)
    cyc_palette = cycle(palette)
    for game in sorted(games):
        occurences = []
        for day in days:
            occurences.append(games_played[day][game])
        plot.line([datetime.combine(day, datetime.min.time()) for day in days],
                  occurences, legend_label=game, line_width=2, color=next(cyc_palette))
    total = sum(total_games.values())
    pie = figure(plot_height=350, title=f"Games played in the last 30 days. (Total: {total})", toolbar_location=None,
                 tools="hover", tooltips=[("Game:", "@games"), ("Played:", "@count")],
                 sizing_mode="scale_both")
    pie.axis.visible = False

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
        angle = count / total * pi2
        current_angle += angle
        data["end_angles"].append(current_angle)

    data["colors"] = [element[1] for element in sorted((game, color) for game, color in zip(data["games"], cycle(palette)))]
    pie.wedge(x=0.5, y=0.5, radius=0.5,
              start_angle="start_angles", end_angle="end_angles", fill_color="colors",
              source=ColumnDataSource(data=data), legend_field="games")

    script, charts = components((plot, pie))
    return render_template("stats.html", js_resources=INLINE.render_js(), css_resources=INLINE.render_css(),
                           chart_data=script, charts=charts)
