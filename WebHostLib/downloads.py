from flask import send_file, Response
from pony.orm import select

from Patch import update_patch_data
from WebHostLib import app, Patch, Room, Seed


@app.route("/dl_patch/<suuid:room_id>/<int:patch_id>")
def download_patch(room_id, patch_id):
    patch = Patch.get(id=patch_id)
    if not patch:
        return "Patch not found"
    else:
        import io

        room = Room.get(id=room_id)
        last_port = room.last_port
        pname = room.seed.multidata["names"][0][patch.player - 1]

        patch_data = update_patch_data(patch.data, server="berserkermulti.world:" + str(last_port))
        patch_data = io.BytesIO(patch_data)

        fname = f"P{patch.player}_{pname}_{app.jinja_env.filters['suuid'](room_id)}.bmbp"
        return send_file(patch_data, as_attachment=True, attachment_filename=fname)


@app.route("/dl_spoiler/<suuid:seed_id>")
def download_spoiler(seed_id):
    return Response(Seed.get(id=seed_id).spoiler, mimetype="text/plain")


@app.route("/dl_raw_patch/<suuid:seed_id>/<int:player_id>")
def download_raw_patch(seed_id, player_id):
    patch = select(patch for patch in Patch if patch.player == player_id and patch.seed.id == seed_id).first()

    if not patch:
        return "Patch not found"
    else:
        import io

        pname = patch.seed.multidata["names"][0][patch.player - 1]

        patch_data = update_patch_data(patch.data, server="")
        patch_data = io.BytesIO(patch_data)

        fname = f"P{patch.player}_{pname}_{app.jinja_env.filters['suuid'](seed_id)}.bmbp"
        return send_file(patch_data, as_attachment=True, attachment_filename=fname)
