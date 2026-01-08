from __future__ import annotations
import os
import sys
import asyncio
import shutil
import aiohttp
import webbrowser
import time
import ast

import ModuleUpdate

ModuleUpdate.update()

import Utils

if __name__ == "__main__":
    Utils.init_logging("osu!Client", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


class APosuClientCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: APosuContext):
        super().__init__(ctx)
        self.ctx = ctx
        self.mode_names = {'fruits': 'fruits',
                           'catch': 'fruits',
                           'ctb': 'fruits',
                           '4k': 'mania',
                           '7k': 'mania',
                           'o!m': 'mania',
                           'mania': 'mania',
                           'osu': 'osu',
                           'std': 'osu',
                           'standard': 'osu',
                           'taiko': 'taiko',
                           '': ''}
        self.download_types = {'mirror': 'mirror',
                               'direct': 'direct'}

    # def _cmd_slot_data(self):
    #    """Show Slot Data, For Debug Purposes. Probably don't run this"""
    #    self.output(f"Data: {str(self.ctx.pairs)}")
    #    pass

    def _cmd_set_api_key(self, key=""):
        """Sets the Client Secret, generated in the "OAuth" Section of Account Settings"""
        os.environ['API_KEY'] = key
        self.output(f"Set to ##################")

    def _cmd_set_client_id(self, id=""):
        """Sets the Client ID, generated in the "OAuth" Section of Account Settings"""
        os.environ['CLIENT_ID'] = id
        self.output(f"Set to {id}")

    def _cmd_set_player_id(self, id=""):
        """Sets the player's user ID, found in the URL of their profile"""
        os.environ['PLAYER_ID'] = id
        self.output(f"Set to {id}")

    def _cmd_save_keys(self):
        """Saves the player's current IDs"""
        filename = "config"
        path = self.ctx.game_communication_path+' config'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, filename), 'w') as f:
            for info in [os.environ['API_KEY'], os.environ['CLIENT_ID'], os.environ['PLAYER_ID']]:
                f.write(info)
                f.write(" ")
        self.output("Saved Current Keys")

    def _cmd_load_keys(self):
        """loads the player's previously saved IDs"""
        filename = "config"
        path = self.ctx.game_communication_path+' config'
        with open(os.path.join(path, filename), 'r') as f:
            data = f.read()
        d = data.split(" ")
        os.environ['API_KEY'], os.environ['CLIENT_ID'], os.environ['PLAYER_ID'] = d[0], d[1], d[2],
        self.output("Loaded Previous Keys")

    def _cmd_save_settings(self):
        """Saves the player's current settings. Doesn't include API keys or IDs."""
        filename = "settings"
        path = self.ctx.game_communication_path+' config'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, filename), 'w') as f:
            for info in [self.ctx.auto_modes, self.ctx.auto_download, self.ctx.download_type]:
                f.write(str(info))
                f.write("\t")
        self.output("Saved Auto Tracking, Auto Download, and Download Type Settings.")

    def _cmd_load_settings(self):
        """Loads the player's previously saved settings. Doesn't include API keys or IDs."""
        filename = "settings"
        path = self.ctx.game_communication_path+' config'
        with open(os.path.join(path, filename), 'r') as f:
            data = f.read()
        d = data.split("\t")
        self.ctx.auto_modes, self.ctx.auto_download, self.ctx.download_type = ast.literal_eval(d[0]), ast.literal_eval(d[1]), d[2],
        self.output("Loaded Previous Settings")

    def _cmd_save_all(self):
        """Saves both the player's current IDs, and their settings."""
        filename = "config"
        path = self.ctx.game_communication_path+' config'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, filename), 'w') as f:
            for info in [os.environ['API_KEY'], os.environ['CLIENT_ID'], os.environ['PLAYER_ID']]:
                f.write(info)
                f.write(" ")
        self.output("Saved Current Keys")
        filename = "settings"
        path = self.ctx.game_communication_path + ' config'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, filename), 'w') as f:
            for info in [self.ctx.auto_modes, self.ctx.auto_download, self.ctx.download_type]:
                f.write(str(info))
                f.write("\t")
        self.output("Saved Auto Tracking, Auto Download, and Download Type Settings.")

    def _cmd_load_all(self):
        """loads the player's previously saved IDs, and their settings."""
        filename = "config"
        path = self.ctx.game_communication_path+' config'
        with open(os.path.join(path, filename), 'r') as f:
            data = f.read()
            d = data.split(" ")
            os.environ['API_KEY'], os.environ['CLIENT_ID'], os.environ['PLAYER_ID'] = d[0], d[1], d[2],
            self.output("Loaded Previous Keys")
        filename = "settings"
        path = self.ctx.game_communication_path + ' config'
        with open(os.path.join(path, filename), 'r') as f:
            data = f.read()
        d = data.split("\t")
        self.ctx.auto_modes, self.ctx.auto_download, self.ctx.download_type = ast.literal_eval(d[0]), ast.literal_eval(d[1]), d[2],
        self.output("Loaded Previous Settings")

    def _cmd_songs(self):
        """Display all songs in logic."""
        indexes = get_available_ids(self.ctx)
        self.output(f"You Have {count_item(self.ctx, 726999999)} Performance Points, you need {self.ctx.preformance_points_needed} to unlock your goal.")
        self.output(f"You currently have {len(indexes)} songs in Logic")
        for i in indexes:
            song = list(self.ctx.pairs.keys())[i]
            beatmapset = self.ctx.pairs[song]
            self.output(f"{song}: {beatmapset['title']} (ID: {beatmapset['id']})")

    def _cmd_all_songs(self):
        """Displays all songs included in current generation."""
        played_songs = get_played_songs(self.ctx)
        self.output(f"You have played {len(played_songs)}/{len(self.ctx.pairs)-1} songs")
        for song in self.ctx.pairs:
            beatmapset = self.ctx.pairs[song]
            self.output(f"{song}: {beatmapset['title']} (ID: {beatmapset['id']}) {'(passed)' if song in played_songs else ''}")

    def _cmd_update(self, mode=''):
        """Gets the player's last score, in a given gamemode or their set default"""
        asyncio.create_task(get_last_scores(self, mode))

    def _cmd_download(self, number=''):
        """Downloads the given song number in '/songs'. Also Accepts "Next" and "Victory"."""
        if number.lower() == 'next':
            if len(get_available_ids(self.ctx)) > 0:
                number = get_available_ids(self.ctx)[0]+1
            else:
                self.output("You have no songs to download")
                return
        try:
            song_number = int(number)-1
        except ValueError:
            if not (number.lower().capitalize() == 'Victory'):
                self.output("Please Give a Number, 'next' or 'Victory'")
                return
            song_number = -1
        try:
            song = list(self.ctx.pairs.keys())[song_number]
        except IndexError:
            self.output("Use the Song Numbers in '/songs' (Not the IDs)")
            return
        beatmapset = self.ctx.pairs[song]
        if self.ctx.download_type == 'mirror':
            self.output(f"Downloading {song}: {beatmapset['title']} (ID: {beatmapset['id']}) as '{beatmapset['id']} {beatmapset['artist']} - {beatmapset['title']}.osz'")
            asyncio.create_task(self.download_beatmapset(beatmapset))
            return
        if self.ctx.download_type == 'direct':
            self.output(f"Opening {song}: {beatmapset['title']} (ID: {beatmapset['id']}) in osu!Direct")
            # Newer versions of this APworld have difficulty IDs, older ones do not
            try:
                asyncio.create_task(open_set_in_direct(self.ctx, beatmapset['diffs'][0]))
            except KeyError:
                self.output("No Difficulty ID found, attempting fallback")
                asyncio.create_task(open_set_in_direct(self.ctx, beatmapset['id'], True))

    def _cmd_auto_track(self, mode=''):
        """Toggles Auto Tracking for the Given Mode (or "All"). Supports Multiple Modes."""
        try:
            [os.environ['API_KEY'], os.environ['CLIENT_ID'], os.environ['PLAYER_ID']]
        except KeyError:
            self.output('Please set your Client ID, Client Secret, and Player ID')
            return
        if mode.lower() == 'all':
            self.ctx.auto_modes = ['osu', 'fruits', 'taiko', 'mania']
            self.output('Auto Tracking Enabled for all modes')
            return
        if mode.lower() in self.mode_names.keys():
            if self.mode_names[mode.lower()] not in self.ctx.auto_modes:
                self.ctx.auto_modes.append(self.mode_names[mode.lower()])
                self.output(f'Auto Tracking Enabled{f" for {mode}" if mode else " for your default mode"}')
                return
            self.output(f'Auto Tracking Disabled{f" for {mode}" if mode else " for your default mode"}')
            self.ctx.auto_modes.remove(self.mode_names[mode.lower()])
            return
        self.output('Please Supply a Valid Mode')

    def _cmd_auto_download(self):
        """Toggles Auto Downloads when Auto Tracking"""
        try:
            [os.environ['API_KEY'], os.environ['CLIENT_ID']]
        except KeyError:
            self.output('Please set your Client ID, and Client Secret')
            return
        self.ctx.auto_download = not self.ctx.auto_download
        if self.ctx.auto_download:
            self.output('Toggled Auto Downloading On')
            return
        self.output('Toggled Auto Downloading Off')

    def _cmd_download_type(self, download_type=''):
        """Sets Download type. Valid Options are 'Direct' and 'Mirror'"""
        try:
            [os.environ['API_KEY'], os.environ['CLIENT_ID']]
        except KeyError:
            self.output('Please set your Client ID, and Client Secret')
            return
        if download_type.lower() in self.download_types:
            self.ctx.download_type = self.download_types[download_type.lower()]
            self.output(f'Download type set to "{self.ctx.download_type.capitalize()}"')
            return
        self.output('Please Use Either "Direct" or "Mirror"')

    def _cmd_check_diff(self, number=''):
        """Outputs the difficulties of a given song number that are in logic. Only Applies for Difficulty Sync."""
        try:
            [os.environ['API_KEY'], os.environ['CLIENT_ID']]
        except KeyError:
            self.output('Please set your Client ID, and Client Secret')
            return
        if number.lower() == 'next':
            if len(get_available_ids(self.ctx)) > 0:
                number = get_available_ids(self.ctx)[0]+1
            else:
                self.output("You have no songs in logic")
                return
        try:
            song_number = int(number)-1
        except ValueError:
            if not (number.lower().capitalize() == 'Victory'):
                self.output("Please Give a Number, 'next' or 'Victory'")
                return
            song_number = -1
        try:
            song = list(self.ctx.pairs.keys())[song_number]
        except IndexError:
            self.output("Use the Song Numbers in '/songs' (Not the IDs)")
            return
        if not self.ctx.difficulty_sync:
            self.output("You aren't using difficulty sync.")
            return
        beatmapset = self.ctx.pairs[song]
        asyncio.create_task(self.get_diff_name(beatmapset))

    async def get_diff_name(self, song):
        if not self.ctx.token:
            await get_token(self.ctx)
        url = f"https://osu.ppy.sh/api/v2/beatmapsets/{song['id']}"
        headers = {"Accept": "application/json", "Content-Type": "application/json",
                   "Authorization": f"Bearer {self.ctx.token}"}
        async with aiohttp.request("GET", url, headers=headers) as request:
            beatmapset = await request.json()
        for i in beatmapset['beatmaps']:
            if i['id'] in song['diffs']:
                self.output(f'{i["version"]} - {i["difficulty_rating"]}*')

    def check_location(self, score):
        self.output(score['beatmapset']['title'] + " " + score['beatmap']['version'] + f' Passed: {score["passed"]}')
        # Check if the score is a pass, then check if it's in the AP
        if not score['passed']:
            # self.output("You cannot check a location without passing the song")
            return
        if self.ctx.disable_difficulty_reduction and any(mod['acronym'] in ['NF', 'EZ', 'HT', 'DC'] for mod in score['mods']):
            self.output("Your current settings do not allow difficulty reduction mods.")
            return
        if self.ctx.minimum_grade:
            grade = calculate_grade(score)
            grades = ['X', 'S', 'A', 'B', 'C', 'D']
            if grades.index(grade) >= self.ctx.minimum_grade:
                required_grade = 'SS' if grades[self.ctx.minimum_grade-1] == 'X' else grades[self.ctx.minimum_grade-1]
                self.output(f"You did not get a high enough grade. You need atleast a"
                            f"{'n' if required_grade == 'A' else ''} {required_grade} Rank")
                return
        for song in self.ctx.pairs:
            if self.ctx.pairs[song]['id'] == score['beatmapset']['id']:
                self.output(f'Play Matches {song}')
                # check for the correct diff
                if self.ctx.difficulty_sync and score['beatmap_id'] not in self.ctx.pairs[song]['diffs']:
                    self.output('The incorrect difficulty was played')
                    self.output(f'The correct difficulty(ies) is: {self.ctx.pairs[song]["diffs"]}')
                    return
                # check for converts
                if self.ctx.disallow_converts:
                    # Find the diff that was played
                    for beatmap in self.ctx.pairs[song]['beatmaps']:
                        if beatmap['id'] == score['beatmap_id']:
                            # Only Standard maps can be converted
                            if score['ruleset_id'] != 0 and beatmap['mode'] == 'osu':
                                self.output('Your settings do not allow converts')
                                return
                if song == "Victory":
                    if count_item(self.ctx, 726999999) >= self.ctx.preformance_points_needed:
                        message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
                        asyncio.create_task(self.ctx.send_msgs(message))
                        return
                    self.output("You don't have enough preformance points")
                    return
                if not count_item(self.ctx, 727000000 + list(self.ctx.pairs.keys()).index(song)):
                    self.output("You don't have this song unlocked")
                    return
                locations = []
                for i in range(2):
                    location_id = 727000000 + (2 * list(self.ctx.pairs.keys()).index(song)) + i
                    if location_id in self.ctx.missing_locations:
                        if location_id in self.ctx.missing_locations:
                            locations.append(int(location_id))
                if locations:
                    message = [{"cmd": 'LocationChecks', "locations": locations}]
                    task = asyncio.create_task(self.ctx.send_msgs(message))
                    if self.ctx.auto_download:
                        asyncio.create_task(download_next_beatmapset(self, task))

    async def download_beatmapset(self, beatmapset):
        print(f'Downloading {beatmapset["artist"]} - {beatmapset["title"]} ({beatmapset["id"]})')
        try:
            async with aiohttp.request("GET", f"https://beatconnect.io/b/{beatmapset['id']}") as req:
                content_length = req.headers.get('Content-Length')
                req_status = req.status
                if req_status != 200:
                    # The library doesn't have a built-in way to get the status name in our version of aiohttp, so we have to do it manually sadly
                    # I have only included the most likely status codes to be returned by beatconnect
                    http_status_names = {
                        400: 'Bad Request',
                        401: 'Unauthorized',
                        403: 'Forbidden',
                        404: 'Not Found',
                        408: 'Request Timeout',
                        429: 'Too Many Requests',
                        500: 'Internal Server Error',
                        502: 'Bad Gateway',
                        503: 'Service Unavailable',
                        504: 'Gateway Timeout',
                    }
                    self.output(f'Error Downloading {beatmapset["id"]} {beatmapset["artist"]} - {beatmapset["title"]}.osz')
                    self.output(f'Please Manually Add the Map or Try Again Later. ({req_status} - {http_status_names.get(req_status, "Unknown Error")})')
                    return
                # With beatconnect we always know the total size of the download, so this is always true
                if content_length is not None:
                    total_bytes = int(content_length)
                    total_mb = total_bytes / (1024 ** 2)
                    # Beatconnect is slow to respond, so this message will appear when the download starts unlike when you run the command
                    self.output(f"Starting download of beatmapset ({total_mb:.2f}MB)")

                downloaded_content = []
                downloaded_bytes = 0
                last_print_time = time.time()
                async for chunk in req.content.iter_any():
                    downloaded_content.append(chunk)
                    downloaded_bytes += len(chunk)
                    downloaded_mb = downloaded_bytes / (1024 ** 2)

                    # If we know the total size, calculate the progress
                    if content_length is not None:
                        progress = min(100, int(downloaded_bytes / total_bytes * 100))

                        # Check if at least half a second has passed since last print or if the download is done
                        # Filesizes are small enough that we can do half a second intervals instead of 1 second
                        current_time = time.time()
                        if current_time - last_print_time >= 0.5 or downloaded_bytes == total_bytes:
                            self.output(f"Downloaded: {downloaded_mb:.2f}MB / {total_mb:.2f}MB ({progress}%)")
                            last_print_time = current_time

                    # If we don't know the total size, just print the downloaded amount
                    else:
                        self.output(f"Downloaded: {downloaded_mb:.2f}MB")

                # Combine all the chunks into one just like req.read() would do
                content = b"".join(downloaded_content)
            f = f'{beatmapset["id"]} {beatmapset["artist"]} - {beatmapset["title"]}.osz'
            filename = "".join(i for i in f if i not in "\/:*?<>|\"")
            path = os.path.join(self.ctx.game_communication_path, 'config')

            if not os.path.exists(path):
                os.makedirs(path)

            file_path = os.path.join(path, filename)
            with open(file_path, 'wb') as f:
                f.write(content)

            self.output(f'Opening {filename}...')  # More feedback to the user
            webbrowser.open(file_path)
        except Exception as e:
            self.output(f"An error occurred: {repr(e)}")




class APosuContext(CommonContext):
    command_processor: int = APosuClientCommandProcessor
    game = "osu!"
    items_handling = 0b111  # full remote
    want_slot_data = True

    def __init__(self, server_address, password):
        super(APosuContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.pairs: dict = {}
        self.last_scores: list = []
        self.auto_modes: list[str] = []
        self.auto_download: bool = False
        self.download_type: str = 'mirror'
        self.token: str = ''
        self.disable_difficulty_reduction: bool = False
        self.all_locations: list[int] = []
        self.difficulty_sync = 0
        self.minimum_grade = 0
        self.disallow_converts = False
        self.preformance_points_needed = 9999  # High Enough to never accidently trigger if the slot data fails
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%/APosu")
        else:
            # not windows. game is an exe so let's see if wine might be around to run it
            if "WINEPREFIX" in os.environ:
                wineprefix = os.environ["WINEPREFIX"]
            elif shutil.which("wine") or shutil.which("wine-stable"):
                wineprefix = os.path.expanduser(
                    "~/.wine")  # default root of wine system data, deep in which is app data
            else:
                msg = "APosuClient couldn't detect system type. Unable to infer required game_communication_path"
                logger.error("Error: " + msg)
                Utils.messagebox("Error", msg, error=True)
                sys.exit(1)
            self.game_communication_path = os.path.join(
                wineprefix,
                "drive_c",
                os.path.expandvars("users/$USER/Local Settings/Application Data/APosu"))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(APosuContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(APosuContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(APosuContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            print(args)
            slot_data = args.get('slot_data', None)
            if slot_data:
                self.pairs = slot_data.get('Pairs', {})
                self.preformance_points_needed = slot_data.get('PreformancePointsNeeded', 9999)
                self.disable_difficulty_reduction = slot_data.get('DisableDifficultyReduction', False)
                self.difficulty_sync = slot_data.get('DifficultySync', 0)
                self.minimum_grade = slot_data.get('MinimumGrade', 0)
                self.disallow_converts = slot_data.get('DisallowConverts', False)
                version = slot_data.get('VersionNumber', None)
                if version is None:
                    pass
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class OsuManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago osu! Client"

        self.ui = OsuManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def count_item(ctx, code) -> int:
    current = 0
    for item in ctx.items_received:
        if item.item == code:
            current += 1
    return current


def get_available_ids(ctx):
    # Gets the Index of each Song the player has but has not played
    incomplete_items = []
    for item in ctx.items_received:
        song_index = item.item-727000000
        location_id = (song_index*2)+727000000
        if (location_id in ctx.missing_locations or location_id+1 in ctx.missing_locations) and song_index not in incomplete_items:
            incomplete_items.append(song_index)
    if count_item(ctx, 726999999) >= ctx.preformance_points_needed:
        incomplete_items.append(-1)
    incomplete_items.sort()
    return incomplete_items


async def get_token(ctx):
    try:
        async with aiohttp.request("POST", "https://osu.ppy.sh/oauth/token",
                                    headers={"Accept": "application/json",
                                    "Content-Type": "application/x-www-form-urlencoded"},
                                    data=f"client_id={os.environ['CLIENT_ID']}&client_secret={os.environ['API_KEY']}"
                                         f"&grant_type=client_credentials&scope=public") as authreq:
            tokenjson = await authreq.json()
            print(tokenjson)
            ctx.token = tokenjson['access_token']
    except KeyError:
        print('nokey')
        return


async def open_set_in_direct(ctx, diff_id: int, fallback: bool = False) -> None:
    # If the beatmapset has no difficulty ID, we have to fall back to the beatmap ID as done in previous versions
    if fallback:
        set_id = diff_id
        if not ctx.token:
            await get_token(ctx)
        url = f"https://osu.ppy.sh/api/v2/beatmapsets/{set_id}"
        headers = {"Accept": "application/json", "Content-Type": "application/json",
                   "Authorization": f"Bearer {ctx.token}"}
        async with aiohttp.request("GET", url, headers=headers) as conversion:
            beatmapset = await conversion.json()
            print(beatmapset)
        webbrowser.open(f"osu://b/{beatmapset['beatmaps'][0]['id']}")
        return
    # otherwise we can just open the first diff directly
    webbrowser.open(f"osu://b/{diff_id}")

# This is the silent version of the function below where this one is used in game watcher
async def download_next_beatmapset_silent(ctx, task):
    await task
    await asyncio.sleep(1)  # Delay to get the reply
    if len(get_available_ids(ctx)) <= 0:
        return
    beatmapset = ctx.pairs[list(ctx.pairs.keys())[get_available_ids(ctx)[0]]]
    if ctx.download_type == 'direct':
        try:
            asyncio.create_task(open_set_in_direct(ctx, beatmapset['diffs'][0]))
        except KeyError:
            asyncio.create_task(open_set_in_direct(ctx, beatmapset['id'], True))
        return
    print(f'Downloading {beatmapset["artist"]} - {beatmapset["title"]} ({beatmapset["id"]})')
    try:
        async with aiohttp.request("GET", f"https://beatconnect.io/b/{beatmapset['id']}") as req:
            content = await req.read()
            req_status = req.status
        if req_status != 200:
            print(f'Download Failed, Status Code: {req_status}')
            return
        f = f'{beatmapset["id"]} {beatmapset["artist"]} - {beatmapset["title"]}.osz'
        filename = "".join(i for i in f if i not in "\/:*?<>|\"")
        path = os.path.join(ctx.game_communication_path, 'config')

        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, filename)
        with open(file_path, 'wb') as f:
            f.write(content)

        webbrowser.open(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")

# This is the non-silent version of the function above where this one is used in the update command
async def download_next_beatmapset(self, task):
    await task
    await asyncio.sleep(0.2)  # Delay to get the reply
    if len(get_available_ids(self.ctx)) <= 0:
        return
    beatmapset = self.ctx.pairs[list(self.ctx.pairs.keys())[get_available_ids(self.ctx)[0]]]
    if self.ctx.download_type == 'direct':
        self.output(f'Opening {beatmapset["artist"]} - {beatmapset["title"]} ({beatmapset["id"]}) in osu!Direct')
        try:
            asyncio.create_task(open_set_in_direct(self.ctx, beatmapset['diffs'][0]))
        except KeyError:
            self.output("No Difficulty ID found, attempting fallback")
            asyncio.create_task(open_set_in_direct(self.ctx, beatmapset['id'], True))
        return
    self.output(f'Downloading {beatmapset["artist"]} - {beatmapset["title"]} ({beatmapset["id"]})')
    try:
        async with aiohttp.request("GET", f"https://beatconnect.io/b/{beatmapset['id']}") as req:
            content = await req.read()
            req_status = req.status
        if req_status != 200:
            self.output(f'Download Failed, Status Code: {req_status}')
            return
        f = f'{beatmapset["id"]} {beatmapset["artist"]} - {beatmapset["title"]}.osz'
        filename = "".join(i for i in f if i not in "\/:*?<>|\"")
        path = os.path.join(self.ctx.game_communication_path, 'config')

        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, filename)
        with open(file_path, 'wb') as f:
            f.write(content)

        webbrowser.open(file_path)
    except Exception as e:
        self.output(f"An error occurred: {e}")

# This is the silent version of the function below where this one is used in game watcher
async def auto_get_last_scores(ctx, mode=''):
    # Make URl for the request
    try:
        request = f"https://osu.ppy.sh/api/v2/users/{os.environ['PLAYER_ID']}/scores/recent?include_fails=1&limit=10"
    except KeyError:
        print('No Player ID')
        return
    # Add Mode to request, otherwise it will use the user's default
    if mode:
        request += f"&mode={mode}"
    if not ctx.token:
        await get_token(ctx)
    headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {ctx.token}", "x-api-version" : "20240529"}
    async with aiohttp.request("GET", request, headers=headers) as scores:
        try:
            score_list = await scores.json()
            print(score_list, "a")
            print(scores)
        except (KeyError, IndexError):
            await get_token(ctx)
            print("Error Retrieving plays, Check your API Key.")
            return
    if not score_list:
        print("No Plays Found. Check the Gamemode")
        return
    found = False
    for score in score_list:
        if score['ended_at'] in ctx.last_scores:
            if not found:
                print("No New Plays Found.")
            return
        found = True
        ctx.last_scores.append(score['ended_at'])
        if len(ctx.last_scores) > 100:
            ctx.last_scores.pop(0)
        check_location(ctx, score)

# This is the non-silent version of the function above where this one is used in the update command
async def get_last_scores(self, mode=''):
    # Make URl for the request
    try:
        request = f"https://osu.ppy.sh/api/v2/users/{os.environ['PLAYER_ID']}/scores/recent?include_fails=1&limit=100"
    except KeyError:
        self.output('Set a Player ID')
        return
    # Add Mode to request, otherwise it will use the user's default
    if mode and mode.lower() in self.mode_names.keys():
        request += f"&mode={self.mode_names[mode.lower()]}"
    if not self.ctx.token:
        await get_token(self.ctx)
    headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {self.ctx.token}", "x-api-version": "20240529"}
    async with aiohttp.request("GET", request, headers=headers) as scores:
        try:
            score_list = await scores.json()
        except (KeyError, IndexError):
            await get_token(self.ctx)
            self.output("Error Retrieving plays, Check your API Key.")
            return
    if not score_list:
        self.output("No Plays Found. Check the Gamemode")
        return
    found = False
    for score in score_list:
        if score['ended_at'] in self.ctx.last_scores:
            if not found:
                self.output("No New Plays Found.")
            return
        found = True
        self.ctx.last_scores.append(score['ended_at'])
        if len(self.ctx.last_scores) > 100:
            self.ctx.last_scores.pop(0)
        self.check_location(score)


# calculates the grade of a score with the ability to differentiate between stable and lazer scores
def calculate_grade(score):
    acc = float(score['accuracy'])
    gamemode = int(score['ruleset_id'])

    # if the score has 100% accuracy, then it is an SS no matter gamemode or grading system
    # skip the rest of the checks
    if acc == 1:
        return 'X'

    # if this score has the Classic mod enabled or if it has a legacy id, then we assume it is a stable score
    elif any(mod['acronym'] == 'CL' for mod in score['mods']) or score['legacy_score_id']:
        if gamemode == 0 or gamemode == 1: # osu!standard or osu!taiko

            # for some reason these statistics are missing if you get 0 of any of these
            # so we have to check if they exist before we try to get them
            miss_count = int(score['statistics'].get('miss', 0) or 0)
            num_300s = int(score['statistics'].get('great', 0) or 0)
            num_100s = int(score['statistics'].get('ok', 0) or 0)
            num_50s = int(score['statistics'].get('meh', 0) or 0)
            total_judgements = miss_count + num_300s + num_100s + num_50s
            percent_300s = num_300s / total_judgements
            precent_50s = num_50s / (num_300s + num_100s + num_50s)
            if miss_count == 0 and precent_50s <= 0.01:
                if percent_300s > 0.9: return 'S'
                if percent_300s > 0.8: return 'A'
                if percent_300s > 0.7: return 'B'
                if percent_300s > 0.6: return 'C'
                return 'D'
            else:
                if percent_300s > 0.9: return 'A'
                if percent_300s > 0.8: return 'B'
                if percent_300s > 0.6: return 'C'
                return 'D'
        elif gamemode == 2:  # osu!catch
            if acc > 0.98: return 'S'
            if acc > 0.94: return 'A'
            if acc > 0.9: return 'B'
            if acc > 0.85: return 'C'
            return 'D'
        elif gamemode == 3:  # osu!mania
            # Mania's Accuracy with classic mod is different from stable, so we have to do it manually
            mania_total = 300 * score['statistics'].get('perfect', 0)  # Perfects are worth 305 with classic mod
            mania_total += 300 * score['statistics'].get('great', 0)
            mania_total += 200 * score['statistics'].get('good', 0)
            mania_total += 100 * score['statistics'].get('ok', 0)
            mania_total += 50 * score['statistics'].get('meh', 0)
            mania_total += 0 * score['statistics'].get('miss', 0)
            mania_acc = mania_total / (sum(score['statistics'].values()) * 300)  # This is also out of 305 on laser
            if mania_acc > 0.95: return 'S'
            if mania_acc > 0.9: return 'A'
            if mania_acc > 0.8: return 'B'
            if mania_acc > 0.7: return 'C'
            return 'D'
    # if it is a lazer score, then the API did all the work for us
    else:
        return score['rank'].replace('XH', 'X').replace('SH', 'S')  # remove hidden and flashlight from the grade

def get_played_ids(ctx):
    # Gets the Index of each Song the player has played
    played_items = []
    for item in ctx.items_received:
        song_index = item.item-727000000
        location_id = (song_index*2)+727000000
        if location_id < 727000000: continue
        if (location_id not in ctx.missing_locations and location_id+1 not in ctx.missing_locations) and song_index not in played_items:
            played_items.append(song_index)
    played_items.sort()
    return played_items


def get_played_songs(ctx):
    # Gets the Song value of each Song the player has played
    played_ids = get_played_ids(ctx)
    played_songs = []
    for played in played_ids:
        played_songs.append(list(ctx.pairs.keys())[played])
    return played_songs


def check_location(ctx, score):
    if not score['passed']:
        return
    if ctx.disable_difficulty_reduction and any(mod['acronym'] in ['NF', 'EZ', 'HT', 'DC'] for mod in score['mods']):
        return
    if ctx.minimum_grade:
        grade = calculate_grade(score)
        if ['X', 'S', 'A', 'B', 'C', 'D'].index(grade) >= ctx.minimum_grade:
            return
    for song in ctx.pairs:
        if ctx.pairs[song]['id'] == score['beatmapset']['id']:
            print(f'Play Matches {song}')
            # check for the correct diff
            if ctx.difficulty_sync and score['beatmap_id'] not in ctx.pairs[song]['diffs']:
                print('The incorrect difficulty was played')
                return
            # check for converts
            if ctx.disallow_converts:
                # Find the diff that was played
                for beatmap in ctx.pairs[song]['beatmaps']:
                    if beatmap['id'] == score['beatmap_id']:
                        if score['ruleset_id'] != 0 and beatmap['mode'] == 'osu':
                            print('Your settings do not allow converts')
                            return
            if song == "Victory":
                if count_item(ctx, 726999999) >= ctx.preformance_points_needed:
                    asyncio.create_task(ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
                    return
                print("You don't have enough performance points")
                return
            if not count_item(ctx, 727000000 + list(ctx.pairs.keys()).index(song)):
                print("You don't have this song unlocked")
                return
            locations = []
            for i in range(2):
                location_id = 727000000 + (2 * list(ctx.pairs.keys()).index(song)) + i
                if location_id in ctx.missing_locations:
                    if location_id in ctx.missing_locations:
                        locations.append(int(location_id))
            if locations:
                message = [{"cmd": 'LocationChecks', "locations": locations}]
                task = asyncio.create_task(ctx.send_msgs(message))
                if ctx.auto_download:
                    asyncio.create_task(download_next_beatmapset_silent(ctx, task))


async def game_watcher(ctx: APosuContext):
    count = 0
    while not ctx.exit_event.is_set():
        if count >= 30:
            for mode in ctx.auto_modes:
                await auto_get_last_scores(ctx, mode)
                await asyncio.sleep(1)
            count = 0
        count += 1
        await asyncio.sleep(0.1)


def main():
    async def _main(args):
        ctx = APosuContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="osu!ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="osu! Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(_main(args))
    colorama.deinit()


if __name__ == '__main__':
    main()