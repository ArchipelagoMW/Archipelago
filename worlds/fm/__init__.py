import typing
import warnings

from itertools import chain
from collections import Counter
from worlds.AutoWorld import World, WebWorld
from BaseClasses import CollectionState, Region, Tutorial, LocationProgressType
from worlds.generic.Rules import set_rule
from .items import item_name_to_item_id as item_id_map
from .items import create_item as fabricate_item
from .items import FMItem, create_victory_event, create_starchip_items, starchip_item_ids_to_starchip_values
from .utils import Constants, flatten
from .locations import location_name_to_id as location_map
from .locations import FMLocation, CardLocation, DuelistLocation
from .cards import Card, all_cards
from .options import (FMOptions, DuelistProgression, Final6Progression, Final6Sequence, ATecTrap,
                      ItemMode, duelist_progression_map)
from .duelists import Duelist, mage_pairs, map_duelists_to_ids
from .drop_pools import DuelRank, Drop
# This registers the client. The comment ignores "unused import" linter messages
from .client import FMClient  # type: ignore  # noqa
from .logic import (get_all_cards_that_have_locations, filter_to_in_logic_cards, get_unlocked_duelists,
                    LogicCard)
from .version import __version__


class FMWeb(WebWorld):
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing {Constants.GAME_NAME} with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["sg4e"]
    )

    tutorials = [setup_en]


MINIMUM_FARM_VIABILITY: typing.Final[int] = 3


class FMWorld(World):
    """Yu-Gi-Oh! Forbidden Memories is a PlayStation RPG with card-battling mechanics. Assume the role of the Prince of
    Egypt who transcends time in order to thwart a cataclysmic evil."""
    game: str = Constants.GAME_NAME
    options_dataclass = FMOptions
    options: FMOptions
    required_client_version = (0, 4, 4)
    web = FMWeb()

    final_6_order: typing.List[Duelist]
    # each tuple is a group of duelists unlocked with a single Progressive Duelist item before Final 6
    # duelist_unlock_order[0] is unlocked from the start
    # Final 6 unlocks are handled separately
    duelist_unlock_order: typing.List[typing.Tuple[Duelist, ...]]

    location_name_to_id = location_map
    item_name_to_id = item_id_map

    def get_available_duelists(self, state: CollectionState) -> typing.List[Duelist]:
        progressive_duelist_item_count: int = state.count(Constants.PROGRESSIVE_DUELIST_ITEM_NAME, self.player)
        return get_unlocked_duelists(progressive_duelist_item_count, self.duelist_unlock_order, self.final_6_order)

    def is_card_location_accessible_with_duelists(self, location: CardLocation,
                                                  duelists_available: typing.List[Duelist]) -> bool:
        card_probs: typing.List[Drop] = [drop for drop in location.accessible_drops if drop.duelist in
                                         duelists_available]
        if not card_probs:
            return False
        if any(drop.duel_rank is DuelRank.SAPOW or drop.duel_rank is DuelRank.BCD for drop in card_probs):
            return True
        if any(drop.duel_rank is DuelRank.SATEC for drop in card_probs):
            # ATecs are in logic only if the player has access to farming a trap
            # Acid Trap Hole and Widespread Ruin BCD drops:
            trap_drops: typing.List[Duelist] = [Duelist.PEGASUS, Duelist.ISIS, Duelist.KAIBA]
            if self.options.atec_trap.value <= ATecTrap.option_invisible_wire:
                trap_drops.extend((Duelist.BANDIT_KEITH, Duelist.MAI_VALENTINE, Duelist.YAMI_BAKURA))
            if self.options.atec_trap.value <= ATecTrap.option_fake_trap:
                trap_drops.extend((Duelist.SIMON_MURAN, Duelist.TEANA, Duelist.JONO, Duelist.VILLAGER1))
            return any(duelist in duelists_available for duelist in trap_drops)
        return False

    def is_card_location_accessible(self, location: CardLocation, state: CollectionState) -> bool:
        return self.is_card_location_accessible_with_duelists(location, self.get_available_duelists(state))

    def generate_early(self) -> None:
        self.final_6_order = [Duelist.GUARDIAN_SEBEK, Duelist.GUARDIAN_NEKU, Duelist.HEISHIN_2ND, Duelist.SETO_3RD,
                              Duelist.DARKNITE]
        if self.options.final6_sequence.value >= Final6Sequence.option_first_5_shuffled:
            self.random.shuffle(self.final_6_order)
        if self.options.final6_sequence.value == Final6Sequence.option_all_6_shuffled:
            self.final_6_order.insert(self.random.randint(0, len(self.final_6_order)), Duelist.NITEMARE)
        else:
            self.final_6_order.append(Duelist.NITEMARE)

        self.duelist_unlock_order = list(duelist_progression_map[self.options.duelist_progression.value])
        if self.options.randomize_duelist_order:
            starting_unlocks: typing.Tuple[Duelist, ...] = self.duelist_unlock_order[0]
            to_randomize: typing.List[typing.Tuple[Duelist, ...]] = self.duelist_unlock_order[1:]
            self.random.shuffle(to_randomize)
            to_randomize.insert(0, starting_unlocks)
            self.duelist_unlock_order = to_randomize
        if self.options.duelist_progression.value == DuelistProgression.option_campaign:
            def pop_random_pair(x): return x.pop(self.random.randint(0, len(x) - 1))
            mages = list(mage_pairs)
            first_mages_unlocked: typing.List[Duelist] = []
            for _ in range(2):
                pair = pop_random_pair(mages)
                first_mages_unlocked.extend(pair)
            self.duelist_unlock_order.append(tuple(first_mages_unlocked))
            self.duelist_unlock_order.append((Duelist.LABYRINTH_MAGE,))
            self.duelist_unlock_order.append((Duelist.SETO_2ND,))
            self.duelist_unlock_order.append(tuple(flatten(mages)))
        elif self.options.duelist_progression.value == DuelistProgression.option_singular:
            mages = list(chain.from_iterable(mage_pairs))
            mages += [Duelist.LABYRINTH_MAGE, Duelist.SETO_2ND]
            self.random.shuffle(mages)
            for mage in mages:
                self.duelist_unlock_order.append((mage,))
        elif self.options.duelist_progression.value != DuelistProgression.option_thematic:
            raise ValueError(f"Invalid DuelistProgression option: {self.options.duelist_progression.value}")

    def create_item(self, name: str) -> FMItem:
        return fabricate_item(name, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        # All duelists are accessible from the menu, so it's our only region
        free_duel_region = Region("Free Duel", self.player, self.multiworld)

        # If obtaining a card is outside of the player's settings, set it to excluded
        card_locations: typing.List[CardLocation] = []
        valid_cards_for_locations: typing.List[Card] = get_all_cards_that_have_locations(self.options)
        in_logic_cards: typing.List[LogicCard] = filter_to_in_logic_cards(valid_cards_for_locations, self.options)
        for logic_card in in_logic_cards:
            loc = CardLocation(free_duel_region, self.player, logic_card.card, logic_card.accessible_drops)
            card_locations.append(loc)

        # Tracker doesn't care about these. The logic is irrevelant; they are excluded from the pool
        # and guaranteed to be worthless
        for out_of_logic_card in [
            c for c in valid_cards_for_locations if c.id not in map(lambda c: c.card.id, in_logic_cards)
        ]:
            loc = CardLocation(free_duel_region, self.player, out_of_logic_card, out_of_logic_card.drop_pool)
            loc.exclude()
            card_locations.append(loc)
        for loc in card_locations:
            set_rule(loc, lambda state, card_location=loc: self.is_card_location_accessible(card_location, state))

        # Handle half-check mode if set
        reward_cards: typing.List[Card] = []
        if self.options.item_mode.value == ItemMode.option_cards:
            reward_pool_size = len(card_locations) // 2
            reward_indices: typing.List[int] = self.random.sample(range(len(card_locations)), reward_pool_size)
            reward_card_locations: typing.List[CardLocation] = [
                card for i, card in enumerate(card_locations) if i not in reward_indices
            ]
            card_locations = [card for card in card_locations if card not in reward_card_locations]
            if self.options.unobtainable_rewards:
                reward_cards = [card for card in all_cards if card not in [cl.card for cl in card_locations]]
            else:
                reward_cards = [loc.card for loc in reward_card_locations]

        free_duel_region.locations.extend(card_locations)
        # Add duelist locations
        # Hold a reference to these to set locked items and victory event
        final_6_duelist_locations: typing.List[DuelistLocation] = []
        for duelist in Duelist:
            if duelist is not Duelist.HEISHIN:
                duelist_location: DuelistLocation = DuelistLocation(free_duel_region, self.player, duelist)
                set_rule(duelist_location, (lambda state, d=duelist_location:
                                            d.duelist in self.get_available_duelists(state)))
                if duelist.is_final_6:
                    final_6_duelist_locations.append(duelist_location)  # These get added to the region later
                else:
                    free_duel_region.locations.append(duelist_location)
        final_6_duelist_locations.sort(key=lambda x: self.final_6_order.index(x.duelist))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            Constants.VICTORY_ITEM_NAME, self.player
        )

        itempool: typing.List[FMItem] = []
        if self.options.final6_progression.value == Final6Progression.option_fixed:
            for i in range(len(final_6_duelist_locations) - 1):
                final_6_duelist_locations[i].place_locked_item(
                    self.create_item(Constants.PROGRESSIVE_DUELIST_ITEM_NAME)
                )
        elif self.options.final6_progression.value == Final6Progression.option_shuffled:
            for _ in range(len(final_6_duelist_locations) - 1):
                itempool.append(self.create_item(Constants.PROGRESSIVE_DUELIST_ITEM_NAME))
        else:
            raise ValueError(f"Invalid Final6Progression option: {self.options.final6_progression.value}")
        final_6_duelist_locations[-1].place_locked_item(create_victory_event(self.player))
        free_duel_region.locations.extend(final_6_duelist_locations)
        # Add progressive duelist items
        # This is not an off-by-one error
        for _ in range(len(self.duelist_unlock_order) + self.options.extra_progressive_duelists):
            itempool.append(self.create_item(Constants.PROGRESSIVE_DUELIST_ITEM_NAME))
        # Fill the item pool with starchips; Final 6 duelist locations are all placed manually
        filler_slots: int = len(free_duel_region.locations) - len(itempool) - len(final_6_duelist_locations)
        # With shuffled progression, the first 5 F6 duelists do not have lock-placed items in their locations
        if self.options.final6_progression.value == Final6Progression.option_shuffled:
            filler_slots += len(final_6_duelist_locations) - 1
        assert (
            sum(1 for loc in free_duel_region.locations if not loc.item) - len(itempool) == filler_slots
        ), "Filler slots and filler locations do not match."
        starchip_items: typing.List[FMItem] = []
        if self.options.item_mode.value == ItemMode.option_starchips:
            starchip_items += create_starchip_items(self.player, filler_slots, self.random)
        elif self.options.item_mode.value == ItemMode.option_cards:
            self.random.shuffle(reward_cards)
            # For some reason, additional (16) locations go unfilled, so double-up the item pool to fill them
            reward_cards += reward_cards
            itempool += [fabricate_item(card.name, self.player) for card in reward_cards][:filler_slots]
        else:
            raise ValueError(f"Invalid ItemMode: {self.options.item_mode.value}")
        if self.options.local_starchips and self.options.item_mode.value == ItemMode.option_starchips:
            assert all([x.code for x in starchip_items])
            starchip_items.sort(key=lambda x: starchip_item_ids_to_starchip_values[x.code] if x.code else 0)
            split_index: int = len(starchip_items) * 3 // 4
            local_starchip_items: typing.List[FMItem] = starchip_items[:split_index]
            foreign_starchip_items: typing.List[FMItem] = starchip_items[split_index:]
            itempool.extend(foreign_starchip_items)
            # Start by filling all excluded locations with filler
            excluded_locations: typing.List[FMLocation] = [
                typing.cast(FMLocation, loc) for loc in free_duel_region.locations if (
                    loc.progress_type == LocationProgressType.EXCLUDED and not loc.item
                    )
            ]
            self.random.shuffle(excluded_locations)
            starchip_index: int = 0
            while starchip_index < len(local_starchip_items) and starchip_index < len(excluded_locations):
                excluded_locations[starchip_index].place(local_starchip_items[starchip_index])
                starchip_index += 1
            # Distribute remaining local starchip items across pools
            unfilled_locs: typing.List[CardLocation] = [loc for loc in free_duel_region.locations if (
                isinstance(loc, CardLocation) and not loc.item
            )]
            farm_logical_drops: typing.Counter[typing.Tuple[Duelist, DuelRank]] = Counter()
            for loc in unfilled_locs:
                farm_logical_drops.update([(drop.duelist, drop.duel_rank) for drop in loc.accessible_drops])
            while unfilled_locs and starchip_index < len(local_starchip_items):
                potential_place: CardLocation = self.random.choice(unfilled_locs)
                # If any match, farm is endangered and isn't eligible.
                if not any(farm_logical_drops[(drop.duelist, drop.duel_rank)] <= MINIMUM_FARM_VIABILITY for drop in
                           potential_place.accessible_drops):
                    for drop in potential_place.accessible_drops:
                        farm_logical_drops[(drop.duelist, drop.duel_rank)] -= 1
                    potential_place.place(local_starchip_items[starchip_index])
                    starchip_index += 1
                unfilled_locs.remove(potential_place)
            if starchip_index < len(local_starchip_items):
                warnings.warn(
                    "Out of locations to place local starchips. Adding "
                    f"{len(local_starchip_items) - starchip_index} starchip items to the multiworld pool..."
                )
                itempool.extend(local_starchip_items[starchip_index:])
        else:
            itempool.extend(starchip_items)
        self.multiworld.itempool.extend(itempool)

        menu_region.connect(free_duel_region)
        self.multiworld.regions.append(free_duel_region)
        self.multiworld.regions.append(menu_region)

    def write_spoiler_header(self, spoiler_handle: typing.TextIO) -> None:
        if self.options.randomize_duelist_order:
            spoiler_handle.write("\nDuelist Unlock Order:\n\n")
            for group in self.duelist_unlock_order:
                spoiler_handle.write(", ".join(map(str, group)) + "\n")

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            Constants.GENERATED_WITH_KEY: __version__,
            Constants.DUELIST_UNLOCK_ORDER_KEY: map_duelists_to_ids(self.duelist_unlock_order),
            Constants.FINAL_6_ORDER_KEY: tuple(duelist.id for duelist in self.final_6_order),
            Constants.GAME_OPTIONS_KEY: self.options.serialize(),
            Constants.DEATHLINK_OPTION_KEY: self.options.death_link.value
        }
