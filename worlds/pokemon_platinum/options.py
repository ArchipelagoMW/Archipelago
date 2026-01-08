# options.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from dataclasses import dataclass
from typing import Any
from Options import Choice, DefaultOnToggle, OptionDict, OptionError, OptionSet, PerGameCommonOptions, Range, Toggle

class RandomizeHms(DefaultOnToggle):
    """Adds the HMs to the pool."""
    display_name = "Randomize HMs"

class RandomizeBadges(DefaultOnToggle):
    """Adds the badges to the pool."""
    display_name = "Randomize Badges"

class RandomizeOverworlds(DefaultOnToggle):
    """Adds overworld items to the pool."""
    display_name = "Randomize Overworlds"

class RandomizeHiddenItems(Toggle):
    """Adds hidden items to the pool."""
    display_name = "Randomize Hidden Items"

class RandomizeNpcGifts(DefaultOnToggle):
    """Adds NPC gifts to the pool."""
    display_name = "Randomize NPC Gifts"

class RandomizeKeyItems(Choice):
    """Adds key items to the pool."""
    display_name = "Randomize Key Items"
    default = 1
    option_vanilla = 0
    option_most = 1
    option_all = 2

    def are_most_randomized(self) -> bool:
        return self.value >= self.option_most

class RandomizeRods(DefaultOnToggle):
    """Adds rods to the pool. Currently, the Super Rod is unavailable, as it is post-game."""
    display_name = "Randomize Rods"

class RandomizePoketchApps(DefaultOnToggle):
    """Adds Pokétch apps to the pool (and the Pokétch)."""
    display_name = "Randomize Poketch Apps"

class RandomizeRunningShoes(Toggle):
    """Adds the running shoes to the pool."""
    display_name = "Randomize Running Shoes"

class RandomizeBicycle(Toggle):
    """Adds the bicycle to the pool."""
    display_name = "Randomize Bicycle"

class RandomizePokedex(Toggle):
    """Add the Pokedex to the pool. Note: this also adds the national dex to the pool."""
    display_name = "Randomize Pokedex"

class RandomizeAccessories(Toggle):
    """Adds fashion accessories to the item pool."""
    display_name = "Randomize Accessories"

class HmBadgeRequirements(DefaultOnToggle):
    """Require the corresponding badge to use an HM outside of battle."""
    display_name = "Require Badges for HMs"

class RemoveBadgeRequirement(OptionSet):
    """
    Specify which HMs do not require a badge to use outside of battle. This overrides the HM Badge Requirements setting.

    HMs should be provided in the form: "FLY", "WATERFALL", "ROCK_SMASH", etc.
    """
    display_name = "Remove Badge Requirement"
    valid_keys = ["CUT", "FLY", "SURF", "STRENGTH", "DEFOG", "ROCK_SMASH", "WATERFALL", "ROCK_CLIMB"]

class VisibilityHmLogic(DefaultOnToggle):
    """Logically require Flash or Defog for traversing and finding locations in applicable regions."""
    display_name = "Logically Require Flash or Defog for Applicable Regions"

class DowsingMachineLogic(DefaultOnToggle):
    """Logically require the Dowsing Machine to find hidden items."""
    display_name = "Logically Require Dowsing Machine for Hidden Items"

class Goal(Choice):
    """The goal of the randomizer. Currently, this only supports defeating the champion and entering the hall of fame."""
    display_name = "Goal"
    default = 0
    option_champion = 0

class AddMasterRepel(Toggle):
    """
    Add a master repel item to the item pool. The master repel is a key item.
    It is a repel that blocks all encounters, and never runs out.
    """
    display_name = "Add Master Repel"

class ExpMultiplier(Range):
    """Set an experience multiplier for all gained experience."""
    display_name = "Exp. Multiplier"
    range_start = 1
    range_end = 16
    default = 1

class BlindTrainers(Toggle):
    """
    Set whether trainers will be blind.

    This option can also be modified in the in-game options menu.
    """
    display_name = "Blind Trainers"

class GameOptions(OptionDict):
    """
    Presets in-game options.

    Allowed options and values, with default first:

    text_speed: mid/slow/fast - Sets the text speed
    sound: stereo/mono - Sets the shound mode
    battle_scene: on/off - Sets whether the battle animations are shown
    battle_style: shift/set - Sets whether pokemon can be changed when the opponent's pokemon faints
    button_mode: normal/start=x/l=a - Sets the button mode
    text_frame: 1-20 - Sets the textbox frame. "random" will pick a random frame.
    received_items_notification: jingle/nothing/message - Sets the received_items_notification.
    default_player_name: player_name/custom/random/vanilla - Sets the default player name. with player_name, tries to use the AP player name.
    default_rival_name: random/custom/player_name/vanilla - Sets the default rival name. with random, picks from one of the players in the AP.
    default_gender: vanilla/male/female/random - Sets the default gender.

    The text_speed, sound, battle_scene, battle_style, button_mode, text_frame, and received_items_notification
    options can additionally be modifier in the in-game options menu.

    for the player and rival names, the maximum length is 7 characters, and
    the following characters are accepted:
    all alphanumeric characters (A-Z, a-z, 0-9),
    and the following symbols: , . ' - : ; ! ? " ( ) ~ @ # % + * / =,
    and as spaces.
    as well, there are some special sequences.
      {"} is an opening double-quotation mark
      {'} is an opening single-quotation mark
      {.} is a centred dot (centred vertically)
      {Z} are two superimposed Zs (as in sleep)
      ^ is an upwards arrow
      {v} is a downwards arrow
      {MALE} is the male sign
      {FEMALE} is the female sign
      {...} are ellipsis
      {O.} is a circle with a dot inside it. {.O} also works
      {CIRCLE} is a circle
      {SQUARE} is a square
      {TRIANGLE} is a triangle
      {DIAMOND} is a diamond (hollow)
      {SPADE} is a spade
      {CLUB} is a club
      {HEART} is a heart
      {SUIT DIAMOND} is a diamond (filled)
      {STAR} is a star
      {NOTE} is a music note (1/8)
      {SUN} is a sun
      {CLOUD} is a cloud
      {UMBRELLA} is an umbrella
      {SILHOUETTE} is a really bad looking silhouette
      {SMILE} is a smiling face
      {LAUGH} is a laughing face
      {UPSET} is an upset face
      {FROWN} is a frowning face

    If the player or rival names do not satisfy these constraints, the game will use its original
    behaviour, where the player or rival names are entered during the starting cutscene.
    """
    display_name = "Game Options"
    default = {
        "text_speed": "mid",
        "sound": "stereo",
        "battle_scene": "on",
        "battle_style": "shift",
        "button_mode": "normal",
        "text_frame": 1,
        "received_items_notification": "jingle",
        "default_player_name": "player_name",
        "default_rival_name": "random",
        "default_gender": "vanilla",
    }

    def __getattr__(self, name: str) -> Any:
        if name in GameOptions.default:
            return self.get(name, GameOptions.default[name])
        else:
            raise AttributeError(name, self)

class RequireFlyForNorthSinnoh(Toggle):
    """
    Require HM02 Fly (and the badge if necessary) to logically access North Sinnoh.
    """
    display_name = "North Sinnoh Requires Fly"

class RequireParcelCouponsCheckRoute203(DefaultOnToggle):
    """
    Whether Looker blocks you from exiting Jubilife city towards Route 203 if you
    haven't delivered the parcel and exchanged the three coupons.
    """
    display_name = "Require Parcel and Coupons for Route 203 from Jubilife"

class ShowUnrandomizedProgressionItems(DefaultOnToggle):
    """
    Whether unrandomized progression items should be sent to the server and
    displayed in the chat. This also means that trackers will consider it a location
    to be checked. If this is off, trackers may assume that it is obtained when
    accessible.
    """
    display_name = "Show Unrandomized Progression Items"

class RemoteItems(Toggle):
    """
    Whether local items should be given in-game, or sent by the server.
    This overrides the show randomized progression items option: all items are shown.
    It is highly recommended to use nothing for received items notification, otherwise
    you will be notified twice for each item.
    """
    display_name = "Remote Items"

class FPS60(Toggle):
    """
    Whether the 60 FPS patch should be applied.

    This option can also be modified in the in-game options menu.
    """
    display_name = "60 FPS"

class AddSSTicket(Toggle):
    """
    Add the S.S. Ticket to the item pool.
    The S.S. ticket can be used to travel to the fight area before defeating Cynthia.
    """
    display_name = "Add S.S. Ticket"

class NationalDexNumMons(Range):
    """
    Number of seen regional Pokémon required to complete the Regional
    Pokédex. (This is when you can receive the National Dex from Oak)
    """
    display_name = "National Dex Num Mons"
    range_start = 1
    # range end will be expanded as more encounters are added.
    range_end = 80
    default = 60

class AddMarshPass(Toggle):
    """
    Add the Marsh Pass item to the game. The Marsh pass gives free access to the Great Marsh,
    but if it is enabled, it is required to enter. (i.e., you cannot pay to enter the Great Marsh
    if this option is enabled)
    """
    display_name = "Add Marsh Pass"

class SunyshoreEarly(Toggle):
    """
    With this option enabled, access to Sunyshore City via Valor Lakefront is no longer blocked
    until the Distortion World has been cleared.
    """
    display_name = "Early Sunyshore"

class AddStorageKey(Toggle):
    """
    Add the Storage Key item to the item pool. This allows access to the warehouse portion
    of the Veilstone Galactic HQ without having to clear all three lake events.
    """
    display_name = "Add Storage Key"

class UnownsOption(Choice):
    """
    How the Maniac Tunnel is handled.

    Vanilla: 26 Unown forms must be encountered before the Maniac Tunnel is traversable.
    Item: 28 "Unown Form" items are added to the item pool. 26 of them must be collected
    before the Maniac Tunnel is traversable.
    None: The Maniac Tunnel is always traversable.
    """
    display_name = "Unowns Choice"
    option_vanilla = 0
    option_item = 1
    option_none = 2
    default = 1

class AddBag(Toggle):
    """
    Add the bag to the item pool. Before obtaining it, the bag cannot be opened in the menu.
    """
    display_name = "Add Bag"

class PastoriaBarriers(Toggle):
    """
    Add barriers in Route 212 and Route 214, blocking the path to Pastoria City
    until the player has surf.
    """
    display_name = "Pastoria Barriers"

class HMCutIns(Toggle):
    """
    Whether HM Cut-Ins should be played.

    This option can also be modified in the in-game options menu.
    """
    display_name = "HM Cut-Ins"

class BuckPos(Toggle):
    """
    Whether Buck should be moved to the end of Stark Mountain.

    This option can also be modified in the in-game options menu.
    """
    display_name = "Buck Position"

class HBSpeed(Range):
    """
    The speed multiplier of the health bar.

    This option can also be modified in the in-game options menu.
    """
    display_name = "Healthbar Speed"
    range_start = 1
    range_end = 16
    default = 1

@dataclass
class PokemonPlatinumOptions(PerGameCommonOptions):
    hms: RandomizeHms
    badges: RandomizeBadges
    overworlds: RandomizeOverworlds
    hiddens: RandomizeHiddenItems
    npc_gifts: RandomizeNpcGifts
    key_items: RandomizeKeyItems
    rods: RandomizeRods
    poketch_apps: RandomizePoketchApps
    running_shoes: RandomizeRunningShoes
    bicycle: RandomizeBicycle
    pokedex: RandomizePokedex
    accessories: RandomizeAccessories

    hm_badge_requirement: HmBadgeRequirements
    remove_badge_requirements: RemoveBadgeRequirement
    visibility_hm_logic: VisibilityHmLogic
    dowsing_machine_logic: DowsingMachineLogic
    north_sinnoh_fly: RequireFlyForNorthSinnoh
    parcel_coupons_route_203: RequireParcelCouponsCheckRoute203
    regional_dex_goal: NationalDexNumMons
    early_sunyshore: SunyshoreEarly
    pastoria_barriers: PastoriaBarriers

    game_options: GameOptions
    blind_trainers: BlindTrainers
    hm_cut_ins: HMCutIns
    fps60: FPS60
    buck_pos: BuckPos
    hb_speed: HBSpeed

    master_repel: AddMasterRepel
    s_s_ticket: AddSSTicket
    marsh_pass: AddMarshPass
    exp_multiplier: ExpMultiplier
    storage_key: AddStorageKey
    bag: AddBag
    unown_option: UnownsOption

    show_unrandomized_progression_items: ShowUnrandomizedProgressionItems
    remote_items: RemoteItems

    goal: Goal

    def requires_badge(self, hm: str) -> bool:
        return self.hm_badge_requirement.value == 1 or hm in self.remove_badge_requirements

    def validate(self) -> None:
        if self.pastoria_barriers:
            if not self.badges and self.requires_badge("SURF"):
                raise OptionError(f"cannot enable Pastoria barriers if Surf requires the Fen Badge and badges are not randomized.")
            if not (self.hms or self.key_items.are_most_randomized()):
                raise OptionError(f"cannot enable Pastoria barriers if both HMs and Key Items are not randomized.")
        if not (self.overworlds or self.hiddens or self.npc_gifts or self.key_items.value > 0 or self.poketch_apps):
            raise OptionError(f"at least one of overworlds, hiddens, npc_gifts, key_items, or poketch apps must be enabled")
        if self.bag and self.dowsing_machine_logic and not (self.overworlds or self.npc_gifts or self.rods or self.running_shoes or self.pokedex or self.key_items.value > 0):
            raise OptionError(f"if the bag is enabled, then at least one of overworlds, npc_gifts, rods, running_shoes, pokedex, key_items must be enabled")

