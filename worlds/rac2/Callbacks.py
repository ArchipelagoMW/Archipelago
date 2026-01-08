from . import Locations
from .Rac2Interface import Rac2Planet, Rac2Interface, PauseState, Vendor, MissingAddressError
from .TextManager import *
from .data import Items, Planets
from .data.Items import EquipmentData
from .data.Locations import LocationData
from .data.RamAddresses import Addresses

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


def update(ctx: 'Rac2Context', ap_connected: bool):
    """Called continuously as long as a planet is loaded"""
    game_interface = ctx.game_interface
    planet = ctx.current_planet

    if planet is Rac2Planet.Title_Screen or planet is None:
        return

    button_input: int = game_interface.pcsx2_interface.read_int16(game_interface.addresses.controller_input)
    if button_input == 0x10F:  # L1 + L2 + R1 + R2 + SELECT
        if game_interface.switch_planet(Rac2Planet.Ship_Shack):
            game_interface.logger.info("Resetting to Ship Shack")

    replace_text(ctx, ap_connected)

    if not ap_connected:
        if ctx.notification_manager.queue_size() == 0:
            ctx.notification_manager.queue_notification("\14Warning!\10 Not connected to Archipelago server", 1.0)
        return

    try:
        handle_vendor(ctx)
    except MissingAddressError:
        pass

    if ctx.slot_data is not None:
        # Handle some edge-case weapons XP if extended weapon progression is enabled
        if ctx.slot_data.get("extend_weapon_progression", False):
            handle_specific_weapon_xp(ctx)


def init(ctx: 'Rac2Context'):
    """Called every time the player lands on a planet or connects to Archipelago server"""
    if ctx.current_planet is Rac2Planet.Title_Screen or ctx.current_planet is None:
        return

    # Allow skipping cutscenes by only pressing START on loaded saves.
    ctx.game_interface.pcsx2_interface.write_int8(ctx.game_interface.addresses.easy_cutscene_skip, 0x1)

    # Ship Wupash if option is enabled.
    if ctx.slot_data.get("skip_wupash_nebula", False):
        ctx.game_interface.pcsx2_interface.write_int8(ctx.game_interface.addresses.wupash_complete_flag, 1)

    for addr, bitmask in ctx.game_interface.addresses.cutscene_flags:
        value = ctx.game_interface.pcsx2_interface.read_int8(addr)
        if value & bitmask == 0:
            ctx.game_interface.pcsx2_interface.write_int8(addr, value | bitmask)

    # TODO: Make these warnings better
    unstuck_message: str = (
        "It appears that you don't have the required equipment to escape this area.\1\1"
        "Select Go to Ship Shack from the Special menu to fly back to the \12Ship Shack\10."
    )
    if ctx.current_planet == Rac2Planet.Tabora:
        has_heli_pack = ctx.game_interface.count_inventory_item(Items.HELI_PACK) > 0
        has_swingshot = ctx.game_interface.count_inventory_item(Items.SWINGSHOT) > 0
        if not (has_heli_pack and has_swingshot):
            ctx.notification_manager.queue_notification(unstuck_message, 5.0)

    if ctx.current_planet == Rac2Planet.Aranos_Prison:
        has_gravity_boots = ctx.game_interface.count_inventory_item(Items.GRAVITY_BOOTS) > 0
        has_levitator = ctx.game_interface.count_inventory_item(Items.LEVITATOR) > 0
        has_infiltrator = ctx.game_interface.count_inventory_item(Items.INFILTRATOR) > 0
        if not (has_gravity_boots and has_levitator and has_infiltrator):
            ctx.notification_manager.queue_notification(unstuck_message, 5.0)


def handle_specific_weapon_xp(ctx: 'Rac2Context'):
    game_interface = ctx.game_interface

    # If extended weapon progression is enabled, we need to regularly transfer XP from Qwark Statuette to Walloper,
    # since the Walloper adds XP to the wrong equipment and it would be hard to fix
    pending_walloper_xp = game_interface.get_weapon_xp(Items.QWARK_STATUETTE.offset)
    if pending_walloper_xp > 0:
        current_walloper_xp = game_interface.get_weapon_xp(Items.WALLOPER.offset)
        game_interface.set_weapon_xp(Items.QWARK_STATUETTE.offset, 0)
        # There are rare times where that XP increases even without using the walloper (most likely enemies killing
        # other enemies), so we discard the XP instead of transferring it if walloper is not equipped
        if game_interface.get_equipped_weapon() == Items.WALLOPER.offset:
            game_interface.set_weapon_xp(Items.WALLOPER.offset, current_walloper_xp + pending_walloper_xp)

    # Track decoy glove ammo to add experience on use, since it cannot do damage
    decoy_glove_ammo = game_interface.get_ammo(Items.DECOY_GLOVE)
    used_decoy_gloves = ctx.previous_decoy_glove_ammo - decoy_glove_ammo
    ctx.previous_decoy_glove_ammo = decoy_glove_ammo
    if used_decoy_gloves > 0:
        decoy_glove_xp = game_interface.get_weapon_xp(Items.DECOY_GLOVE.offset)
        game_interface.set_weapon_xp(Items.DECOY_GLOVE.offset, decoy_glove_xp + 0x180)


def replace_text(ctx: 'Rac2Context', ap_connected: bool):
    try:
        manager = TextManager(ctx)

        ctx.notification_manager.handle_notifications(ctx.game_interface, manager)

        # Replace "Short Cuts" button text with "Go to Ship Shack", since that's what the button does now
        manager.inject(0x3202, "Go to Ship Shack")

        if not ap_connected:
            return

        process_spaceship_text(manager, ctx)
        process_vendor_text(manager, ctx)

        if ctx.current_planet is Rac2Planet.Oozla:
            item_name = get_rich_item_name_from_location(ctx, Locations.OOZLA_MEGACORP_SCIENTIST.location_id)
            manager.inject(0x27AE, wrap_for_hud(f"You need %d bolts for {item_name}"))
            manager.inject(0x27AC, wrap_for_hud(f"\x12 Buy {item_name} for %d bolts"))

        elif ctx.current_planet is Rac2Planet.Maktar_Nebula:
            item_name = get_rich_item_name_from_location(ctx, Locations.MAKTAR_ARENA_CHALLENGE.location_id)
            manager.inject(0x2F46, f"You have earned {item_name}")

        elif ctx.current_planet is Rac2Planet.Barlow:
            item_name = get_rich_item_name_from_location(ctx, Locations.BARLOW_INVENTOR.location_id)
            manager.inject(0x27A0, wrap_for_hud(f"You need %d bolts for {item_name}"))
            manager.inject(0x279F, wrap_for_hud(f"\x12 Buy {item_name} for %d bolts"))

        elif ctx.current_planet is Rac2Planet.Notak:
            item_name = get_rich_item_name_from_location(ctx, Locations.NOTAK_WORKER_BOTS.location_id)
            manager.inject(0x27CE, wrap_for_hud(f"You need %d bolts for {item_name}"))
            manager.inject(0x27CF, wrap_for_hud(f"\x12 Buy {item_name} for %d bolts"))

        elif ctx.current_planet is Rac2Planet.Joba:
            item_name = get_rich_item_name_from_location(ctx, Locations.JOBA_SHADY_SALESMAN.location_id)
            manager.inject(0x27BB, wrap_for_hud(f"\x12 Buy {item_name} for %d bolts"))
            manager.inject(0x27BC, wrap_for_hud(f"You need %d bolts for {item_name}"))
            item_name = get_rich_item_name_from_location(ctx, Locations.JOBA_ARENA_BATTLE.location_id)
            manager.inject(0x2F66, f"Battle for {item_name}")
            manager.inject(0x2F96, f"You have earned {item_name}")
            item_name = get_rich_item_name_from_location(ctx, Locations.JOBA_ARENA_CAGE_MATCH.location_id)
            manager.inject(0x2F67, f"Cage Match for {item_name}")
            manager.inject(0x2F97, f"You have earned {item_name}")

        elif ctx.current_planet is Rac2Planet.Todano:
            item_name = get_rich_item_name_from_location(ctx, Locations.TODANO_STUART_ZURGO_TRADE.location_id)
            manager.inject(0x27D3, wrap_for_hud(f"You need the Qwark action figure for {item_name}"))
            manager.inject(0x27D4, wrap_for_hud(f"\x12 Trade Qwark action figure for {item_name}"))

        elif ctx.current_planet is Rac2Planet.Aranos_Prison:
            item_name = get_rich_item_name_from_location(ctx, Locations.ARANOS_PLUMBER.location_id)
            manager.inject(0x27D5, wrap_for_hud(f"You need %d bolts for {item_name}"))
            manager.inject(0x27D6, wrap_for_hud(f"\x12 Buy {item_name} for %d bolts"))

        elif ctx.current_planet is Rac2Planet.Smolg:
            item_name = get_rich_item_name_from_location(ctx, Locations.SMOLG_MUTANT_CRAB.location_id)
            manager.inject(0x27D7, wrap_for_hud(f"You need %d bolts for {item_name}"))
            manager.inject(0x27D8, wrap_for_hud(f"\x12 Buy {item_name} for %d bolts"))

        elif ctx.current_planet is Rac2Planet.Damosel:
            item_name = get_rich_item_name_from_location(ctx, Locations.DAMOSEL_HYPNOTIST.location_id)
            manager.inject(0x27DA, wrap_for_hud(f"You need %d bolts for {item_name}"))
            manager.inject(0x27DB, wrap_for_hud(f"\x12 Trade parts and %d bolts for {item_name}"))

        elif ctx.current_planet is Rac2Planet.Grelbin:
            item_name = get_rich_item_name_from_location(ctx, Locations.GRELBIN_MYSTIC_MORE_MOONSTONES.location_id)
            manager.inject(0x27DE, wrap_for_hud(f"You need 16 \x0CMoonstones\x08 for {item_name}"))
            manager.inject(0x27DF, wrap_for_hud(f"\x12 Trade 16 \x0CMoonstones\x08 for {item_name}"))
    except TypeError:
        return


def process_spaceship_text(manager: TextManager, ctx: 'Rac2Context'):
    data = Planets.SPACESHIP_SYSTEMS.get(ctx.current_planet, None)
    if data is None:
        return
    extra_locations = ctx.slot_data.get("extra_spaceship_challenge_locations", False)

    # Challenge 1-3
    for i in range(3):
        item_name = get_rich_item_name_from_location(ctx, data.challenge_locations[i])
        if i > 0 and not extra_locations:
            text = wrap_for_spaceship_menu("No reward for first completion")
            manager.inject(data.challenge_descriptions[i], text)
            continue
        if data.challenge_locations[i] in ctx.checked_locations:
            text = wrap_for_spaceship_menu(f"{COLOR_GREEN}First completion reward already obtained")
            manager.inject(data.challenge_descriptions[i], text)
        else:
            text = wrap_for_spaceship_menu(f"Obtain {item_name} on first challenge completion")
            manager.inject(data.challenge_descriptions[i], text)
        # "Received {item}" message when completing first challenge. It feels a bit inconsistent to
        # have it for challenge 1 and not the others, but it would require some work to extend or remove.
        if i == 0:
            text = wrap_for_spaceship_menu(f"Received {item_name}")
            manager.inject(data.challenge_1_completed_text, text)

    # Challenge 4 (ring race)
    remaining_challenges_text = []
    if extra_locations and data.challenge_locations[3] not in ctx.checked_locations:
        item_name = get_rich_item_name_from_location(ctx, data.challenge_locations[3])
        remaining_challenges_text.append(f"{item_name} on first challenge completion")
    if data.perfect_race_location not in ctx.checked_locations:
        item_name = get_rich_item_name_from_location(ctx, data.perfect_race_location)
        remaining_challenges_text.append(f"{item_name} on a perfect race (not missing any ring)")

    if len(remaining_challenges_text) > 0:
        text = "Obtain " + ", and ".join(remaining_challenges_text)
    elif extra_locations:
        text = f"{COLOR_GREEN}All rewards already obtained"
    else:
        text = f"{COLOR_GREEN}Perfect race reward already obtained"
    manager.inject(data.challenge_descriptions[3], wrap_for_spaceship_menu(text))


def handle_vendor(ctx: "Rac2Context"):
    interface: Rac2Interface = ctx.game_interface
    addresses: Addresses = ctx.game_interface.addresses

    if interface.get_pause_state() == PauseState.VENDOR.value:
        if interface.vendor.mode is Vendor.Mode.CLOSED and interface.vendor.get_type() is Vendor.Type.WEAPON:
            if interface.vendor.is_megacorp():
                interface.vendor.change_mode(ctx, Vendor.Mode.MEGACORP)
            else:
                interface.vendor.change_mode(ctx, Vendor.Mode.GADGETRON)

    if interface.get_pause_state() != PauseState.VENDOR.value and interface.vendor.mode is not Vendor.Mode.CLOSED:
        interface.vendor.change_mode(ctx, Vendor.Mode.CLOSED)

    # Use Down/Up to toggle between ammo/weapon mode
    holding_down: bool = interface.pcsx2_interface.read_int16(addresses.controller_input) == 0x4000
    holding_up: bool = interface.pcsx2_interface.read_int16(addresses.controller_input) == 0x1000
    if holding_down and interface.vendor.mode in [Vendor.Mode.MEGACORP, Vendor.Mode.GADGETRON]:
        interface.vendor.change_mode(ctx, Vendor.Mode.AMMO)
    if holding_up and interface.vendor.mode is Vendor.Mode.AMMO:
        if interface.vendor.is_megacorp():
            interface.vendor.change_mode(ctx, Vendor.Mode.MEGACORP)
        else:
            interface.vendor.change_mode(ctx, Vendor.Mode.GADGETRON)


def process_vendor_text(manager: TextManager, ctx: "Rac2Context") -> None:
    equipment_data: int = ctx.game_interface.addresses.planet[ctx.current_planet].equipment_data
    if not equipment_data:
        return

    vendor: Vendor = ctx.game_interface.vendor
    if vendor.mode is Vendor.Mode.MEGACORP:
        for location, weapon in zip(Locations.MEGACORP_VENDOR_LOCATIONS, Items.MEGACORP_VENDOR_WEAPONS):
            text_id = ctx.game_interface.pcsx2_interface.read_int32(equipment_data + weapon.offset * 0xE0 + 0x08)
            item_name = get_rich_item_name_from_location(ctx, location.location_id)
            manager.inject(text_id, item_name)
    elif vendor.mode is Vendor.Mode.GADGETRON:
        for location, weapon in zip(Locations.GADGETRON_VENDOR_LOCATIONS, Items.GADGETRON_VENDOR_WEAPONS):
            text_id = ctx.game_interface.pcsx2_interface.read_int32(equipment_data + weapon.offset * 0xE0 + 0x08)
            item_name = get_rich_item_name_from_location(ctx, location.location_id)
            manager.inject(text_id, item_name)
    else:
        locations: list[LocationData] = list(Locations.MEGACORP_VENDOR_LOCATIONS) + list(Locations.GADGETRON_VENDOR_LOCATIONS)
        weapons: list[EquipmentData] = list(Items.MEGACORP_VENDOR_WEAPONS) + list(Items.GADGETRON_VENDOR_WEAPONS)
        weapons.remove(Items.CLANK_ZAPPER)
        for i in range(len(locations)):
            text_id = ctx.game_interface.pcsx2_interface.read_int32(equipment_data + weapons[i].offset * 0xE0 + 0x08)
            manager.inject(text_id, weapons[i].name)
