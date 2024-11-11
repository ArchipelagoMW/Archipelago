from dataclasses import dataclass
from Options import Choice, Toggle, DefaultOnToggle, Range, DeathLink, PerGameCommonOptions
import typing

if typing.TYPE_CHECKING:
    from random import Random
else:
    Random = typing.Any


class Logic(Choice):
    """
    Choose the logic used by the randomizer.
    """
    display_name = "Logic"
    option_glitchless = 0
    option_glitched = 1
    default = 0


class SkipIntro(DefaultOnToggle):
    """
    Skips escaping the police station.

    Graffiti spots tagged during the intro will not unlock items.
    """
    display_name = "Skip Intro"


class SkipDreams(Toggle):
    """
    Skips the dream sequences at the end of each chapter.

    This can be changed later in the options menu inside the Archipelago phone app.
    """
    display_name = "Skip Dreams"


class SkipHands(Toggle):
    """
    Skips spraying the lion statue hands after the dream in Chapter 5.
    """
    display_name = "Skip Statue Hands"


class TotalRep(Range):
    """
    Change the total amount of REP in your world.
    
    At least 960 REP is needed to finish the game.
    
    Will be rounded to the nearest number divisible by 8.
    """
    display_name = "Total REP"
    range_start = 1000
    range_end = 2000
    default = 1400

    def round_to_nearest_step(self):
        rem: int = self.value % 8
        if rem >= 5:
            self.value = self.value - rem + 8
        else:
            self.value = self.value - rem
    
    def get_rep_item_counts(self, random_source: Random, location_count: int) -> typing.List[int]:
        def increment_item(item: int) -> int:
            if item >= 32:
                item = 48
            else:
                item += 8
            return item

        items = [8]*location_count
        while sum(items) < self.value:
            index = random_source.randint(0, location_count-1)
            while items[index] >= 48:
                index = random_source.randint(0, location_count-1)
            items[index] = increment_item(items[index])

        while sum(items) > self.value:
            index = random_source.randint(0, location_count-1)
            while not (items[index] == 16 or items[index] == 24 or items[index] == 32):
                index = random_source.randint(0, location_count-1)
            items[index] -= 8

        return [items.count(8), items.count(16), items.count(24), items.count(32), items.count(48)]
    

class EndingREP(Toggle):
    """
    Changes the final boss to require 1000 REP instead of 960 REP to start.
    """
    display_name = "Extra REP Required"


class StartStyle(Choice):
    """
    Choose which movestyle to start with.
    """
    display_name = "Starting Movestyle"
    option_skateboard = 2
    option_inline_skates = 3
    option_bmx = 1
    default = 2


class LimitedGraffiti(Toggle):
    """
    Each graffiti design can only be used a limited number of times before being removed from your inventory.
    
    In some cases, such as completing a dream, using graffiti to defeat enemies, or spraying over your own graffiti, uses will not be counted.
    
    If enabled, doing graffiti is disabled during crew battles, to prevent softlocking.
    """
    display_name = "Limited Graffiti"


class SGraffiti(Choice):
    """
    Choose if small graffiti should be separate, meaning that you will need to switch characters every time you run out, or combined, meaning that unlocking new characters will add 5 uses that any character can use.
    
    Has no effect if Limited Graffiti is disabled.
    """
    display_name = "Small Graffiti Uses"
    option_separate = 0
    option_combined = 1
    default = 0


class JunkPhotos(Toggle):
    """
    Skip taking pictures of Polo for items.
    """
    display_name = "Skip Polo Photos"


class DontSavePhotos(Toggle):
    """
    Photos taken with the Camera app will not be saved.

    This can be changed later in the options menu inside the Archipelago phone app.
    """
    display_name = "Don't Save Photos"


class ScoreDifficulty(Choice):
    """
    Alters the score required to win score challenges and crew battles.

    This can be changed later in the options menu inside the Archipelago phone app.
    """
    display_name = "Score Difficulty"
    option_normal = 0
    option_medium = 1
    option_hard = 2
    option_very_hard = 3
    option_extreme = 4
    default = 0


class DamageMultiplier(Range):
    """
    Multiplies all damage received.

    At 3x, most damage will OHKO the player, including falling into pits.
    At 6x, all damage will OHKO the player.

    This can be changed later in the options menu inside the Archipelago phone app.
    """
    display_name = "Damage Multiplier"
    range_start = 1
    range_end = 6
    default = 1


class BRCDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    This can be changed later in the options menu inside the Archipelago phone app."


@dataclass
class BombRushCyberfunkOptions(PerGameCommonOptions):
    logic: Logic
    skip_intro: SkipIntro
    skip_dreams: SkipDreams
    skip_statue_hands: SkipHands
    total_rep: TotalRep
    extra_rep_required: EndingREP
    starting_movestyle: StartStyle
    limited_graffiti: LimitedGraffiti
    small_graffiti_uses: SGraffiti
    skip_polo_photos: JunkPhotos
    dont_save_photos: DontSavePhotos
    score_difficulty: ScoreDifficulty
    damage_multiplier: DamageMultiplier
    death_link: BRCDeathLink
