from flask import send_file, Response
from pony.orm import select

from Patch import update_patch_data
from WebHostLib import app, Slot, Room, Seed
import zipfile

@app.route("/dl_patch/<suuid:room_id>/<int:patch_id>")
def download_patch(room_id, patch_id):
    patch = Slot.get(id=patch_id)
    if not patch:
        return "Patch not found"
    else:
        import io

        room = Room.get(id=room_id)
        last_port = room.last_port

        patch_data = update_patch_data(patch.data, server=f"{app.config['PATCH_TARGET']}:{last_port}")
        patch_data = io.BytesIO(patch_data)

        fname = f"P{patch.player_id}_{patch.player_name}_{app.jinja_env.filters['suuid'](room_id)}.apbp"
        return send_file(patch_data, as_attachment=True, attachment_filename=fname)


@app.route("/dl_spoiler/<suuid:seed_id>")
def download_spoiler(seed_id):
    return Response(Seed.get(id=seed_id).spoiler, mimetype="text/plain")


@app.route("/dl_raw_patch/<suuid:seed_id>/<int:player_id>")
def download_raw_patch(seed_id, player_id: int):
    seed = Seed.get(id=seed_id)
    patch = select(patch for patch in seed.slots if
                   patch.player_id == player_id).first()

    if not patch:
        return "Patch not found"
    else:
        import io

        patch_data = update_patch_data(patch.data, server="")
        patch_data = io.BytesIO(patch_data)

        fname = f"P{patch.player_id}_{patch.player_name}_{app.jinja_env.filters['suuid'](seed_id)}.apbp"
        return send_file(patch_data, as_attachment=True, attachment_filename=fname)

@app.route("/slot_file/<suuid:room_id>/<int:player_id>")
def download_slot_file(room_id, player_id: int):
    room = Room.get(id=room_id)
    slot_data: Slot = select(patch for patch in room.seed.slots if
                   patch.player_id == player_id).first()

    if not slot_data:
        return "Slot Data not found"
    else:
        import io

        if slot_data.game == "Minecraft":
            from worlds.minecraft import mc_update_output
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_P{slot_data.player_id}_{slot_data.player_name}.apmc"
            data = mc_update_output(slot_data.data, server=app.config['PATCH_TARGET'], port=room.last_port)
            return send_file(io.BytesIO(data), as_attachment=True, attachment_filename=fname)
        elif slot_data.game == "Factorio":
            with zipfile.ZipFile(io.BytesIO(slot_data.data)) as zf:
                for name in zf.namelist():
                    if name.endswith("info.json"):
                        fname = name.rsplit("/", 1)[0]+".zip"
        else:
            return "Game download not supported."
        return send_file(io.BytesIO(slot_data.data), as_attachment=True, attachment_filename=fname)