from .patches import enemies, bingo
from .locations.items import *
from .entranceInfo import ENTRANCE_INFO
from . import logic
from .utils import Error


MULTI_CHEST_OPTIONS = [MAGIC_POWDER, BOMB, MEDICINE, RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL, GEL, ARROWS_10, SINGLE_ARROW]
MULTI_CHEST_WEIGHTS = [20,           20,   20,       50,        50,        20,         10,         5,          5,        20,  10,        10]

# List of all the possible locations where we can place our starting house
start_locations = [
    "phone_d8",
    "rooster_house",
    "writes_phone",
    "castle_phone",
    "photo_house",
    "start_house",
    "prairie_right_phone",
    "banana_seller",
    "prairie_low_phone",
    "animal_phone",
]


class WorldSetup:
    def __init__(self):
        self.entrance_mapping = {k: f"{k}:inside" for k in ENTRANCE_INFO.keys()}
        self.entrance_mapping.update({f"{k}:inside": k for k in ENTRANCE_INFO.keys()})
        self.boss_mapping = list(range(9))
        self.miniboss_mapping = {
            # Main minibosses
            '0': "ROLLING_BONES", '1': "HINOX", '2': "DODONGO", '3': "CUE_BALL", '4': "GHOMA", '5': "SMASHER", '6': "GRIM_CREEPER", '7': "BLAINO",
            # Color dungeon needs to be special, as always.
            "c1": "AVALAUNCH", "c2": "GIANT_BUZZ_BLOB",
            # Overworld
            "moblin_cave": "MOBLIN_KING",
            "armos_temple": "ARMOS_KNIGHT",
        }
        self.goal = None
        self.bingo_goals = None
        self.multichest = RUPEES_20
        self.map = None  # Randomly generated map data
        self.inside_to_outside = True
        self.keep_two_way = True
        self.one_on_one = True

    def getEntrancePool(self, settings, connectorsOnly=False):
        entrances = []

        if connectorsOnly:
            if settings.entranceshuffle in {"split", "mixed", "wild", "chaos", "insane", "madness"}:
                entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "connector"]
            entrances += [f"{k}:inside" for k in entrances]
            return entrances

        if settings.dungeonshuffle and settings.entranceshuffle == "none":
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "dungeon"]
        if settings.entranceshuffle in {"simple", "split", "mixed", "wild", "chaos", "insane", "madness"}:
            types = {"single"}
            if settings.tradequest:
                types.add("trade")
            if settings.shufflejunk:
                types.update(["dummy", "trade"])
            if settings.shuffleannoying:
                types.add("insanity")
            if settings.shufflewater:
                types.add("water")
            if settings.randomstartlocation:
                types.add("start")
            if settings.dungeonshuffle:
                types.add("dungeon")
            if settings.entranceshuffle in {"mixed", "wild", "chaos", "insane", "madness"}:
                types.add("connector")
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type in types]

        entrances += [f"{k}:inside" for k in entrances]
        return entrances

    def _swapEntrances(self, a, b):
        # Two two two-way entrances to connect disconnecting islands
        assert self.keep_two_way
        temp = self.entrance_mapping[a]
        self.entrance_mapping[a] = self.entrance_mapping[b]
        self.entrance_mapping[b] = temp
        self.entrance_mapping[self.entrance_mapping[a]] = a
        self.entrance_mapping[self.entrance_mapping[b]] = b

    def _injectEntrance(self, source, target):
        # Inject an entrance into a chain of entrances with decoupled mode
        assert not self.keep_two_way
        to_source = None
        for k, v in self.entrance_mapping.items():
            if v == source:
                to_source = k
                break
        assert to_source is not None
        temp = self.entrance_mapping[target]
        self.entrance_mapping[target] = source
        self.entrance_mapping[to_source] = temp

    def _addConnectionTowards(self, sources, rnd, target):
        # When no one-on-one requirement is needed, we can simply disconnect
        # one of the doulble connected entrances.
        entrance_to = {}
        for s in sources:
            if self.entrance_mapping[s] not in entrance_to:
                entrance_to[self.entrance_mapping[s]] = []
            entrance_to[self.entrance_mapping[s]].append(s)
        options = []
        for k, v in entrance_to.items():
            if len(v) > 1:
                options += v
        option = rnd.choice(options)
        self.entrance_mapping[option] = target

    def inaccessibleEntrances(self, settings, entrancePool):
        log = logic.Logic(settings, world_setup=self)
        return [x for x in entrancePool if log.world.entrances[x].location and log.world.entrances[x].location not in log.location_list]

    def _randomizeEntrances(self, rnd, entrancePool):
        unmappedEntrances = list(entrancePool)

        done = set()
        for entrance in [x for x in entrancePool]:
            if entrance in done:
                continue
            while entrance not in done:
                pick_idx = rnd.randrange(len(unmappedEntrances))
                pick = unmappedEntrances[pick_idx]
                if pick == entrance:
                    if len(unmappedEntrances) < 2:
                        raise Error("Cannot map entrance to itself")
                    continue
                if self.inside_to_outside and entrance.endswith(":inside") == pick.endswith(":inside"):
                    continue
                if self.one_on_one:
                    unmappedEntrances.pop(pick_idx)
                self.entrance_mapping[entrance] = pick
                done.add(entrance)
                if self.keep_two_way:
                    unmappedEntrances.remove(entrance)
                    self.entrance_mapping[pick] = entrance
                    done.add(pick)

    def pickEntrances(self, settings, rnd):
        if settings.overworld in {"random", "dungeonchain", "alttp"}:
            return
        if settings.overworld == "dungeondive":
            self.entrance_mapping = {"d%d" % (n): "d%d:inside" % (n) for n in range(9)}
            self.entrance_mapping.update({"d%d:inside" % (n): "d%d" % (n) for n in range(9)})
        if settings.randomstartlocation and settings.entranceshuffle == "none":
            start_location = start_locations[rnd.randrange(len(start_locations))]
            if start_location != "start_house":
                self.entrance_mapping[start_location] = "start_house:inside"
                self.entrance_mapping["start_house:inside"] = start_location
                self.entrance_mapping["start_house"] = f"{start_location}:inside"
                self.entrance_mapping[f"{start_location}:inside"] = "start_house"

        entrancePool = self.getEntrancePool(settings)
        self._randomizeEntrances(rnd, entrancePool)

        if settings.entranceshuffle == 'split':
            # Shuffle connectors among themselves
            # entrancePool is intentionally overwritten so we're only swapping connectors
            entrancePool = self.getEntrancePool(settings, connectorsOnly=True)
            self._randomizeEntrances(rnd, entrancePool)

        # Make sure all entrances in the pool are accessible
        for _ in range(1000):
            islands = self.inaccessibleEntrances(settings, entrancePool)

            if not islands:
                break

            island = rnd.choice(islands)
            mains = [x for x in entrancePool if x not in islands]
            main = rnd.choice(mains)

            if self.inside_to_outside:
                if island.endswith(":inside") != main.endswith(":inside"):
                    continue

            if not self.one_on_one:
                self._addConnectionTowards(mains, rnd, island)
            elif self.keep_two_way:
                self._swapEntrances(island, main)
            else:
                self._injectEntrance(island, main)

        if self.inaccessibleEntrances(settings, entrancePool):
            raise Error("Failed to make all entrances accessible after a bunch of retries")
        self._checkEntranceRules()

    def _checkEntranceRules(self):
        if self.inside_to_outside:
            for k, v in self.entrance_mapping.items():
                if k.endswith(":inside"):
                    assert not v.endswith(":inside"), f"inside-to-outside rule violated: {k}->{v}"
                else:
                    assert v.endswith(":inside"), f"inside-to-outside rule violated: {k}->{v}"
        if self.keep_two_way:
            for k, v in self.entrance_mapping.items():
                assert self.entrance_mapping[v] == k, f"keep-two-way rule violated: {k}->{v}"
        if self.one_on_one:
            found = set()
            for k, v in self.entrance_mapping.items():
                assert v not in found, f"one-on-one rule violated: {k}->{v}"
                found.add(v)

    def randomize(self, settings, rnd, ap_options):
        if settings.boss != "default":
            values = list(range(9))
            if settings.heartcontainers:
                # Color dungeon boss does not drop a heart container so we cannot shuffle him when we
                # have heart container shuffling
                values.remove(8)
            self.boss_mapping = []
            for n in range(8 if settings.heartcontainers else 9):
                value = rnd.choice(values)
                self.boss_mapping.append(value)
                if value in (3, 6) or settings.boss == "shuffle":
                    values.remove(value)
            if settings.heartcontainers:
                self.boss_mapping += [8]
        if settings.miniboss != "default":
            values = [name for name in self.miniboss_mapping.values()]
            for key in self.miniboss_mapping.keys():
                self.miniboss_mapping[key] = rnd.choice(values)
                if settings.miniboss == 'shuffle':
                    values.remove(self.miniboss_mapping[key])

        if settings.goal == 'random':
            self.goal = rnd.randint(-1, 8)
        elif settings.goal == 'open':
            self.goal = -1
        elif settings.goal in {"seashells", "bingo", "bingo-full"}:
            self.goal = settings.goal
        elif settings.goal == "specific":
            instrument_count = max(1, ap_options.instrument_count.value)
            instruments = [c for c in "12345678"]
            rnd.shuffle(instruments)
            self.goal = "=" + "".join(instruments[:instrument_count])
        elif "-" in settings.goal:
            a, b = settings.goal.split("-")
            if a == "open":
                a = -1
            self.goal = rnd.randint(int(a), int(b))
        else:
            self.goal = int(settings.goal)
        if self.goal in {"bingo", "bingo-full"}:
            self.bingo_goals = bingo.randomizeGoals(rnd, settings)

        self.multichest = rnd.choices(MULTI_CHEST_OPTIONS, MULTI_CHEST_WEIGHTS)[0]

        self.inside_to_outside = settings.entranceshuffle not in {"wild", "insane", "madness"}
        self.keep_two_way = settings.entranceshuffle not in {"chaos", "insane", "madness"}
        self.one_on_one = settings.entranceshuffle not in {"madness"}
        self.pickEntrances(settings, rnd)

    def loadFromRom(self, rom):
        import patches.overworld
        if patches.overworld.isNormalOverworld(rom):
            import patches.entrances
            self.entrance_mapping = patches.entrances.readEntrances(rom)
        else:
            self.entrance_mapping = {"d%d" % (n): "d%d:inside" % (n) for n in range(9)}
            self.entrance_mapping.update({"d%d:inside" % (n): "d%d" % (n) for n in range(9)})
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
        self.goal = 8 # Better then nothing
