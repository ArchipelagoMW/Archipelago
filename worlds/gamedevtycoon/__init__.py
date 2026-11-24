from collections.abc import Callable
from typing import Any

from BaseClasses import CollectionState, ItemClassification, LocationProgressType, Region, Tutorial
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from .Options import GDTOptions
from .Items import GDTItem, ITEM_TABLE, MODDED_ITEM_PREFIX, MODDED_LIMITS
from .Locations import GDTLocation, LOCATION_TABLE, CONSOLE_LOCATIONS, MODDED_LOCATIONS

# Casual is left out on purpose: the game only offers it after the "Casual games" research.
STARTING_GENRE_CHOICES = ["Action", "Adventure", "RPG", "Simulation", "Strategy"]
ALL_TOPICS = [
    "Sports",
    "Military",
    "Medieval",
    "Space",
    "Racing",
    "Fantasy",
    "Pirate",
    "Sci-Fi",
    "Airplane",
    "Dungeon",
    "Martial Arts",
    "History",
    "Horror",
    "Business",
    "Transport",
    "Comedy",
    "Ninja",
    "Romance",
    "Movies",
    "Spy",
    "Detective",
    "Cyberpunk",
    "UFO",
    "Hospital",
    "Evolution",
    "Time Travel",
    "Life",
    "Virtual Pet",
    "Vocabulary",
    "Hunting",
    "Law",
    "Game Dev",
    "City",
    "School",
    "Fashion",
    "Zombies",
    "Hacking",
    "Government",
    "Prison",
    "Surgery",
    "Rhythm",
    "Superheroes",
    "Post Apocalyptic",
    "Alternate History",
    "Vampire",
    "Werewolf",
    "Aliens",
    "Wild West",
    "Cooking",
    "Farming",
    "Crime",
    "Disasters",
    "Assassin",
    "Thief",
    "Colonization",
    "Construction",
    "Mythology",
    "Abstract",
    "Mad Science",
    "Extreme Sports",
    "Dystopian",
    "Expedition",
    "Technology",
    "Mystery",
    "Music",
    "Dance",
]
GREAT_COMBOS = [
    ("Fantasy", "RPG"),
    ("Sci-Fi", "Strategy"),
    ("Zombies", "Action"),
    ("Cyberpunk", "RPG"),
    ("Space", "Simulation"),
    ("Medieval", "RPG"),
    ("Time Travel", "Adventure"),
    ("Dungeon", "RPG"),
    ("Pirate", "Adventure"),
    ("Ninja", "Action"),
    ("Aliens", "Action"),
    ("Post Apocalyptic", "RPG"),
    ("Superheroes", "Action"),
    ("Sports", "Action"),
    ("Racing", "Simulation"),
    ("Military", "Strategy"),
    ("Hacking", "Simulation"),
    ("Game Dev", "Simulation"),
    ("History", "Strategy"),
    ("Horror", "Action"),
    ("Detective", "Adventure"),
    ("Martial Arts", "Action"),
    ("Transport", "Simulation"),
    ("Evolution", "Strategy"),
]

FILLERS = [
    "Investor Cash Grant (+$250K)",
    "Research Bundle (+25 RP)",
    "Hype Campaign (+50 Hype)",
    "Staff Design Training (+100 Design)",
    "Staff Tech Workshop (+100 Tech)",
    "Staff Speed Bootcamp (+100 Speed)",
    "Staff Research Seminar (+100 Research)",
]
PROGRESSIVE = {"Progressive Office Upgrade": 3, "Progressive Staff License": 6}

# Office tiers in the game: 1 garage, 2 small office, 3 big office, 4 studio with labs.
# Each Progressive Office Upgrade lets the "move office" offer appear for the next tier.
L4_KEYS = [
    "$250M",
    "$500M",
    "$1B",
    "5,000,000",
    "30 Games",
    "Feature #2",
    "Feature #30",
    "Research Game Size: AAA",
    "Research Expansion Packs",
    "R&D: ",
    "Achievement: Professional",
    "Achievement: Legend",
    "Achievement: Diamond",
    "Achievement: 1M Engine",
    "Achievement: Detective",
    "Achievement: Game Dev Tycoon",
    "Achievement: Perfect Game",
    "Achievement: Turn it up to 11",
    "Achievement: Welcome Chief",
    "Achievement: The sky is not the limit.",
    "Achievement: Painting with nature.",
    "Achievement: Eat Cake",
    "Achievement: Famous",
    "Story Event: Red Barrels",
]
L3_KEYS = [
    "$25M",
    "$50M",
    "$100M",
    "500,000",
    "1,000,000",
    "20 Games",
    "Feature #16",
    "Feature #17",
    "Feature #18",
    "Feature #19",
    "Research Game Size: Large",
    "Research Multi-Platform",
    "Achievement: Platinum",
    "Achievement: 500K Engine",
    "Achievement: Best ride to work ever",
    "Achievement: Welcome to your hospital",
    "Achievement: Diversity",
    "Achievement: Versatile",
    "Story Event: Solar Power Initiative",
]
L2_KEYS = [
    "$2.5M",
    "$5M",
    "$10M",
    "50,000",
    "100,000",
    "250,000",
    "10 Games",
    "15 Games",
    "Research Engine Feature",
    "Research Game Size: Medium",
    "Research Marketing",
    "Research Multi-Genre",
    "Hire Employee",
    "Achievement: Gold",
    "Achievement: 100K Engine",
    "Achievement: Cult Status",
    "Achievement: Bluehair reporting for space duty",
    "Achievement: Welcome to Mars",
    "Story Event: Coding Contest",
    "Story Event: Women in Tech",
    "Story Event: Security Upgrade",
    "Story Event: Fan Game Infringement",
    "Story Event: Patent Troll Lawsuit",
    "Story Event: Magazine Interview",
]

# Items for a console this version of the game doesn't have: they would do nothing, so they stay out of the pool.
# The game gives these three to every custom engine, so as items they would do nothing.
UNUSED_ITEMS = {"Platform: mPad", "Retire Platform: mPad", "2D Graphics V2", "Linear Story", "Savegame"}

# (Story events used to be missable; now each has an "Event: X" item that makes it happen, so none are.)
# Needs an MMO on sale, which the game may never offer in a run.
MISSABLE: set = {"Research Expansion Packs"}
# Own Convention needs 1M fans, or opens for everyone from this year on.
OWN_CONVENTION_YEAR = 23

# Locations that need hired staff: (licenses needed, office upgrades needed)
STAFF_RULES = {
    "Hire Employee #1": (1, 1),
    "Hire Employee #2": (2, 1),
    "Hire Employee #3": (3, 1),
    "Hire Employee #4": (4, 1),
    "Hire Employee #5": (5, 3),
    "Hire Employee #6": (6, 3),
    "Research Game Size: Medium": (1, 1),
    "Research Game Size: Large": (4, 2),
    "Story Event: Security Upgrade": (1, 1),
    "Story Event: Women in Tech": (1, 1),
    "Story Event: Fan Game Infringement": (1, 1),
    "Story Event: Coding Contest": (4, 1),
    "Story Event: Air Conditioning": (3, 1),
}


def _tier(loc_name: str) -> int:
    for tier, keys in ((3, L4_KEYS), (2, L3_KEYS), (1, L2_KEYS)):
        if any(k in loc_name for k in keys):
            return tier
    return 0


class GDTWeb(WebWorld):
    theme = "ocean"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "Setup guide for Game Dev Tycoon in Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["ioicaleb"],
        )
    ]


class GDTWorld(World):
    """Game Dev Tycoon: Build a video game studio from a 1980s garage with randomized topics, genres, and platforms."""

    game = "Game Dev Tycoon"
    web = GDTWeb()
    options_dataclass = GDTOptions
    options: GDTOptions
    item_name_to_id: dict[str, int] = ITEM_TABLE
    location_name_to_id: dict[str, int] = LOCATION_TABLE

    def generate_early(self) -> None:
        # modded content: {kind: [names]} from the in-game export, checked against the slot limits
        self.modded: dict[str, list[str]] = {}
        for kind, names in dict(self.options.modded_content.value).items():
            if names is None:
                continue
            if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
                raise OptionError(f"Game Dev Tycoon: modded_content {kind} must be a list of names")
            if len(names) > MODDED_LIMITS[kind]:
                raise OptionError(
                    f"Game Dev Tycoon: modded_content has {len(names)} {kind}; the limit is {MODDED_LIMITS[kind]}"
                )
            self.modded[kind] = list(names)
        if self.options.friendly_start.value:
            t1, g1 = self.random.choice(GREAT_COMBOS)
            t2 = self.random.choice([t for t in ALL_TOPICS if t != t1])
            g2 = self.random.choice([g for g in STARTING_GENRE_CHOICES if g != g1])
            self.starting_topics = sorted([t1, t2])
            self.starting_genres = sorted([g1, g2])
        else:
            self.starting_topics = sorted(self.random.sample(ALL_TOPICS, 2))
            self.starting_genres = sorted(self.random.sample(STARTING_GENRE_CHOICES, 2))

    def create_item(self, name: str) -> GDTItem:
        if (
            name.startswith(("Genre: ", "Platform: ", "Modded Platform ", "Modded Genre ", "Modded Event ", "Event: "))
            or name in PROGRESSIVE
            or name == "Progressive Game Size"
        ):
            classification = ItemClassification.progression
        elif name.startswith(("Topic: ", "Modded Topic ", "Modded Feature ", "Business: ")) or (
            20200 <= ITEM_TABLE[name] < 20300
        ):
            classification = ItemClassification.useful
        elif name.startswith("Retire Platform: "):
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler
        return GDTItem(name, classification, ITEM_TABLE[name], self.player)

    def _tier_rule(self, tier: int) -> Callable[[CollectionState], bool]:
        sizes = tier if self.options.shuffle_game_sizes else 0  # bigger offices are expected to make bigger games
        return lambda state: (
            state.has("Progressive Office Upgrade", self.player, tier)
            and state.has("Progressive Game Size", self.player, sizes)
        )

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        tiers = [
            Region(n, self.player, self.multiworld)
            for n in (
                "Garage (Office Tier 1)",
                "Small Office (Office Tier 2)",
                "Big Office (Office Tier 3)",
                "Studio (Office Tier 4)",
            )
        ]
        self.multiworld.regions.extend([menu, *tiers])

        for loc_name, loc_id in LOCATION_TABLE.items():
            modded = MODDED_LOCATIONS.get(loc_name)
            if modded and modded[1] >= len(self.modded.get(modded[0], [])):
                continue  # slot not used by this player's mods
            region = tiers[_tier(loc_name)]
            loc = GDTLocation(self.player, loc_name, loc_id, region)
            if loc_name in MISSABLE or (
                loc_name == "R&D: Own Convention" and self.options.retirement_year.value < OWN_CONVENTION_YEAR
            ):
                loc.progress_type = LocationProgressType.EXCLUDED
            if loc_name in STAFF_RULES:
                licenses, offices = STAFF_RULES[loc_name]
                loc.access_rule = lambda s, l=licenses, o=offices: (
                    s.has("Progressive Staff License", self.player, l)
                    and s.has("Progressive Office Upgrade", self.player, o)
                )
            elif loc_name in CONSOLE_LOCATIONS:
                # release a game on the console (or its fan build): needs that console's Platform item
                platform = "Platform: " + loc_name[len("Release a Game on ") :]
                loc.access_rule = lambda s, p=platform: s.has(p, self.player)
            elif modded and modded[0] in ("platforms", "genres", "events"):
                # release on the modded platform / in the modded genre, or the event happening: needs its item
                item = f"{MODDED_ITEM_PREFIX[modded[0]]} {modded[1] + 1}"
                loc.access_rule = lambda s, i=item: s.has(i, self.player)
            elif loc_name == "Achievement: Diversity":
                # a hit game in every genre: needs all genres you didn't start with
                genres = [f"Genre: {g}" for g in STARTING_GENRE_CHOICES + ["Casual"] if g not in self.starting_genres]
                loc.access_rule = lambda s, g=genres: s.has_all(g, self.player)
            if loc_name.startswith("Story Event: "):
                # the event's item makes it happen (on top of any staff/office rule above)
                event_item, rule = "Event: " + loc_name[len("Story Event: ") :], loc.access_rule
                loc.access_rule = lambda s, e=event_item, r=rule: s.has(e, self.player) and r(s)
            region.locations.append(loc)

        menu.connect(tiers[0])
        for i in range(1, 4):
            tiers[i - 1].connect(tiers[i], rule=self._tier_rule(i))

        # The goal is always to retire. Just surviving needs nothing from the multiworld; a millionaire
        # ($10M / 100K fans) fits in the small office; a tycoon ($100M / 1M fans) needs the full studio.
        goal_region = tiers[{0: 0, 1: 1, 2: 3}[self.options.success_level.value]]
        retire = GDTLocation(self.player, "Retire", None, goal_region)
        retire.place_locked_item(GDTItem("Victory", ItemClassification.progression, None, self.player))
        goal_region.locations.append(retire)

    def create_items(self) -> None:
        pool: list[GDTItem] = []
        for name, count in PROGRESSIVE.items():
            pool += [self.create_item(name) for _ in range(count)]
        excluded = {f"Genre: {g}" for g in self.starting_genres} | {f"Topic: {t}" for t in self.starting_topics}
        unused_modded = {
            f"{prefix} {i + 1}"
            for kind, prefix in MODDED_ITEM_PREFIX.items()
            for i in range(len(self.modded.get(kind, [])), MODDED_LIMITS[kind])
        }
        if self.options.shuffle_game_sizes:
            pool += [self.create_item("Progressive Game Size") for _ in range(3)]
        for name in ITEM_TABLE:
            if (
                name not in PROGRESSIVE
                and name != "Progressive Game Size"
                and name not in FILLERS
                and name not in excluded
                and name not in UNUSED_ITEMS
                and name not in unused_modded
            ):
                pool.append(self.create_item(name))
        total = len(self.multiworld.get_unfilled_locations(self.player))
        if len(pool) > total:
            raise OptionError(f"Game Dev Tycoon: {len(pool)} items for {total} locations")
        i = 0
        while len(pool) < total:
            pool.append(self.create_item(FILLERS[i % len(FILLERS)]))
            i += 1
        self.multiworld.itempool.extend(pool)

    def get_filler_item_name(self) -> str:
        return self.random.choice(FILLERS)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda s: s.has("Victory", self.player)

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "retirement_year": int(self.options.retirement_year.value),
            "success_level": int(self.options.success_level.value),
            "starting_topics": ",".join(self.starting_topics),
            "starting_genres": ",".join(self.starting_genres),
            "shuffle_game_sizes": bool(self.options.shuffle_game_sizes.value),
            "modded_content": self.modded,  # slot N of each kind = the Nth name here
        }
