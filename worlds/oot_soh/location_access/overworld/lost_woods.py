from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    LW_GOSSIP_STONE_SONG_FAIRY = "LW Gossip Stone Song Fairy"
    LW_BEAN_PLANT_FAIRY = "LW Bean Plant Fairy"
    LW_BUG_GRASS = "LW Bug Grass"
    LW_SKULL_KID_MASK_TRADE = "LW Skull Kid Mask Trade"
    LW_BUTTERFLY_FAIRY = "LW Butterfly Fairy"
    LW_NEAR_SHORTCUTS_GROTTO_GOSSIP_STONE_SONG_FAIRY = "LW Near Shortcuts Grotto Gossip Stone Song Fairy"
    LW_NEAR_SHORTCUTS_GROTTO_BUTTERFLY_FAIRY = "LW Near Shortcuts Grotto Butterfly Fairy"
    LW_NEAR_SHORTCUTS_GROTTO_BUG_GRASS = "LW Near Shortcuts Grotto Bug Grass"
    LW_NEAR_SHORTCUTS_GROTTO_PUDDLE_FISH = "LW Near Shortcuts Grotto Puddle Fish"
    LW_BRIDGE_BEAN_PATCH = "LW Bridge Bean Patch"
    LW_THEATER_BEAN_PATCH = "LW Theater Bean Patch"


class LocalEvents(StrEnum):
    LW_BRIDGE_BEAN_PLANTED = "LW Bridge Bean Planted"
    LW_THEATER_BEAN_PLANTED = "LW Theater Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    # LW Forest Exit
    # Connections
    connect_regions(Regions.LW_FOREST_EXIT, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True),
    ])

    # Lost Woods
    # Events
    add_events(Regions.LOST_WOODS, world, [
        (EventLocations.LW_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (EventLocations.LW_BEAN_PLANT_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (EventLocations.LW_BUG_GRASS, Events.CAN_ACCESS_BUGS,
         lambda bundle: can_cut_shrubs(bundle)),
        (EventLocations.LW_SKULL_KID_MASK_TRADE, Events.SOLD_SKULL_MASK,
         lambda bundle: is_child(bundle) and can_use(Items.SARIAS_SONG, bundle) and has_item(Events.CAN_BORROW_SKULL_MASK,
                                                                                             bundle) and has_item(
             Items.CHILD_WALLET, bundle)),
        (EventLocations.LW_BRIDGE_BEAN_PATCH, LocalEvents.LW_BRIDGE_BEAN_PLANTED,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle)),
    ])
    # Locations
    add_locations(Regions.LOST_WOODS, world, [
        (Locations.LW_SKULL_KID, lambda bundle: is_child(
            bundle) and can_use(Items.SARIAS_SONG, bundle)),
        (Locations.LW_TRADE_COJIRO, lambda bundle: is_adult(
            bundle) and can_use(Items.COJIRO, bundle)),
        (Locations.LW_TRADE_ODD_POTION, lambda bundle: is_adult(
            bundle) and can_use(Items.ODD_POTION, bundle)),
        (Locations.LW_OCARINA_MEMORY_GAME, lambda bundle:
            is_child(bundle) and has_item(Items.FAIRY_OCARINA, bundle) and ocarina_button_count(bundle) >= 5),
        (Locations.LW_TARGET_IN_WOODS, lambda bundle: is_child(
            bundle) and can_use(Items.FAIRY_SLINGSHOT, bundle)),
        (Locations.LW_DEKU_SCRUB_NEAR_BRIDGE,
         lambda bundle: is_child(bundle) and can_stun_deku(bundle)),
        (Locations.LW_GS_BEAN_PATCH_NEAR_BRIDGE,
         lambda bundle: can_spawn_soil_skull(bundle) and can_attack(bundle)),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE1,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE2,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE3,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE4,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE5,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE6,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE7,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_UNDERWATER_SHORTCUT_RUPEE8,
         lambda bundle: is_child(bundle) and (has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LW_BEAN_SPROUT_NEAR_BRIDGE_FAIRY1,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (Locations.LW_BEAN_SPROUT_NEAR_BRIDGE_FAIRY2,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (Locations.LW_BEAN_SPROUT_NEAR_BRIDGE_FAIRY3,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (Locations.LW_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.LW_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LW_SHORTCUTS_SONG_OF_STORMS_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LW_NEAR_SHORTCUTS_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SHORTCUTS_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SHORTCUTS_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.LOST_WOODS, world, [
        (Regions.LW_FOREST_EXIT, lambda bundle: True),
        (Regions.GC_WOODS_WARP, lambda bundle: True),
        (Regions.LW_BRIDGE, lambda bundle: (is_adult(bundle) and (
            has_item(LocalEvents.LW_BRIDGE_BEAN_PLANTED, bundle) or can_do_trick(Tricks.LW_BRIDGE, bundle))) or can_use(Items.HOVER_BOOTS,
                                                                                                                        bundle) or can_use(
            Items.LONGSHOT, bundle)),
        (Regions.ZR_FROM_SHORTCUT,
         lambda bundle: has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or (can_do_trick(
             Tricks.LOST_WOOD_NAVI_DIVE, bundle) and is_child(bundle) and has_item(Items.BRONZE_SCALE,
                                                                                   bundle) and can_jump_slash(bundle))),
        (Regions.LW_BEYOND_MIDO,
         lambda bundle: is_child(bundle) or can_use(Items.SARIAS_SONG, bundle) or can_do_trick(Tricks.LW_MIDO_BACKFLIP,
                                                                                               bundle)),
        (Regions.LW_NEAR_SHORTCUTS_GROTTO, lambda bundle: blast_or_smash(bundle)),
    ])

    # LW Beyond Mido
    # Events
    add_events(Regions.LW_BEYOND_MIDO, world, [
        (EventLocations.LW_BUTTERFLY_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.STICKS, bundle)),
        (EventLocations.LW_THEATER_BEAN_PATCH, LocalEvents.LW_THEATER_BEAN_PLANTED,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle)),
    ])
    # Locations
    add_locations(Regions.LW_BEYOND_MIDO, world, [
        (Locations.LW_DEKU_SCRUB_NEAR_DEKU_THEATER_RIGHT,
         lambda bundle: is_child(bundle) and can_stun_deku(bundle)),
        (Locations.LW_DEKU_SCRUB_NEAR_DEKU_THEATER_LEFT,
         lambda bundle: is_child(bundle) and can_stun_deku(bundle)),
        (Locations.LW_GS_ABOVE_THEATER, lambda bundle: is_adult(bundle) and can_get_nighttime_gs(bundle)
         and (has_item(LocalEvents.LW_THEATER_BEAN_PLANTED, bundle) and (can_attack(bundle))
              or (can_do_trick(Tricks.LW_GS_BEAN, bundle)
                  and can_use(Items.LONGSHOT, bundle)
                  and can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.BOMBCHUS_5, Items.DINS_FIRE], bundle)))),
        (Locations.LW_GS_BEAN_PATCH_NEAR_THEATER,
         lambda bundle: can_spawn_soil_skull(bundle) and (can_attack(bundle) or
                                                          (world.options.shuffle_scrubs.value == 0 and can_reflect_nuts(bundle)))),
        (Locations.LW_BOULDER_RUPEE, lambda bundle: blast_or_smash(bundle)),
        (Locations.LW_BEAN_SPROUT_NEAR_THEATRE_FAIRY1,
         lambda bundle: is_child(bundle) and has_item(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                            bundle)),
        (Locations.LW_BEAN_SPROUT_NEAR_THEATRE_FAIRY2,
         lambda bundle: is_child(bundle) and has_item(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                            bundle)),
        (Locations.LW_BEAN_SPROUT_NEAR_THEATRE_FAIRY3,
         lambda bundle: is_child(bundle) and has_item(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                            bundle)),
        (Locations.LW_AFTER_MIDO_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_AFTER_MIDO_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_AFTER_MIDO_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SFM_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SFM_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SFM_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.LW_BEYOND_MIDO, world, [
        (Regions.LW_FOREST_EXIT, lambda bundle: True),
        (Regions.LOST_WOODS, lambda bundle: is_child(
            bundle) or can_use(Items.SARIAS_SONG, bundle)),
        (Regions.SFM_ENTRYWAY, lambda bundle: True),
        (Regions.DEKU_THEATER, lambda bundle: True),
        (Regions.LW_SCRUBS_GROTTO, lambda bundle: blast_or_smash(bundle)),
    ])

    # LW Near Shortcuts Grotto
    # Events
    add_events(Regions.LW_NEAR_SHORTCUTS_GROTTO, world, [
        (EventLocations.LW_NEAR_SHORTCUTS_GROTTO_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.LW_NEAR_SHORTCUTS_GROTTO_BUTTERFLY_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: can_use(Items.STICKS, bundle)),
        (EventLocations.LW_NEAR_SHORTCUTS_GROTTO_BUG_GRASS,
         Events.CAN_ACCESS_BUGS, lambda bundle: can_cut_shrubs(bundle)),
        (EventLocations.LW_NEAR_SHORTCUTS_GROTTO_PUDDLE_FISH,
         Events.CAN_ACCESS_FISH, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.LW_NEAR_SHORTCUTS_GROTTO, world, [
        (Locations.LW_NEAR_SHORTCUTS_GROTTO_CHEST, lambda bundle: True),
        (Locations.LW_NEAR_SHORTCUTS_GROTTO_FISH,
         lambda bundle: has_bottle(bundle)),
        (Locations.LW_TUNNEL_GROTTO_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.LW_TUNNEL_GROTTO_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LW_TUNNEL_GROTTO_BEEHIVE_LEFT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.LW_TUNNEL_GROTTO_BEEHIVE_RIGHT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.LW_NEAR_SHORTCUTS_GROTTO_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SHORTCUTS_GROTTO_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SHORTCUTS_GROTTO_GRASS3,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LW_NEAR_SHORTCUTS_GROTTO_GRASS4,
         lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.LW_NEAR_SHORTCUTS_GROTTO, world, [
        (Regions.LOST_WOODS, lambda bundle: True),
    ])

    # Deku Theater
    # Locations
    add_locations(Regions.DEKU_THEATER, world, [
        (Locations.LW_DEKU_THEATER_SKULL_MASK,
         lambda bundle: is_child(bundle) and has_item(Events.CAN_BORROW_SKULL_MASK, bundle)),
        (Locations.LW_DEKU_THEATER_MASK_OF_TRUTH,
         lambda bundle: is_child(bundle) and has_item(Events.CAN_BORROW_MASK_OF_TRUTH, bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_THEATER, world, [
        (Regions.LOST_WOODS, lambda bundle: True),
    ])

    # LW Scrubs Grotto
    add_locations(Regions.LW_SCRUBS_GROTTO, world, [
        (Locations.LW_DEKU_SCRUB_GROTTO_REAR,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LW_DEKU_SCRUB_GROTTO_FRONT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LW_DEKU_SCRUB_GROTTO_BEEHIVE,
         lambda bundle: can_break_upper_beehives(bundle)),
        (Locations.LW_DEKU_SCRUB_GROTTO_SUN_FAIRY,
         lambda bundle: can_use(Items.SUNS_SONG, bundle)),
    ])
    # Connections
    connect_regions(Regions.LW_BEYOND_MIDO, world, [
        (Regions.LW_BEYOND_MIDO, lambda bundle: True),
    ])

    # LW Bridge From Forest
    # Location
    add_locations(Regions.LW_BRIDGE_FROM_FOREST, world, [
        (Locations.LW_GIFT_FROM_SARIA, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.LW_BRIDGE_FROM_FOREST, world, [
        (Regions.LW_BRIDGE, lambda bundle: True),
    ])

    # LW Bridge
    # Connections
    connect_regions(Regions.LW_BRIDGE, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True),
        (Regions.HYRULE_FIELD, lambda bundle: True),
        (Regions.LOST_WOODS, lambda bundle: can_use(Items.LONGSHOT, bundle))
    ])
