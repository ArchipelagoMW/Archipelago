import zipfile
import json
from io import BytesIO

from flask import send_file, Response, render_template
from pony.orm import select

from Patch import update_patch_data, preferred_endings, AutoPatchRegister
from WebHostLib import app, Slot, Room, Seed, cache


@app.route("/dl_patch/<suuid:room_id>/<int:patch_id>")
def download_patch(room_id, patch_id):
    patch = Slot.get(id=patch_id)
    if not patch:
        return "Patch not found"
    else:
        room = Room.get(id=room_id)
        last_port = room.last_port
        filelike = BytesIO(patch.data)
        greater_than_version_3 = zipfile.is_zipfile(filelike)
        if greater_than_version_3:
            # Python's zipfile module cannot overwrite/delete files in a zip, so we recreate the whole thing in ram
            new_file = BytesIO()
            with zipfile.ZipFile(filelike, "a") as zf:
                with zf.open("archipelago.json", "r") as f:
                    manifest = json.load(f)
                manifest["server"] = f"{app.config['PATCH_TARGET']}:{last_port}" if last_port else None
                with zipfile.ZipFile(new_file, "w") as new_zip:
                    for file in zf.infolist():
                        if file.filename == "archipelago.json":
                            new_zip.writestr("archipelago.json", json.dumps(manifest))
                        else:
                            new_zip.writestr(file.filename, zf.read(file), file.compress_type, 9)

            fname = f"P{patch.player_id}_{patch.player_name}_{app.jinja_env.filters['suuid'](room_id)}" \
                    f"{AutoPatchRegister.patch_types[patch.game].patch_file_ending}"
            new_file.seek(0)
            return send_file(new_file, as_attachment=True, download_name=fname)
        else:
            patch_data = update_patch_data(patch.data, server=f"{app.config['PATCH_TARGET']}:{last_port}")
            patch_data = BytesIO(patch_data)

            fname = f"P{patch.player_id}_{patch.player_name}_{app.jinja_env.filters['suuid'](room_id)}." \
                    f"{preferred_endings[patch.game]}"
        return send_file(patch_data, as_attachment=True, download_name=fname)


@app.route("/dl_spoiler/<suuid:seed_id>")
def download_spoiler(seed_id):
    return Response(Seed.get(id=seed_id).spoiler, mimetype="text/plain")


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
            return send_file(io.BytesIO(data), as_attachment=True, download_name=fname)
        elif slot_data.game == "Factorio":
            with zipfile.ZipFile(io.BytesIO(slot_data.data)) as zf:
                for name in zf.namelist():
                    if name.endswith("info.json"):
                        fname = name.rsplit("/", 1)[0] + ".zip"
        elif slot_data.game == "Ocarina of Time":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_P{slot_data.player_id}_{slot_data.player_name}.apz5"
        elif slot_data.game == "VVVVVV":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_SP.apv6"
        elif slot_data.game == "Super Mario 64":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_SP.apsm64ex"
        elif slot_data.game == "Dark Souls III":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}.json"
        else:
            return "Game download not supported."
        return send_file(io.BytesIO(slot_data.data), as_attachment=True, download_name=fname)


@app.route("/templates")
@cache.cached()
def list_yaml_templates():
    files = []
    from worlds.AutoWorld import AutoWorldRegister
    for world_name, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            files.append(world_name)
    return render_template("templates.html", files=files)
