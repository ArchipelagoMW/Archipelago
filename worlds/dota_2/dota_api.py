import asyncio
import json
import logging

import requests
import time

from dataclasses import dataclass, field
@dataclass
class DotaMatchData:
    match_id: int
    hero_id: int
    kills: int
    deaths: int
    assists: int
    purchase: list[str]
    last_hits: int
    denies: int
    win: int
    dewards: int
    rosh: int
    # Global challenges and quests (see challenges.py)
    first_blood: bool = False
    courier_kills: int = 0
    runes: dict = field(default_factory=dict)
    buybacks: int = 0
    aegis: bool = False
    position: int = 0
    duration: int = 0
    all_players_stayed: bool = False
    team_roshan_kills: int = 0
    camps_stacked: int = 0
    wards_placed: int = 0
    building_damage: int = 0
    healing: int = 0
    physical_damage: int = 0
    magical_damage: int = 0
    physical_hit: int = 0
    magical_hit: int = 0


api_logger = logging.getLogger("Client")

class OpenDotaLocal:
    BASE_URL = "https://api.opendota.com/api"

    def __init__(self):
        self.session = requests.Session()

    def get(self, endpoint, params=None, retries=3):
        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=(5, 20)  # 5 sec connection, 15 sec read
                )

                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                api_logger.warning(
                    f"OpenDota request timed out "
                    f"(attempt {attempt + 1}/{retries}): {url}"
                )

                if attempt < retries - 1:
                    time.sleep(2)

            except requests.exceptions.RequestException as e:
                api_logger.warning(
                    f"OpenDota request failed "
                    f"(attempt {attempt + 1}/{retries}): {e}"
                )

                if attempt < retries - 1:
                    time.sleep(2)

        api_logger.error(f"OpenDota request failed after {retries} attempts: {url}")
        
        return None

    def post(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.post(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    def get_player_matches(
        self,
        player_id: int,
        request_parse: bool = False,
        days: int = 2
    ):
        """Matches played by a player."""

        endpoint = f"/players/{player_id}/recentMatches"

        matches = self.get(
            endpoint,
            params={"date": days, "force": True}
        )
        if matches is None:
            return None
    
        if request_parse:
            for match in matches:
                match_id = match["match_id"]

                version = match.get("version")

                if version is None or version < 20:
                    json_data = self.request_parse(match_id)

                    api_logger.info(f"Match ID: {match_id}")
                    api_logger.info(
                        f"Job ID: {json_data['job']['jobId']}"
                    )

        return matches

    def request_parse(self, match_id: int | str):
        """Submit a new parse request."""

        api_logger.info(
            f"Requesting parse for match {match_id}"
        )

        endpoint = f"/request/{match_id}"

        return self.post(endpoint)

    def request_status(self, job_id: int | str):
        """Get parse request state."""

        endpoint = f"/request/{job_id}"

        return self.get(endpoint)

    def get_match(self, match_id: int | str):
        """Get match data."""

        endpoint = f"/matches/{match_id}"

        return self.get(endpoint)

    
#OPEN_DOTA = opendota.OpenDota()
OPEN_DOTA = OpenDotaLocal()



def get_most_recent_match_id(steamID):
    #print(f"DEBUG: awaiting getting player matches")
    matches = OPEN_DOTA.get_player_matches(steamID)
    if not matches:
        api_logger.warning("Could not retrieve player matches from OpenDota.")
        return None
    #print(f"DEBUG: {matches[0]['match_id']}")
    return matches[0]['match_id']

async def request_match_parse(steamID):
    match_id = get_most_recent_match_id(steamID)

    if match_id is None:
        return None
    result = OPEN_DOTA.request_parse(match_id)

    job_id = result['job']["jobId"]
    #print(f'{job_id}')
    #print(f"DEBUG: parse loop")
    while True:
        status = OPEN_DOTA.request_status(job_id)
        #print(f"DEBUG: status = {status}")
        if status == None:
            break

        await asyncio.sleep(10)

    return OPEN_DOTA.get_match(match_id)

def get_my_player(players, steamID) -> dict:
    #print(f"DEBUG: getting player")
    for player in players:
        if player['account_id'] == steamID:
            return player

    raise ValueError("Player not found in match")

async def parse_most_recent_match_data(steamID):
    #print(f"DEBUG: Steam ID = {steamID}")
    match = await request_match_parse(steamID)
    match_id = match['match_id']
    #print(f"{match_id}")
    players = match['players']
    my_player = get_my_player(players, steamID)
    api_logger.info(my_player["hero_id"])
    #print(f"{my_player['hero_id']}")
    return DotaMatchData(
        match_id = match_id,
        hero_id = my_player['hero_id'],
        kills = my_player['kills'],
        deaths = my_player['deaths'],
        assists = my_player['assists'],
        purchase = list(my_player.get("purchase", {}).keys()),
        last_hits = my_player['last_hits'],
        denies = my_player['denies'],
        win = my_player['win'],
        dewards = my_player['observer_kills'] + my_player['sentry_kills'],
        rosh = my_player['roshan_kills'],
        **challenge_data(match, my_player),
    )

def challenge_data(match, me) -> dict:
    """Fields of DotaMatchData used by the global challenges and quests."""
    objectives = match.get('objectives') or []
    my_team = 2 if me['player_slot'] < 128 else 3  # objectives use 2 for Radiant, 3 for Dire
    players = match.get('players') or []
    return dict(
        first_blood = bool(me.get('firstblood_claimed')),
        courier_kills = me.get('courier_kills') or 0,
        runes = {str(k): v for k, v in (me.get('runes') or {}).items()},
        buybacks = me.get('buyback_count') or len(me.get('buyback_log') or []),
        aegis = any(o.get('type') == 'CHAT_MESSAGE_AEGIS' and o.get('player_slot') == me['player_slot'] for o in objectives),
        position = me.get('position_est') or 0,
        duration = match.get('duration') or 0,
        all_players_stayed = match.get('human_players') == 10 and len(players) == 10
            and all((p.get('leaver_status') or 0) == 0 for p in players),
        team_roshan_kills = sum(1 for o in objectives if o.get('type') == 'CHAT_MESSAGE_ROSHAN_KILL' and o.get('team') == my_team),
        camps_stacked = me.get('camps_stacked') or 0,
        wards_placed = (me.get('obs_placed') or 0) + (me.get('sen_placed') or 0),
        building_damage = me.get('tower_damage') or 0,
        healing = me.get('hero_healing') or 0,
        **damage_by_type(me),
    )


_ABILITY_DAMAGE_TYPES: dict | None = None

def ability_damage_types() -> dict:
    """Damage type of each ability (Magical, Physical, Pure), from OpenDota's constants."""
    global _ABILITY_DAMAGE_TYPES
    if _ABILITY_DAMAGE_TYPES is None:
        from importlib import resources
        with resources.files(__package__).joinpath("data/abilityDamageTypes.json").open("r", encoding="utf-8") as f:
            _ABILITY_DAMAGE_TYPES = json.load(f)["ability_damage_types"]
    return _ABILITY_DAMAGE_TYPES

def damage_by_type(me) -> dict:
    """Physical and magical damage to heroes, and the biggest hit of each type we can be sure of.
    Auto-attacks (inflictor "null") are physical; pure damage and items count as neither.
    OpenDota keeps only the match's single biggest hit, so a type's biggest hit is that one when it has this type,
    or else the best average hit of a source of this type (at least one hit was that big)."""
    types = ability_damage_types()
    kind = lambda source: "Physical" if source in (None, "null") else types.get(source)
    inflictors, hits = me.get('damage_inflictor') or {}, me.get('hero_hits') or {}
    totals = {"Physical": 0, "Magical": 0}
    best = {"Physical": 0, "Magical": 0}
    for source, damage in inflictors.items():
        t = kind(source)
        if t in totals:
            totals[t] += damage
            if hits.get(source):
                best[t] = max(best[t], damage // hits[source])
    biggest = me.get('max_hero_hit') or {}
    t = kind(biggest.get('inflictor'))
    if t in best:
        best[t] = max(best[t], biggest.get('value') or 0)
    return dict(physical_damage=totals["Physical"], magical_damage=totals["Magical"],
                physical_hit=best["Physical"], magical_hit=best["Magical"])



