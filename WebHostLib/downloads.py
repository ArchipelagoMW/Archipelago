import json
import zipfile
from io import BytesIO

from flask import send_file, Response, render_template
from pony.orm import select

from worlds.Files import AutoPatchRegister
from . import app, cache
from .models import Slot, Room, Seed


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
                manifest["server"] = f"{app.config['HOST_ADDRESS']}:{last_port}" if last_port else None
                with zipfile.ZipFile(new_file, "w") as new_zip:
                    for file in zf.infolist():
                        if file.filename == "archipelago.json":
                            new_zip.writestr("archipelago.json", json.dumps(manifest))
                        else:
                            new_zip.writestr(file.filename, zf.read(file), file.compress_type, 9)
            if "patch_file_ending" in manifest:
                patch_file_ending = manifest["patch_file_ending"]
            else:
                patch_file_ending = AutoPatchRegister.patch_types[patch.game].patch_file_ending
            fname = f"P{patch.player_id}_{patch.player_name}_{app.jinja_env.filters['suuid'](room_id)}" \
                    f"{patch_file_ending}"
            new_file.seek(0)
            return send_file(new_file, as_attachment=True, download_name=fname)
        else:
            return "Old Patch file, no longer compatible."


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

        if slot_data.game == "Factorio":
            with zipfile.ZipFile(io.BytesIO(slot_data.data)) as zf:
                for name in zf.namelist():
                    if name.endswith("info.json"):
                        fname = name.rsplit("/", 1)[0] + ".zip"
        elif slot_data.game == "Ocarina of Time":
            stream = io.BytesIO(slot_data.data)
            if zipfile.is_zipfile(stream):
                with zipfile.ZipFile(stream) as zf:
                    for name in zf.namelist():
                        if name.endswith(".zpf"):
                            fname = name.rsplit(".", 1)[0] + ".apz5"
            else: # pre-ootr-7.0 support
                fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_P{slot_data.player_id}_{slot_data.player_name}.apz5"
        elif slot_data.game == "VVVVVV":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_SP.apv6"
        elif slot_data.game == "Zillion":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_SP.apzl"
        elif slot_data.game == "Super Mario 64":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_SP.apsm64ex"
        elif slot_data.game == "Dark Souls III":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}.json"
        elif slot_data.game == "Kingdom Hearts 2":
            fname = f"AP_{app.jinja_env.filters['suuid'](room_id)}_P{slot_data.player_id}_{slot_data.player_name}.zip"
        elif slot_data.game == "Final Fantasy Mystic Quest":
            fname = f"AP+{app.jinja_env.filters['suuid'](room_id)}_P{slot_data.player_id}_{slot_data.player_name}.apmq"
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
