import collections.abc
import os
import yaml
import requests
import json
import flask

import Options
from Options import Visibility
from flask import redirect, render_template, request, Response
from worlds.AutoWorld import AutoWorldRegister
from Utils import local_path
from textwrap import dedent
from . import app, cache


def create():
    target_folder = local_path("WebHostLib", "static", "generated")
    yaml_folder = os.path.join(target_folder, "configs")

    Options.generate_yaml_templates(yaml_folder)


def get_world_theme(game_name: str):
    if game_name in AutoWorldRegister.world_types:
        return AutoWorldRegister.world_types[game_name].web.theme
    return 'grass'


def render_options_page(template: str, world_name: str, is_complex: bool = False):
    world = AutoWorldRegister.world_types[world_name]
    if world.hidden or world.web.options_page is False:
        return redirect("games")

    option_groups = {option: option_group.name
                     for option_group in world.web.option_groups
                     for option in option_group.options}
    ordered_groups = ["Game Options", *[group.name for group in world.web.option_groups]]
    grouped_options = {group: {} for group in ordered_groups}
    for option_name, option in world.options_dataclass.type_hints.items():
        # Exclude settings from options pages if their visibility is disabled
        if not is_complex and option.visibility < Visibility.simple_ui:
            continue

        if is_complex and option.visibility < Visibility.complex_ui:
            continue

        grouped_options[option_groups.get(option, "Game Options")][option_name] = option

    return render_template(
        template,
        world_name=world_name,
        world=world,
        option_groups=grouped_options,
        issubclass=issubclass,
        Options=Options,
        theme=get_world_theme(world_name),
    )


def generate_game(player_name: str, formatted_options: dict):
    payload = {
        "race": 0,
        "hint_cost": 10,
        "forfeit_mode": "auto",
        "remaining_mode": "disabled",
        "collect_mode": "goal",
        "weights": {
            player_name: formatted_options,
        },
    }
    r = requests.post("https://archipelago.gg/api/generate", json=payload)
    if 200 <= r.status_code <= 299:
        response_data = r.json()
        return redirect(response_data["url"])
    else:
        return r.text


def send_yaml(player_name: str, formatted_options: dict):
    response = Response(yaml.dump(formatted_options, sort_keys=False))
    response.headers["Content-Type"] = "text/yaml"
    response.headers["Content-Disposition"] = f"attachment; filename={player_name}.yaml"
    return response


@app.template_filter("dedent")
def filter_dedent(text: str):
    return dedent(text).strip("\n ")


@app.template_test("ordered")
def test_ordered(obj):
    return isinstance(obj, collections.abc.Sequence)


@app.route("/games/<string:game>/option-presets", methods=["GET"])
@cache.cached()
def option_presets(game: str) -> Response:
    world = AutoWorldRegister.world_types[game]
    presets = {}

    if world.web.options_presets:
        presets = presets | world.web.options_presets

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            from collections.abc import Set
            if isinstance(obj, Set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    json_data = json.dumps(presets, cls=SetEncoder)
    response = flask.Response(json_data)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/weighted-options")
def weighted_options_old():
    return redirect("games", 301)


@app.route("/games/<string:game>/weighted-options")
@cache.cached()
def weighted_options(game: str):
    return render_options_page("weightedOptions/weightedOptions.html", game, is_complex=True)


@app.route("/games/<string:game>/generate-weighted-yaml", methods=["POST"])
def generate_weighted_yaml(game: str):
    if request.method == "POST":
        intent_generate = False
        options = {}

        for key, val in request.form.items():
            if "||" not in key:
                if len(str(val)) == 0:
                    continue

                options[key] = val
            else:
                if int(val) == 0:
                    continue

                [option, setting] = key.split("||")
                options.setdefault(option, {})[setting] = int(val)

        # Error checking
        if "name" not in options:
            return "Player name is required."

        # Remove POST data irrelevant to YAML
        if "intent-generate" in options:
            intent_generate = True
            del options["intent-generate"]
        if "intent-export" in options:
            del options["intent-export"]

        # Properly format YAML output
        player_name = options["name"]
        del options["name"]

        formatted_options = {
            "name": player_name,
            "game": game,
            "description": f"Generated by https://archipelago.gg/ for {game}",
            game: options,
        }

        if intent_generate:
            return generate_game(player_name, formatted_options)

        else:
            return send_yaml(player_name, formatted_options)


# Player options pages
@app.route("/games/<string:game>/player-options")
@cache.cached()
def player_options(game: str):
    return render_options_page("playerOptions/playerOptions.html", game, is_complex=False)


# YAML generator for player-options
@app.route("/games/<string:game>/generate-yaml", methods=["POST"])
def generate_yaml(game: str):
    if request.method == "POST":
        options = {}
        intent_generate = False
        for key, val in request.form.items(multi=True):
            if key in options:
                if not isinstance(options[key], list):
                    options[key] = [options[key]]
                options[key].append(val)
            else:
                options[key] = val

        # Detect and build ItemDict options from their name pattern
        for key, val in options.copy().items():
            key_parts = key.rsplit("||", 2)
            if key_parts[-1] == "qty":
                if key_parts[0] not in options:
                    options[key_parts[0]] = {}
                if val != "0":
                    options[key_parts[0]][key_parts[1]] = int(val)
                del options[key]

        # Detect random-* keys and set their options accordingly
        for key, val in options.copy().items():
            if key.startswith("random-"):
                options[key.removeprefix("random-")] = "random"
                del options[key]

        # Error checking
        if not options["name"]:
            return "Player name is required."

        # Remove POST data irrelevant to YAML
        preset_name = 'default'
        if "intent-generate" in options:
            intent_generate = True
            del options["intent-generate"]
        if "intent-export" in options:
            del options["intent-export"]
        if "game-options-preset" in options:
            preset_name = options["game-options-preset"]
            del options["game-options-preset"]

        # Properly format YAML output
        player_name = options["name"]
        del options["name"]

        description = f"Generated by https://archipelago.gg/ for {game}"
        if preset_name != 'default' and preset_name != 'custom':
            description += f" using {preset_name} preset"

        formatted_options = {
            "name": player_name,
            "game": game,
            "description": description,
            game: options,
        }

        if intent_generate:
            return generate_game(player_name, formatted_options)

        else:
            return send_yaml(player_name, formatted_options)
