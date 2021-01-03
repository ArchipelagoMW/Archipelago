import pickle
from uuid import UUID

from . import api_endpoints
from flask import request, session, url_for
from pony.orm import commit

from WebHostLib import app, Generation, STATE_QUEUED, Seed, STATE_ERROR
from WebHostLib.check import get_yaml_data, roll_options


@api_endpoints.route('/generate', methods=['POST'])
def generate_api():
    try:
        options = {}
        race = False

        if 'file' in request.files:
            file = request.files['file']
            options = get_yaml_data(file)
            if type(options) == str:
                return {"text": options}, 400
            if "race" in request.form:
                race = bool(0 if request.form["race"] in {"false"} else int(request.form["race"]))

        json_data = request.get_json()
        if json_data:
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

        results, gen_options = roll_options(options)
        if any(type(result) == str for result in results.values()):
            return {"text": str(results),
                    "detail": results}, 400
        else:
            gen = Generation(
                options=pickle.dumps({name: vars(options) for name, options in gen_options.items()}),
                # convert to json compatible
                meta=pickle.dumps({"race": race}), state=STATE_QUEUED,
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
