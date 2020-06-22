"""Friendly reminder that if you want to host this somewhere on the internet, that it's licensed under MIT Berserker66
So unless you're Berserker you need to include license information."""

import json
import os
import logging
import typing
import multiprocessing
import threading
import zlib
import collections

from pony.flask import Pony
from flask import Flask, request, redirect, url_for, render_template, Response, session, abort, flash
from flask_caching import Cache
from pony.orm import commit

from .models import *

UPLOAD_FOLDER = os.path.relpath('uploads')
LOGS_FOLDER = os.path.relpath('logs')
os.makedirs(LOGS_FOLDER, exist_ok=True)


def allowed_file(filename):
    return filename.endswith('multidata')

app = Flask(__name__)
Pony(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 megabyte limit
# if you want persistent sessions on your server, make sure you make this a constant in your config.yaml
app.config["SECRET_KEY"] = os.urandom(32)
app.config['SESSION_PERMANENT'] = True
app.config["PONY"] = {
    'provider': 'sqlite',
    'filename': os.path.abspath('db.db3'),
    'create_db': True
}
app.config["CACHE_TYPE"] = "simple"

cache = Cache(app)

multiworlds = {}


@app.before_request
def register_session():
    session.permanent = True  # technically 31 days after the last visit
    if not session.get("_id", None):
        session["_id"] = uuid4()  # uniquely identify each session without needing a login


class MultiworldInstance():
    def __init__(self, room: Room):
        self.room_id = room.id
        self.process: typing.Optional[multiprocessing.Process] = None
        multiworlds[self.room_id] = self

    def start(self):
        if self.process and self.process.is_alive():
            return False

        logging.info(f"Spinning up {self.room_id}")
        with db_session:
            self.process = multiprocessing.Process(group=None, target=run_server_process,
                                                   args=(self.room_id, app.config["PONY"]),
                                                   name="MultiHost")
        self.process.start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None


@app.route('/seed/<int:seed>')
def view_seed(seed: int):
    seed = Seed.get(id=seed)
    if seed:
        return render_template("view_seed.html", seed=seed)
    else:
        abort(404)


@app.route('/new_room/<int:seed>')
def new_room(seed: int):
    seed = Seed.get(id=seed)
    room = Room(seed=seed, owner=session["_id"])
    commit()
    return redirect(url_for("host_room", room=room.id))


def _read_log(path: str):
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as log:
            yield from log
    else:
        yield f"Logfile {path} does not exist. " \
              f"Likely a crash during spinup of multiworld instance or it is still spinning up."


@app.route('/log/<int:room>')
def display_log(room: int):
    # noinspection PyTypeChecker
    return Response(_read_log(os.path.join("logs", str(room) + ".txt")), mimetype="text/plain;charset=UTF-8")


processstartlock = threading.Lock()


@app.route('/hosted/<int:room>', methods=['GET', 'POST'])
def host_room(room: int):
    room = Room.get(id=room)
    if request.method == "POST":
        if room.owner == session["_id"]:
            cmd = request.form["cmd"]
            Command(room=room, commandtext=cmd)
            commit()
    with db_session:
        multiworld = multiworlds.get(room.id, None)
        if not multiworld:
            multiworld = MultiworldInstance(room)

    with processstartlock:
        multiworld.start()

    return render_template("host_room.html", room=room)


@app.route('/tracker/<int:room>')
@cache.memoize(timeout=60)  # update every minute
def get_tracker(room: int):
    # This more WIP than the rest
    import Items
    def get_id(item_name):
        return Items.item_table[item_name][3]

    room = Room.get(id=room)
    if not room:
        abort(404)
    if room.allow_tracker:
        multidata = room.seed.multidata
        locations = {tuple(k): tuple(v) for k, v in multidata['locations']}

        links = {"Bow": "Progressive Bow",
                 "Silver Arrows": "Progressive Bow",
                 "Progressive Bow (Alt)": "Progressive Bow",
                 "Bottle (Red Potion)": "Bottle",
                 "Bottle (Green Potion)": "Bottle",
                 "Bottle (Blue Potion)": "Bottle",
                 "Bottle (Fairy)": "Bottle",
                 "Bottle (Bee)": "Bottle",
                 "Bottle (Good Bee)": "Bottle",
                 "Fighter Sword": "Progressive Sword",
                 "Master Sword": "Progressive Sword",
                 "Tempered Sword": "Progressive Sword",
                 "Golden Sword": "Progressive Sword",
                 "Power Glove": "Progressive Glove",
                 "Titans Mitts": "Progressive Glove"
                 }

        icons = {
            "Progressive Sword":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/cc/ALttP_Master_Sword_Sprite.png?version=55869db2a20e157cd3b5c8f556097725",
            "Pegasus Boots":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Pegasus_Shoes_Sprite.png?version=405f42f97240c9dcd2b71ffc4bebc7f9",
            "Progressive Glove":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/53/ALttP_Titan's_Mitt_Sprite.png?version=6ac54c3016a23b94413784881fcd3c75",
            "Flippers":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/88/ALttP_Zora's_Flippers_Sprite.png?version=b9d7521bb3a5a4d986879f70a70bc3da",
            "Moon Pearl":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Moon_Pearl_Sprite.png?version=d601542d5abcc3e006ee163254bea77e",
            "Progressive Bow":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Bow_%26_Arrows_Sprite.png?version=cfb7648b3714cccc80e2b17b2adf00ed",
            "Blue Boomerang":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c3/ALttP_Boomerang_Sprite.png?version=96127d163759395eb510b81a556d500e",
            "Red Boomerang":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/b9/ALttP_Magical_Boomerang_Sprite.png?version=47cddce7a07bc3e4c2c10727b491f400",
            "Hookshot":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/24/Hookshot.png?version=c90bc8e07a52e8090377bd6ef854c18b",
            "Mushroom":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/35/ALttP_Mushroom_Sprite.png?version=1f1acb30d71bd96b60a3491e54bbfe59",
            "Magic Powder":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Powder_Sprite.png?version=deaf51f8636823558bd6e6307435fb01",
            "Fire Rod":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d6/FireRod.png?version=6eabc9f24d25697e2c4cd43ddc8207c0",
            "Ice Rod":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d7/ALttP_Ice_Rod_Sprite.png?version=1f944148223d91cfc6a615c92286c3bc",
            "Bombos":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/8c/ALttP_Bombos_Medallion_Sprite.png?version=f4d6aba47fb69375e090178f0fc33b26",
            "Ether":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/3c/Ether.png?version=34027651a5565fcc5a83189178ab17b5",
            "Quake":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/56/ALttP_Quake_Medallion_Sprite.png?version=efd64d451b1831bd59f7b7d6b61b5879",
            "Lamp":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Lantern_Sprite.png?version=e76eaa1ec509c9a5efb2916698d5a4ce",
            "Hammer":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d1/ALttP_Hammer_Sprite.png?version=e0adec227193818dcaedf587eba34500",
            "Shovel":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c4/ALttP_Shovel_Sprite.png?version=e73d1ce0115c2c70eaca15b014bd6f05",
            "Flute":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/db/Flute.png?version=ec4982b31c56da2c0c010905c5c60390",
            "Bug Catching Net":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/54/Bug-CatchingNet.png?version=4d40e0ee015b687ff75b333b968d8be6",
            "Book of Mudora":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/22/ALttP_Book_of_Mudora_Sprite.png?version=11e4632bba54f6b9bf921df06ac93744",
            "Bottle":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ef/ALttP_Magic_Bottle_Sprite.png?version=fd98ab04db775270cbe79fce0235777b",
            "Cane of Somaria":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e1/ALttP_Cane_of_Somaria_Sprite.png?version=8cc1900dfd887890badffc903bb87943",
            "Cane of Byrna":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Cane_of_Byrna_Sprite.png?version=758b607c8cbe2cf1900d42a0b3d0fb54",
            "Cape":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/1/1c/ALttP_Magic_Cape_Sprite.png?version=6b77f0d609aab0c751307fc124736832",
            "Magic Mirror":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Mirror_Sprite.png?version=e035dbc9cbe2a3bd44aa6d047762b0cc",
            "Triforce":
                r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/4/4e/TriforceALttPTitle.png?version=dc398e1293177581c16303e4f9d12a48"
        }
        multi_items = {get_id(name) for name in ("Progressive Sword", "Progressive Bow", "Bottle")}
        links = {get_id(key): get_id(value) for key, value in links.items()}
        inventory = {teamnumber: {playernumber: collections.Counter() for playernumber in range(1, len(team) + 1)}
                     for teamnumber, team in enumerate(multidata["names"])}
        for (team, player), locations_checked in room.multisave.get("location_checks", {}):
            for location in locations_checked:
                item, recipient = locations[location, player]
                inventory[team][recipient][links.get(item, item)] += 1
        for (team, player), game_state in room.multisave.get("client_game_state", []):
            if game_state:
                inventory[team][player][106] = 1  # Triforce
        from MultiServer import get_item_name_from_id
        from Items import lookup_id_to_name
        player_names = {}
        for team, names in enumerate(multidata['names']):
            for player, name in enumerate(names, 1):
                player_names[(team, player)] = name
        tracking_names = ["Progressive Sword", "Progressive Bow", "Book of Mudora", "Hammer",
                          "Hookshot", "Magic Mirror", "Flute",
                          "Pegasus Boots", "Progressive Glove", "Flippers", "Moon Pearl", "Blue Boomerang",
                          "Red Boomerang", "Bug Catching Net", "Cane of Byrna", "Cape", "Mushroom", "Shovel", "Lamp",
                          "Magic Powder",
                          "Cane of Somaria", "Fire Rod", "Ice Rod", "Bombos", "Ether", "Quake",
                          "Bottle", "Triforce"]  # TODO make sure this list has what we need and sort it better
        tracking_ids = []

        for item in tracking_names:
            tracking_ids.append(get_id(item))

        return render_template("tracker.html", inventory=inventory, get_item_name_from_id=get_item_name_from_id,
                               lookup_id_to_name=lookup_id_to_name, player_names=player_names,
                               tracking_names=tracking_names, tracking_ids=tracking_ids, room=room, icons=icons,
                               multi_items=multi_items)
    else:
        return "Tracker disabled for this room."


from WebHost.customserver import run_server_process


@app.route('/', methods=['GET', 'POST'])
def upload_multidata():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        else:
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
            elif file and allowed_file(file.filename):
                try:
                    multidata = json.loads(zlib.decompress(file.read()).decode("utf-8-sig"))
                except:
                    flash("Could not load multidata. File may be corrupted or incompatible.")
                else:
                    seed = Seed(multidata=multidata)
                    commit()  # place into DB and generate ids
                    return redirect(url_for("view_seed", seed=seed.id))
            else:
                flash("Not recognized file format. Awaiting a .multidata file.")
    return render_template("upload_multidata.html")
