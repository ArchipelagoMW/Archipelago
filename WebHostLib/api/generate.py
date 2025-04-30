import json
import pickle
from uuid import UUID

from flask import request, session, url_for
from markupsafe import Markup
from pony.orm import commit

from WebHostLib import app
from WebHostLib.check import get_yaml_data, roll_options
from WebHostLib.generate import get_meta
from WebHostLib.models import Generation, STATE_QUEUED, Seed, STATE_ERROR
from . import api_endpoints


@api_endpoints.route('/generate', methods=['POST'])
def generate_api():
    try:
        options = {}
        race = False
        meta_options_source = {}
        if 'file' in request.files:
            files = request.files.getlist('file')
            options = get_yaml_data(files)
            if isinstance(options, Markup):
                return {"text": options.striptags()}, 400
            if isinstance(options, str):
                return {"text": options}, 400
            if "race" in request.form:
                race = bool(0 if request.form["race"] in {"false"} else int(request.form["race"]))
            meta_options_source = request.form

        # json_data is optional, we can have it silently fall to None as it used to do.
        # See https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request.get_json -> Changelog -> 2.1
        json_data = request.get_json(silent=True)

        if json_data:
            meta_options_source = json_data
            if 'weights' in json_data:
                # example: options = {"player1weights" : {<weightsdata>}}
                options = json_data["weights"]
            if "race" in json_data:
                race = bool(0 if json_data["race"] in {"false"} else int(json_data["race"]))

        if not options:
            return {"text": "No options found. Expected file attachment or json weights."
                    }, 400

        if len(options) > app.config["MAX_ROLL"]:
            return {"text": "Max size of multiworld exceeded",
                    "detail": app.config["MAX_ROLL"]}, 409
        meta = get_meta(meta_options_source, race)
        results, gen_options = roll_options(options, set(meta["plando_options"]))
        if any(type(result) == str for result in results.values()):
            return {"text": str(results),
                    "detail": results}, 400
        else:
            gen = Generation(
                options=pickle.dumps({name: vars(options) for name, options in gen_options.items()}),
                # convert to json compatible
                meta=json.dumps(meta), state=STATE_QUEUED,
                owner=session["_id"])
            commit()
            return {"text": f"Generation of seed {gen.id} started successfully.",
                    "detail": gen.id,
                    "encoded": app.url_map.converters["suuid"].to_url(None, gen.id),
                    "wait_api_url": url_for("api.wait_seed_api", seed=gen.id, _external=True),
                    "url": url_for("wait_seed", seed=gen.id, _external=True)}, 201
    except Exception as e:
        return {"text": "Uncaught Exception:" + str(e)}, 500


@api_endpoints.route('/status/<suuid:seed>')
def wait_seed_api(seed: UUID):
    seed_id = seed
    seed = Seed.get(id=seed_id)
    if seed:
        return {"text": "Generation done"}, 201
    generation = Generation.get(id=seed_id)

    if not generation:
        return {"text": "Generation not found"}, 404
    elif generation.state == STATE_ERROR:
        return {"text": "Generation failed"}, 500
    return {"text": "Generation running"}, 202
