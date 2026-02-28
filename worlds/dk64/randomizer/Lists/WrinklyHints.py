"""Hint location data for Wrinkly hints."""

from __future__ import annotations

from math import sqrt
from typing import TYPE_CHECKING, Any, List, Union, Set

from randomizer.Enums.HintType import HintType
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import WinConditionComplex
from randomizer.Enums.Types import Types

from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.WrinklyKong import WrinklyLocation
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import PreGivenLocations, TrainingBarrelLocations
from randomizer.Lists.MapsAndExits import GetMapId
from randomizer.Lists.PathHintTree import BuildPathHintTree


class HintLocation:
    """Hint object for Wrinkly hint data locations."""

    def __init__(
        self,
        name: str,
        kong: Kongs,
        location: WrinklyLocation,
        hint: str,
        level: Levels,
        banned_keywords: List[Union[Any, str]] = [],
    ) -> None:
        """Create wrinkly hint object.

        Args:
            name (str): Location/String name of wrinkly.
            kong (Kongs): What kong the hint is for.
            location (WrinklyLocation): What lobby the hint is in.
            hint (str): Hint to be written to ROM
        """
        self.name = name
        self.kong = kong
        self.location = location
        self.hint = hint
        self.short_hint = None
        self.hint_type = -1
        self.banned_keywords = banned_keywords.copy()
        self.level = level
        self.related_location = None
        self.related_location_name = None
        self.related_location_item_name = None
        self.related_hint_region_id = None
        self.related_flag = None
        self.is_last_woth_hint = False


class MoveInfo:
    """Move Info for Wrinkly hint text."""

    def __init__(self, *, name="", kong="", move_type="", move_level=0, important=False) -> None:
        """Create move info object."""
        self.name = name
        self.kong = kong
        move_types = ["special", "slam", "gun", "ammo_belt", "instrument"]
        encoded_move_type = move_types.index(move_type)
        self.move_type = encoded_move_type
        self.move_level = move_level
        self.important = important
        ref_kong = kong
        if ref_kong == Kongs.any:
            ref_kong = Kongs.donkey
        self.item_key = {"move_type": move_type, "move_lvl": move_level - 1, "move_kong": ref_kong}


def getDefaultHintList() -> List[HintLocation]:
    """Return the default set of hints."""
    return [
        HintLocation(
            "First Time Talk",
            Kongs.any,
            WrinklyLocation.ftt,
            "WELCOME TO THE DONKEY KONG 64 RANDOMIZER. MADE BY 2DOS, BALLAAM, KILLKLLI, SHADOWSHINE, CFOX, BISMUTH & ZNERNICUS",
            Levels.DKIsles,
        ),
        HintLocation("Japes DK", Kongs.donkey, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Diddy", Kongs.diddy, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Lanky", Kongs.lanky, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Tiny", Kongs.tiny, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Chunky", Kongs.chunky, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Aztec DK", Kongs.donkey, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation("Aztec Diddy", Kongs.diddy, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation("Aztec Lanky", Kongs.lanky, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation("Aztec Tiny", Kongs.tiny, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation(
            "Aztec Chunky",
            Kongs.chunky,
            WrinklyLocation.aztec,
            "",
            Levels.AngryAztec,
            banned_keywords=["Hunky Chunky", "Feather Bow"],
        ),
        HintLocation("Factory DK", Kongs.donkey, WrinklyLocation.factory, "", Levels.FranticFactory),
        HintLocation(
            "Factory Diddy",
            Kongs.diddy,
            WrinklyLocation.factory,
            "",
            Levels.FranticFactory,
            banned_keywords=["Gorilla Grab"],
        ),
        HintLocation(
            "Factory Lanky",
            Kongs.lanky,
            WrinklyLocation.factory,
            "",
            Levels.FranticFactory,
            banned_keywords=["Gorilla Grab"],
        ),
        HintLocation("Factory Tiny", Kongs.tiny, WrinklyLocation.factory, "", Levels.FranticFactory, banned_keywords=["Gorilla Grab"]),
        HintLocation("Factory Chunky", Kongs.chunky, WrinklyLocation.factory, "", Levels.FranticFactory),
        HintLocation("Galleon DK", Kongs.donkey, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Diddy", Kongs.diddy, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Lanky", Kongs.lanky, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Tiny", Kongs.tiny, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Chunky", Kongs.chunky, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Fungi DK", Kongs.donkey, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Diddy", Kongs.diddy, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Lanky", Kongs.lanky, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Tiny", Kongs.tiny, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Chunky", Kongs.chunky, WrinklyLocation.fungi, "", Levels.FungiForest),
        HintLocation("Caves DK", Kongs.donkey, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation(
            "Caves Diddy",
            Kongs.diddy,
            WrinklyLocation.caves,
            "",
            Levels.CrystalCaves,
            banned_keywords=["Primate Punch", "Rocketbarrel Boost"],
        ),
        HintLocation("Caves Lanky", Kongs.lanky, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation("Caves Tiny", Kongs.tiny, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation("Caves Chunky", Kongs.chunky, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation("Castle DK", Kongs.donkey, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Diddy", Kongs.diddy, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Lanky", Kongs.lanky, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Tiny", Kongs.tiny, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Chunky", Kongs.chunky, WrinklyLocation.castle, "", Levels.CreepyCastle),
    ]


class HintSet:
    """A set of hints and all pertinent information about them."""

    def __init__(self, hint_cap=35):
        """Create a hint set object."""
        self.hints: List[HintLocation] = getDefaultHintList()
        self.hint_cap = hint_cap
        self.expectedDistribution = {}
        self.currentDistribution = {}
        self.wothLocationUnhintedScores = {}

    def ClearHintMessages(self) -> None:
        """Reset the hint message for all hints."""
        self.hints = getDefaultHintList()

    def getRandomHintLocation(self, random, location_list=None, kongs=None, levels=None, move_name=None) -> HintLocation:
        """Return an unoccupied hint location. The parameters can be used to specify location requirements."""
        valid_unoccupied_hint_locations = [
            hint
            for hint in self.hints
            if hint.hint == ""
            and (location_list is None or hint in location_list)
            and (kongs is None or hint.kong in kongs)
            and (levels is None or hint.level in levels)
            and move_name not in hint.banned_keywords
        ]
        # If it's too specific, we may not be able to find any
        if len(valid_unoccupied_hint_locations) == 0:
            return None
        hint_location = random.choice(valid_unoccupied_hint_locations)
        # Update the reference so we're updating the main list instead of a copy of it
        for hint in self.hints:
            if hint.name == hint_location.name:
                return hint
        return None

    def getHintLocationsForAccessibleHintItems(self, hint_item_ids: Union[Set[Items], List[Items]], include_occupied=False) -> List[Union[HintLocation, Any]]:
        """Given a list of hint item ids, return unoccupied HintLocation objects they correspond to, possibly returning an empty list."""
        accessible_hints = []
        for item_id in hint_item_ids:
            item = ItemList[item_id]
            matching_hint = [hint for hint in self.hints if hint.level == item.level and hint.kong == item.kong][0]  # Should only match one
            accessible_hints.append(matching_hint)
        if include_occupied:
            return accessible_hints
        return [hint for hint in accessible_hints if hint.hint == ""]  # Filter out the occupied ones

    def RemoveFTT(self) -> None:
        """Remove the FTT hint from the hintset."""
        self.hints = [hint for hint in self.hints if hint.name != "First Time Talk"]

    def CalculateHintScores(self, spoiler, multipath_dict_goals):
        """Evaluate the strength of the hints and attempt to distill it into a score."""
        self.wothLocationUnhintedScores = {}
        # This evaluation only matters with multipath hints - if you're not on multipath hints, aint nothin gonna happen
        if self.expectedDistribution[HintType.Multipath] > 0:
            spoiler.unhinted_score = 0
            spoiler.poor_scoring_locations = {}
            hint_tree = BuildPathHintTree(spoiler.woth_paths)
            # Some locations are known quantities and can be pruned from the tree
            del hint_tree[Locations.BananaHoard]
            if spoiler.settings.key_8_helm:
                if Locations.HelmKey in hint_tree:
                    del hint_tree[Locations.HelmKey]
            # Decorate the tree with information from our placed hints
            for hint in self.hints:
                # Hints with direct locations are either Multipath hints, WotH hints, Entrance hints, or Kong hints
                if hint.related_location is not None and hint.related_location in hint_tree.keys() and hint.hint_type != HintType.Joke:  # ...or it's the WotB hint, what a guy
                    if hint.hint_type == HintType.Multipath:
                        hint_tree[hint.related_location].path_hinted = True
                        # Other locations in the same region as a path hint should be noted down as weakly-hinted, as "clear you hinted regions" is common advice
                        location_ids_in_region = GetLocationIdsInHintRegion(spoiler, hint.related_hint_region_id)
                        for loc_id in location_ids_in_region:
                            if loc_id in hint_tree.keys():
                                # This could be either a very weak hint towards these locations or lampshading by more powerful items
                                hint_tree[loc_id].in_region_with_path_hint = True
                    # Anything that isn't a multipath hint here is functionally a WotH hint
                    else:
                        hint_tree[hint.related_location].woth_hinted = True
                elif hint.hint_type == HintType.RegionItemCount:
                    # Region item count (scouring) hints don't tell you how valuable any of the items are, but it gives you something to look into, so it's a weaker hint
                    location_ids_in_region = GetLocationIdsInHintRegion(spoiler, hint.related_hint_region_id)
                    for loc_id in location_ids_in_region:
                        if loc_id in hint_tree.keys():
                            hint_tree[loc_id].region_hinted = True
            for loc in hint_tree.keys():
                if loc in multipath_dict_goals.keys():
                    hint_tree[loc].goals = multipath_dict_goals[loc]
                # I'm pretty sure this can only happen to training moves
                else:
                    hint_tree[loc].goals = []
            # Loop through nodes, front-to-back, earliest items to latest items, applying unhinted_score based on the connections
            for node in hint_tree.values():
                node_location = spoiler.LocationList[node.node_location_id]
                location_item = ItemList[node_location.item]
                # If the item here is a Kong, it both can't be on the path to anything and is already given a required Kong hint
                if location_item.type == Types.Kong:
                    continue
                # A scouring hint to a vial could be good enough to work with, worthy of a slight reduction in unhinted score
                if node.region_hinted and location_item.type not in (Types.Key, Types.Kong):
                    node.score_multiplier *= 0.8
                # Medal locations and Bosses get an automatic x1.5 unhinted multiplier because they are awful to orphan
                if node_location.type in (Types.Medal, Types.HalfMedal, Types.Key):
                    node.score_multiplier *= 1.5
                # Scores get a multplier boost if the location is not in the main map of a level. This is to simulate having to go out of your way to find this unhinted item.
                # This isn't a foolproof metric, but you are generally more likely to peek or check locations in the main map of each level.
                elif node_location.level != Levels.DKIsles and node_location.type != Types.Shop and node.node_location_id != Locations.RarewareCoin:
                    # The exceptions:
                    # 1. No Isles checks get this boost - all Isles checks are relatively accessible compared to a check deeper in a level.
                    # 2. Shops do not get this boost. You're reasonably likely to look at shops, as most of them fall in the main map. This includes Jetpac.
                    # 3. Boss and Medal locations are already getting a *hefty* multiplier and don't need any more.
                    node_map = GetMapId(spoiler.settings, GetRegionIdOfLocation(spoiler, node.node_location_id))
                    if node_map not in (Maps.JungleJapes, Maps.AngryAztec, Maps.FranticFactory, Maps.GloomyGalleon, Maps.FungiForest, Maps.CrystalCaves, Maps.CreepyCastle):
                        node.score_multiplier *= 1.1
                # Shop locations are much easier (or at least predictable) to find and peek their contents
                if node_location.type == Types.Shop:
                    node.score_multiplier *= 0.4
                # Keys are always an endpoint of a path (unless it's DK Rap win con). These items should be the culmination of other hints and therefore highly unlikely to end up unhinted.
                if spoiler.settings.win_condition_item != WinConditionComplex.dk_rap_items and location_item.type == Types.Key:
                    node.score_multiplier *= 0.7
                # Training barrel locations don't matter if they're hinted or not because you start with them
                if node.node_location_id in TrainingBarrelLocations or node.node_location_id in PreGivenLocations:
                    node.score_multiplier *= 0
                # If this location is hinted, bail before giving it a flat score - this makes the location's final score always 0
                if node.path_hinted or node.woth_hinted or node.score_multiplier == 0:
                    continue
                # The baseline unhinted score for a node is inversely proportional to the number of goals this location is on the path to
                # If something is on the path to a lot of goals, it's often found early and usually less disastrous to be missed
                node.unhinted_score += sqrt(1.0 / max(1, len(node.goals)))  # If something is on the path to 0 goals, it's probably a "diving for level 4" situation, and those are quite dicey
                for parent_loc_id in node.parents:
                    parent_node = hint_tree[parent_loc_id]
                    # If this is the only child of this parent and the parent is directly hinted, this is the only location that can resolve that hint.
                    if len(parent_node.children) == 1 and (parent_node.path_hinted or parent_node.woth_hinted):
                        # Halve the unhinted contribution of this node per hinted solo-parent
                        node.score_multiplier *= 0.5
                    # A woth-hinted location with multiple children means it could resolve in many ways, which could possibly leave this item effectively unhinted
                    # If the parents are path hinted, we need to analyze siblings' goals to determine if this location uniquely solves some portion of the parent's path
                    elif len(parent_node.children) > 1 and parent_node.path_hinted:
                        # Compile a list of all goals that the siblings are on the path to - this is always a subset of the parent's goals!
                        sibling_nodes = [hint_tree[loc_id] for loc_id in parent_node.children if loc_id != node.node_location_id and loc_id in hint_tree.keys()]
                        sibling_goals = set([goal for node in sibling_nodes for goal in node.goals])
                        # If this node has *any* goals that are unique to this location, then this is the only location that can resolve that portion of the parent's path hint.
                        if any(set(node.goals).difference(sibling_goals)):
                            # Because of that, it makes this less unhinted
                            node.score_multiplier *= 0.6
                        # Identify any particularly problematic siblings more directly
                        for child_loc_id in parent_node.children:
                            if child_loc_id != node.node_location_id and child_loc_id in hint_tree.keys():
                                child_node = hint_tree[child_loc_id]
                                # If a parent is path hinted and this sibling could resolve this node's goals, one of the two would be effectively unhinted
                                if set(node.goals).issubset(set(child_node.goals)):
                                    # Split the difference - the current node being evaluated gets half the value
                                    node.unhinted_score += 0.5
                                    # If the goals *exactly* match, then the current node could mask their sibling, even if the sibling is hinted!
                                    if node.goals == child_node.goals:
                                        child_node.unhinted_score += 0.5
                                    # Note that if both are unhinted you'll double the score, which is appropriate for two unhinted items that could resolve the same path hint

            # Now that we've completed tree decoration, we can assess the damage - we have to do this at the end because sibling calculations can affect nodes that were previously calculated
            for node in hint_tree.values():
                node_score = node.unhinted_score * node.score_multiplier
                spoiler.unhinted_score += node_score
                self.wothLocationUnhintedScores[node.node_location_id] = node_score


def UpdateHint(WrinklyHint: HintLocation, message: str):
    """Update the wrinkly hint with the new string.

    Args:
        WrinklyHint (Hint): Wrinkly hint object.
        message (str): Hint message to write.
    """
    # Seek to the wrinkly data
    if len(message) <= 914:
        # We're safely below the character limit
        WrinklyHint.hint = message
        return True
    else:
        raise Exception("Hint message is longer than allowed.")
    return False


def GetRegionIdOfLocation(spoiler, location_id: Locations) -> Regions:
    """Given the id of a Location, return the Region it belongs to."""
    location = spoiler.LocationList[location_id]
    # Shop locations are tied to the level, not the shop regions
    if location.type == Types.Shop:
        for region_id in [id for id, reg in spoiler.RegionList.items() if reg.level == Levels.Shops]:
            if location_id in [location_logic.id for location_logic in spoiler.RegionList[region_id].locations if not location_logic.isAuxiliaryLocation]:
                return region_id
    for region_id in Regions:
        region = spoiler.RegionList[region_id]
        if region.level == location.level or location.type == Types.Hint:
            if location_id in [location_logic.id for location_logic in region.locations if not location_logic.isAuxiliaryLocation]:
                return region_id
    raise Exception(f"Unable to find Region for Location {location_id.name}")  # This should never trigger!


def GetLocationIdsInHintRegion(spoiler, hint_region_id: HintRegion) -> List[Locations]:
    """Given the id of a hint region, return a list of Location ids that belong to it."""
    location_ids_in_region = []
    for region_id in Regions:
        region = spoiler.RegionList[region_id]
        if region.hint_name == hint_region_id:
            location_ids_in_region.extend([location_logic.id for location_logic in region.locations if not location_logic.isAuxiliaryLocation])
    return location_ids_in_region


joke_hint_list = [
    "Did you know - Donkey Kong officially features in Donkey Kong 64.",
    "Fungi Forest was originally intended to be in the other N64 Rareware title, Banjo Kazooie.",
    "Holding up-left when trapped inside of a trap bubble will break you out of it without spinning your stick.",
    "Tiny Kong is the youngest sister of Dixie Kong.",
    "Mornin.",
    "Lanky Kong is the only kong with no canonical relation to the main Kong family tree.",
    "Despite the line in the DK Rap stating otherwise, Chunky is the kong who can jump highest in DK64.",
    "Despite the line in the DK Rap stating otherwise, Tiny is one of the two slowest kongs in DK64.",
    "If you fail the twelfth round of K. Rool, the game will dictate that K. Rool is victorious and end the fight.",
    "Donkey Kong 64 Randomizer started as a LUA Script in early 2019, evolving into a ROM Hack in 2021.",
    "The maximum in-game time that the vanilla file screen time can display is 1165 hours and 5 minutes.",
    "Chunky Kong is the brother of Kiddy Kong.",
    "Fungi Forest contains mushrooms.",
    "Igloos can be found in Crystal Caves.",
    "Frantic Factory has multiple floors where things can be found.",
    "Angry Aztec has so much sand, it's even in the wind.",
    "You can find a rabbit in Fungi Forest and in Crystal Caves.",
    "You can find a beetle in Angry Aztec and in Crystal Caves.",
    "You can find a vulture in Angry Aztec.",
    "You can find an owl in Fungi Forest.",
    "You can find two boulders in Jungle Japes",
    "To buy moves, you will need coins.",
    "You can change the music and sound effects volume in the sound settings on the main menu.",
    "Coin Hoard is a Monkey Smash game mode where players compete to collect the most coins.",
    "Capture Pad is a Monkey Smash game mode where players attempt to capture pads in different corners of the arena.",
    "I have nothing to say to you.",
    "I had something to tell you, but I forgot what it is.",
    "I don't know anything.",
    "I'm as lost as you are. Good luck!",
    "Wrinkly? Never heard of him.",
    "This is it. The peak of all randomizers. No other randomizer exists besides DK64 Randomizer where you can listen to the dk rap in its natural habitat while freeing Chunky Kong in Jungle Japes.",
    "Why do they call it oven when you of in the cold food of out hot eat the food?",
    "Wanna become famous? Buy followers, coconuts and donks at DK64Randomizer (DK64Randomizer . com)!",
    "What you gonna do, SpikeVegeta?",
    "You don't care? Just give it to me? Okay, here it is.",
    "Rumor has it this game was developed in a cave with only a box of scraps!",
    "BOINNG! BOINNG! The current time is: 8:01!",
    "If you backflip right before Chunky punches K. Rool, you must go into first person camera to face him before the punch.",
    "The barrier to \x08Hideout Helm\x08 can be cleared by obtaining \x04801 Golden Bananas\x04. It can also be cleared with fewer than that.",
    "It would be \x05foolish\x05 to \x04not save your spoiler logs\x04 from the dev site.",
    "\x04W\x04\x05O\x05\x06A\x06\x07H\x07\x08,\x08 \x04I\x04 \x05D\x05\x06R\x06\x07O\x07\x08P\x08\x04P\x04\x05E\x05\x06D\x06 \x07A\x07\x08L\x08\x04L\x04 \x05M\x05\x06Y\x06 \x07C\x07\x08R\x08\x04A\x04\x05Y\x05\x06O\x06\x07N\x07\x08S\x08\x04!\x04",
    "[[WOTB]]",
    "By using DK64Randomizer.com, users agree to release the developers from any claims, damages, bad seeds, or liabilities. Please exercise caution and randomizer responsibly.",
    "Bothered? I was bothered once. They put me in a barrel, a bonus barrel. A bonus barrel with beavers, and beavers make me bothered.",
    "Looking for useful information? Try looking at another hint.",
    "Can I interest you in some casino chips? They're tastefully decorated with Hunky Chunky.",
    "Have faith, beanlievers. Your time will come.",
    "I have horrible news. Your seed just got \x0510 percent worse.\x05",
    "Great news! Your seed just got \x0810 percent better!\x08",
    "This is not a joke hint.",
    "I'll get back to you after this colossal dump of blueprints.",
    "Something in the \x0dHalt! The remainder of this hint has been confiscated by the top Kop on the force.\x0d",
    "When I finish Pizza Tower, this hint will update.",
    "Will we see a sub hour seasonal seed? Not a chance. The movement is too optimized at this point. I expect at most 10-20 more seconds can be saved, maybe a minute with TAS.",
    "I could put something useful here, but the \x04dk64randomizer.com\x04 wiki has lots of helpful information about hints already.",
    "If you're watching on YouTube, be sure to like, comment, subscribe, and smash that bell.",
    "I could really go for a hot dog right now.",
    "You can find statues of dinosnakes in Angry Aztec.",
    "If this seed was a channel point redemption, you have my condolences. If it wasn't, you have many options for victims.",
    "You wouldn't steal a coin. You wouldn't steal a banana. You wouldn't fail to report a bug to the devs.",
    "It's time to get your counting practice in: 1, 2, 3, 4, 5, 6, 9...",
    "I asked AI to help you and it said: 'The best way to get better at this game is to play it.'",
    "The hint you're looking for is on the next page, keep scrolling.",
    "Banandium? Void Kong? Pauline? DK, what are you talking about? It's 1999! Go get Cranky to knock some sense into your head.",
]

kong_list = ["\x04Donkey\x04", "\x05Diddy\x05", "\x06Lanky\x06", "\x07Tiny\x07", "\x08Chunky\x08", "\x04Any kong\x04"]
colorless_kong_list = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
kong_colors = ["\x04", "\x05", "\x06", "\x07", "\x08", "\x0c"]

kong_cryptic = [
    [
        "The kong who is bigger, faster and potentially stronger too",
        "The kong who fires in spurts",
        "The kong with a tie",
        "The kong who slaps their instrument to the jungle beat",
    ],
    [
        "The kong who can fly real high",
        "The kong who features in the first two Donkey Kong Country games",
        "The kong who wants to see red",
        "The kong who frees the only female playable kong",
    ],
    [
        "The kong who inflates like a balloon, just like a balloon",
        "The kong who waddles in his overalls",
        "The kong who has a cold race with an insect",
        "The kong who lacks style, grace but not a funny face",
    ],
    [
        "The kong who likes jazz",
        "The kong who shoots K. Rool's tiny toes",
        "The kong who has ammo that is light as a feather",
        "The kong who can shrink in size",
    ],
    [
        "The kong who is one hell of a guy",
        "The kong who can pick up boulders",
        "The kong who fights a blocky boss",
        "The kong who bows down to a dragonfly",
    ],
    ["Members of the DK Crew", "A specific set of relatives", "A number of playable characters"],
]

all_levels = [
    Levels.JungleJapes,
    Levels.AngryAztec,
    Levels.FranticFactory,
    Levels.GloomyGalleon,
    Levels.FungiForest,
    Levels.CrystalCaves,
    Levels.CreepyCastle,
]
level_colors = ["\x08", "\x04", "\x0c", "\x06", "\x07", "\x0a", "\x09", "\x05", "\x0b", "\x0d", "\x0d"]
level_list = [
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
    "Hideout Helm",
    "DK Isles",
    "Cranky's Lab",
    "Snide's HQ",
]
short_level_list = [
    "Japes",
    "Aztec",
    "Factory",
    "Galleon",
    "Forest",
    "Caves",
    "Castle",
    "Helm",
    "Isles",
    "Cranky's Lab",
    "Snide's HQ",
]
vacation_levels_properties = [
    "Glorious Hills",
    "Arid Sands",
    "OSHA Violation Hotspot",
    "Murky Depths",
    "Blissful Greens",
    "Miners Paradise",
    "Haunted Architecture",
    "Timeless Corridors",
    "Undeniable Serenity",
    "Arcade Dwellers Paradise",
    "Rube Goldberg Cacophony",
]

level_cryptic = [
    [
        "The level with a localized storm",
        "The level with a dirt mountain",
        "The level which has two retailers and no race",
    ],
    ["The level with four vases", "The level with two kongs cages", "The level with a spinning totem"],
    [
        "The level with a toy production facility",
        "The level with a tower of blocks",
        "The level with a game from 1981",
        "The level where you need two quarters to play",
    ],
    ["The level with the most water", "The level where you free a water dweller", "The level with stacks of gold"],
    [
        "The level with only two retailers and two races",
        "The level where night can be acquired at will",
        "The level with a nocturnal tree dweller",
    ],
    ["The level with two inches of water", "The level with two ice shields", "The level with an Ice Tomato"],
    [
        "The level with battlements",
        "The level with a dungeon, ballroom and a library",
        "The level with drawbridge and a moat",
    ],
    ["The timed level", "The level with no boss", "The level with no small bananas"],
]

level_cryptic_helm_isles = level_cryptic.copy()
level_cryptic_helm_isles.append(["The hub world", "The world with DK's ugly mug on it", "The world with only a Cranky's Lab and Snide's HQ in it"])

shop_owners = ["\x04Cranky\x04", "\x04Funky\x04", "\x04Candy\x04"]
shop_cryptic = [
    [
        "The shop owner with a walking stick",
        "The shop owner who is old",
        "The shop owner who is persistently grumpy",
        "The shop owner who resides near your Treehouse",
    ],
    [
        "The shop owner who has an armory",
        "The shop owner who has a banana on his shop",
        "The shop owner with sunglasses",
        "The shop owner who calls everyone Dude",
    ],
    [
        "The shop owner who is flirtatious",
        "The shop owner who is not present in Fungi Forest",
        "The shop owner who is not present in Jungle Japes",
        "The shop owner with blonde hair",
    ],
]

crankys_cryptic = ["a location out of this world", "a location 5000 points deep", "a mad scientist's laboratory"]
level_cryptic_helm_isles.append(crankys_cryptic)

snides_cryptic = ["the home of the King K Industries employee", "a place to go to if you need time", "a base of covert operations"]
level_cryptic_helm_isles.append(snides_cryptic)

item_type_names = {
    Types.Blueprint: "\x06a kasplat\x06",
    Types.Fairy: "\x06a fairy\x06",
    Types.Crown: "\x06a battle arena\x06",
    Types.RainbowCoin: "\x06a dirt patch\x06",
    Types.CrateItem: "\x06a melon crate\x06",
    Types.Enemies: "\x06an enemy\x06",
    Types.Hint: "\x06a hint door\x06",
    Types.BoulderItem: "\x06a holdable object\x06",
}
item_type_names_cryptic = {
    Types.Blueprint: ["a minion of K. Rool", "a shockwaving foe", "a colorfully haired henchman"],
    Types.Fairy: ["an aerial ace", "a bit of flying magic", "a Queenly representative"],
    Types.Crown: ["a contest of endurance", "a crowning achievement", "the visage of K. Rool"],
    Types.RainbowCoin: ["the initials of DK", "a muddy mess", "buried treasure"],
    Types.CrateItem: ["a bouncing box", "a breakable cube", "a crate of goodies"],
    Types.Enemies: ["a minor discouragement", "an obstacle along the way", "something found in mad maze maul"],
    Types.Hint: ["a source of a riddle", "the old granny house", "a door to the granny"],
    Types.BoulderItem: ["an object of relative ease", "something as solid as a rock"],
}

moves_data = [
    # Commented out logic sections are saved if we need to revert to the old hint system
    # Donkey
    MoveInfo(name="Baboon Blast", move_level=1, move_type="special", kong=Kongs.donkey),
    MoveInfo(name="Strong Kong", move_level=2, move_type="special", kong=Kongs.donkey),
    MoveInfo(name="Gorilla Grab", move_level=3, move_type="special", kong=Kongs.donkey),
    # Diddy
    MoveInfo(name="Chimpy Charge", move_level=1, move_type="special", kong=Kongs.diddy),
    MoveInfo(name="Rocketbarrel Boost", move_level=2, move_type="special", kong=Kongs.diddy, important=True),  # (spoiler.settings.krool_diddy or spoiler.settings.helm_diddy)),
    MoveInfo(name="Simian Spring", move_level=3, move_type="special", kong=Kongs.diddy),
    # Lanky
    MoveInfo(name="Orangstand", move_level=1, move_type="special", kong=Kongs.lanky),
    MoveInfo(name="Baboon Balloon", move_level=2, move_type="special", kong=Kongs.lanky),
    MoveInfo(name="Orangstand Sprint", move_level=3, move_type="special", kong=Kongs.lanky),
    # Tiny
    MoveInfo(name="Mini Monkey", move_level=1, move_type="special", kong=Kongs.tiny, important=True),  # spoiler.settings.krool_tiny),
    MoveInfo(name="Ponytail Twirl", move_level=2, move_type="special", kong=Kongs.tiny),
    MoveInfo(name="Monkeyport", move_level=3, move_type="special", kong=Kongs.tiny, important=True),
    # Chunky
    MoveInfo(name="Hunky Chunky", move_level=1, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    MoveInfo(name="Primate Punch", move_level=2, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    MoveInfo(name="Gorilla Gone", move_level=3, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    # Slam
    MoveInfo(name="Slam Upgrade", move_level=1, move_type="slam", kong=Kongs.any),
    MoveInfo(name="Slam Upgrade", move_level=2, move_type="slam", kong=Kongs.any),
    MoveInfo(name="Slam Upgrade", move_level=3, move_type="slam", kong=Kongs.any),
    # Guns
    MoveInfo(name="Coconut Shooter", move_level=1, move_type="gun", kong=Kongs.donkey, important=True),
    MoveInfo(name="Peanut Popguns", move_level=1, move_type="gun", kong=Kongs.diddy, important=True),  # spoiler.settings.krool_diddy),
    MoveInfo(name="Grape Shooter", move_level=1, move_type="gun", kong=Kongs.lanky),
    MoveInfo(name="Feather Bow", move_level=1, move_type="gun", kong=Kongs.tiny, important=True),  # spoiler.settings.krool_tiny),
    MoveInfo(name="Pineapple Launcher", move_level=1, move_type="gun", kong=Kongs.chunky),
    # Gun Upgrades
    MoveInfo(name="Homing Ammo", move_level=2, move_type="gun", kong=Kongs.any),
    MoveInfo(name="Sniper Scope", move_level=3, move_type="gun", kong=Kongs.any),
    # Ammo Belt
    MoveInfo(name="Ammo Belt Upgrade", move_level=1, move_type="ammo_belt", kong=Kongs.any),
    MoveInfo(name="Ammo Belt Upgrade", move_level=2, move_type="ammo_belt", kong=Kongs.any),
    # Instruments
    MoveInfo(name="Bongo Blast", move_level=1, move_type="instrument", kong=Kongs.donkey, important=True),  # spoiler.settings.helm_donkey),
    MoveInfo(name="Guitar Gazump", move_level=1, move_type="instrument", kong=Kongs.diddy, important=True),  # spoiler.settings.helm_diddy),
    MoveInfo(name="Trombone Tremor", move_level=1, move_type="instrument", kong=Kongs.lanky, important=True),  # (spoiler.settings.helm_lanky or spoiler.settings.krool_lanky)),
    MoveInfo(name="Saxophone Slam", move_level=1, move_type="instrument", kong=Kongs.tiny, important=True),  # spoiler.settings.helm_tiny),
    MoveInfo(name="Triangle Trample", move_level=1, move_type="instrument", kong=Kongs.chunky, important=True),  # spoiler.settings.helm_chunky),
    # Instrument Upgrades
    MoveInfo(name="Instrument Upgrade", move_level=2, move_type="instrument", kong=Kongs.any),
    MoveInfo(name="Instrument Upgrade", move_level=3, move_type="instrument", kong=Kongs.any),
    MoveInfo(name="Instrument Upgrade", move_level=4, move_type="instrument", kong=Kongs.any),
]

kong_placement_levels = [
    {"name": "Jungle Japes", "level": 0},
    {"name": "Llama Temple", "level": 1},
    {"name": "Tiny Temple", "level": 1},
    {"name": "Frantic Factory", "level": 2},
]

boss_names = {
    Maps.JapesBoss: "Army Dillo 1",
    Maps.AztecBoss: "Dogadon 1",
    Maps.FactoryBoss: "Mad Jack",
    Maps.GalleonBoss: "Pufftoss",
    Maps.FungiBoss: "Dogadon 2",
    Maps.CavesBoss: "Army Dillo 2",
    Maps.CastleBoss: "King Kut Out",
    Maps.KroolDonkeyPhase: "DK Phase",
    Maps.KroolDiddyPhase: "Diddy Phase",
    Maps.KroolLankyPhase: "Lanky Phase",
    Maps.KroolTinyPhase: "Tiny Phase",
    Maps.KroolChunkyPhase: "Chunky Phase",
}
boss_colors = {
    Maps.JapesBoss: "\x08",
    Maps.AztecBoss: "\x04",
    Maps.FactoryBoss: "\x0c",
    Maps.GalleonBoss: "\x06",
    Maps.FungiBoss: "\x07",
    Maps.CavesBoss: "\x0a",
    Maps.CastleBoss: "\x09",
    Maps.KroolDonkeyPhase: "\x04",
    Maps.KroolDiddyPhase: "\x05",
    Maps.KroolLankyPhase: "\x06",
    Maps.KroolTinyPhase: "\x07",
    Maps.KroolChunkyPhase: "\x08",
}

PointSpreadSelector = []
PointSpreadBase = [
    ("Kongs", 11),
    ("Keys", 11),
    ("Guns", 9),
    ("Instruments", 9),
    ("Training Moves", 7),
    ("Fairy Moves", 7),
    ("Important Shared", 5),
    ("Pad Moves", 3),
    ("Barrel Moves", 7),
    ("Active Moves", 5),
    ("Bean", 3),
    ("Shopkeepers", 11),
]
for item in PointSpreadBase:
    PointSpreadSelector.append({"name": item[0], "value": item[0].lower().replace(" ", "_"), "tooltip": "", "default": item[1]})
