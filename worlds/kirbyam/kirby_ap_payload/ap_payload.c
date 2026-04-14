#include <stdint.h>

// Kirby AP item ID base offset
#define KIRBY_ITEM_ID_BASE_OFFSET       3860000u  // must match worlds/kirbyam/data.py BASE_OFFSET

// AP Mailbox Registers
#define AP_BASE                 0x0203B000u
#define AP_IN_FLAG              (*(volatile uint32_t*)(AP_BASE + 0x04u))
#define AP_IN_ITEM_ID           (*(volatile uint32_t*)(AP_BASE + 0x08u))
#define AP_IN_PLAYER            (*(volatile uint32_t*)(AP_BASE + 0x0Cu))
#define AP_ITEM_RCVD_COUNTER    (*(volatile uint32_t*)(AP_BASE + 0x10u))
#define AP_DEBUG_LAST_ITEM_ID   (*(volatile uint32_t*)(AP_BASE + 0x14u))
#define AP_DEBUG_LAST_FROM      (*(volatile uint32_t*)(AP_BASE + 0x18u))

// Monotonic counter incremented every AP hook call (typically once per frame).
#define AP_FRAME_COUNTER        (*(volatile uint32_t*)(AP_BASE + 0x1Cu))
#define AP_HOOK_HEARTBEAT       (*(volatile uint32_t*)(AP_BASE + 0x34u))

// Shard State Registers
#define AP_SHARD_BITFIELD       (*(volatile uint32_t*)(AP_BASE + 0x00u))
// Issue #478: AP shard authority register.
// Bits are set by ap_apply_item() shard delivery; never by boss-defeat hook.
// ap_poll_mailbox_c() may initialize/seed this from native save state when
// mailbox init cookie is absent, then uses this authority when scrubbing
// non-AP-owned temporary boss shard bits after gameplay resumes.
#define AP_DELIVERED_SHARD_BITFIELD  (*(volatile uint32_t*)(AP_BASE + 0x38u))
// Issue #478: Frames remaining before the shard scrub is allowed to run.
// Set to SHARD_BOSS_CUTSCENE_FRAMES by the boss-defeat hook so the
// post-cutscene state machine has time to observe the temporary native write
// before gameplay-resume scrub eligibility is reached.
#define AP_SHARD_SCRUB_DELAY         (*(volatile uint32_t*)(AP_BASE + 0x3Cu))
#define SHARD_BOSS_CUTSCENE_FRAMES   600u  // ~10 s at 60 fps; covers post-boss shard cutscene
// Mailbox initialization cookie to protect against stale EWRAM on cold/soft reset.
#define AP_MAILBOX_INIT_COOKIE       (*(volatile uint32_t*)(AP_BASE + 0x40u))
#define AP_MAILBOX_INIT_COOKIE_VALUE 0x4B41504Du  // "KAPM"
// Tracks shard bits temporarily written by boss defeat hook for cutscene safety.
// Cleared after gameplay resumes and non-AP-owned bits are scrubbed.
#define AP_BOSS_TEMP_SHARD_BITFIELD  (*(volatile uint32_t*)(AP_BASE + 0x44u))
// Bitfield for AP vitality item replay-guard semantics.
// Bit N set means VITALITY_COUNTER_(N+1) has already been applied this EWRAM session.
#define AP_DELIVERED_VITALITY_ITEM_BITS (*(volatile uint32_t*)(AP_BASE + 0x48u))
// Runtime config for enemy copy-ability randomization live reroll hook.
#define AP_ABILITY_RANDOMIZATION_MODE   (*(volatile uint32_t*)(AP_BASE + 0x64u))
#define AP_ABILITY_RANDOMIZATION_SEED_LO (*(volatile uint32_t*)(AP_BASE + 0x68u))
#define AP_ABILITY_RANDOMIZATION_SEED_HI (*(volatile uint32_t*)(AP_BASE + 0x6Cu))
#define AP_ABILITY_RANDOMIZATION_NO_ABILITY_WEIGHT (*(volatile uint32_t*)(AP_BASE + 0x70u))
#define AP_ABILITY_RANDOMIZATION_ALLOWED_MASK (*(volatile uint32_t*)(AP_BASE + 0x74u))
#define AP_ABILITY_RANDOMIZATION_RNG_STATE (*(volatile uint32_t*)(AP_BASE + 0x78u))
#define AP_ABILITY_REROLL_EVENT_COUNTER (*(volatile uint32_t*)(AP_BASE + 0x7Cu))
#define AP_ABILITY_REROLL_SOURCE_ADDR (*(volatile uint32_t*)(AP_BASE + 0x80u))
#define AP_ABILITY_REROLL_ABILITY_ID (*(volatile uint32_t*)(AP_BASE + 0x84u))
// Boss Defeat Transport Register (Issue #35: Boss-defeat locations with shard-delivery decoupling)
// Written by ROM payload when an area boss is defeated; polled by Python client for location checks.
// Bit N set <=> boss of area N was defeated (same bit ordering as shard_bitfield, bits 0-7 used).
// Hook site: BL CollectShard inside sub_0801D948 (ROM addr 0x0801D948, callsite file offset 0x001D952).
#define AP_BOSS_DEFEAT_FLAGS    (*(volatile uint32_t*)(AP_BASE + 0x24u))
#define AP_MAJOR_CHEST_FLAGS    (*(volatile uint32_t*)(AP_BASE + 0x28u))
#define AP_VITALITY_CHEST_FLAGS (*(volatile uint32_t*)(AP_BASE + 0x2Cu))
#define AP_SOUND_PLAYER_CHEST_FLAGS (*(volatile uint32_t*)(AP_BASE + 0x30u))
#define AP_HUB_SWITCH_FLAGS (*(volatile uint32_t*)(AP_BASE + 0x4Cu))
#define AP_STARTING_KIRBY_COLOR_ID (*(volatile uint32_t*)(AP_BASE + 0x50u))
#define KIRBY_SHARD_FLAGS_ADDR  0x02038970u
#define KIRBY_SHARD_FLAGS       (*(volatile uint8_t*)(KIRBY_SHARD_FLAGS_ADDR))
#define KIRBY_ACTIVE_COLOR_ADDR    0x0203ADE0u
#define KIRBY_ACTIVE_COLOR          (*(volatile uint8_t*)(KIRBY_ACTIVE_COLOR_ADDR))
// gUnk_0203ADE0 only takes effect before the game's graphics system initialises (boot-time).
// KIRBY_TRANSITION_COLOR is the variable the game applies on every screen transition (runtime).
#define KIRBY_TRANSITION_COLOR_ADDR 0x02020FBFu
#define KIRBY_TRANSITION_COLOR      (*(volatile uint8_t*)(KIRBY_TRANSITION_COLOR_ADDR))
#define AI_KIRBY_STATE_ADDR     0x0203AD2Cu
#define AI_KIRBY_STATE          (*(volatile uint32_t*)(AI_KIRBY_STATE_ADDR))
#define DEMO_PLAYBACK_FLAGS_ADDR 0x0203AD10u
#define DEMO_PLAYBACK_FLAGS     (*(volatile uint32_t*)(DEMO_PLAYBACK_FLAGS_ADDR))
#define DEMO_PLAYBACK_ACTIVE_FLAG 0x10u
#define AI_STATE_NORMAL         300u
#define AI_STATE_DARK_MIND_CLEAR 9999u
#define AI_STATE_FULL_CLEAR     10000u
#define KIRBY_BIG_CHEST_FLAGS_ADDR 0x0203897Cu
#define KIRBY_BIG_CHEST_FLAGS   (*(volatile uint32_t*)(KIRBY_BIG_CHEST_FLAGS_ADDR))
#define KIRBY_VITALITY_COUNTER_ADDR 0x02038980u
#define KIRBY_VITALITY_COUNTER  (*(volatile uint16_t*)(KIRBY_VITALITY_COUNTER_ADDR))
// Kirby has four AP vitality counter items in the current item contract.
// Clamp native vitality state to that count so mailbox replay/reset paths
// cannot over-grant vitality above intended progression.
#define KIRBY_MAX_VITALITY_COUNTERS 4u

#define KIRBY_STRUCTS_ADDR       0x02020EE0u
#define KIRBY_CURRENT_PLAYER_ADDR 0x0203AD3Cu
#define KIRBY_CURRENT_PLAYER     (*(volatile uint8_t*)(KIRBY_CURRENT_PLAYER_ADDR))
#define KIRBY_STRUCT_STRIDE      0x1A8u
#define KIRBY_STRUCT_BATTERY_OFFSET 0xDCu
// Reverse-engineered timed-effect fields used by BonusGiveInvincibility in the
// KatAM decomp (`bonus.c`): clear the effect-reset byte, set the invincibility
// kind byte to 100, mark the state byte active, and store a 1000-tick duration.
#define KIRBY_STRUCT_INVINCIBILITY_RESET_OFFSET 0xE1u
#define KIRBY_STRUCT_INVINCIBILITY_DURATION_OFFSET 0xE2u
#define KIRBY_STRUCT_INVINCIBILITY_KIND_OFFSET 0xE4u
#define KIRBY_STRUCT_INVINCIBILITY_STATE_OFFSET 0xE5u
#define KIRBY_STRUCT_HP_OFFSET   0x100u
#define KIRBY_STRUCT_MAX_HP_OFFSET 0x101u
#define KIRBY_INVINCIBILITY_KIND 100u
#define KIRBY_INVINCIBILITY_DURATION 1000u
#define KIRBY_EFFECT_ACTIVE_COUNTDOWN 0xFFu

// Player lives is a single byte in EWRAM
#define KIRBY_LIVES_ADDR        0x02020FE2u
#define KIRBY_LIVES             (*(volatile uint8_t*)(KIRBY_LIVES_ADDR))

// SRAM-based persistent shard state (Issue #109: Reset-Safe Mirror Shard Grant Handling)
// Reference: KitAM disassembly save system + Treasure struct observation
// These addresses mirror the persistent shard state written when changing rooms
#define SRAM_BASE               0x0E000000u
#define SRAM_SHARD_FIELD_OFFSET 0x12u  // Primary shard persistence field (Issue #109 candidate)
#define SRAM_SHARD_FIELD        (*(volatile uint8_t*)(SRAM_BASE + SRAM_SHARD_FIELD_OFFSET))

// Secondary checksum fields (Issue #109 candidates for save integrity)
// These are updated alongside shard changes to prevent save corruption on reset
#define SRAM_CHECKSUM_1_OFFSET  0x18u
#define SRAM_CHECKSUM_1         (*(volatile uint8_t*)(SRAM_BASE + SRAM_CHECKSUM_1_OFFSET))
#define SRAM_CHECKSUM_2_OFFSET  0x1Au
#define SRAM_CHECKSUM_2         (*(volatile uint8_t*)(SRAM_BASE + SRAM_CHECKSUM_2_OFFSET))
#define SRAM_CHECKSUM_3_OFFSET  0x1Cu
#define SRAM_CHECKSUM_3         (*(volatile uint8_t*)(SRAM_BASE + SRAM_CHECKSUM_3_OFFSET))

// Archipelago info structure (not used in this payload)
__attribute__((section(".apinfo")))
const unsigned char gArchipelagoInfo[16] = {0};


// Issue #109: Persist shard grants to SRAM to survive reset without room change
// This function writes the shard bitfield to persistent storage alongside checksum fields
// to prevent save corruption when adding shards without entering a new room.
static void persist_shard_to_sram(uint8_t new_shard_bitfield) {
    // Write the primary shard field to SRAM
    SRAM_SHARD_FIELD = new_shard_bitfield;
    
    // Update checksum fields to maintain save file integrity.
    // The game validates these when loading, so they must change consistently with shard changes.
    // These specific addresses were identified through Issue #109 investigation.
    SRAM_CHECKSUM_1 = (uint8_t)(new_shard_bitfield ^ 0xFFu);  // Inverted checksum
    SRAM_CHECKSUM_2 = (uint8_t)(new_shard_bitfield + 0x42u);  // Offset checksum
    SRAM_CHECKSUM_3 = (uint8_t)(SRAM_CHECKSUM_1 + SRAM_CHECKSUM_2); // Derived checksum
}


// Issue #35: Set the boss-defeat flag for <boss_index> (0–7) in the transport register.
// This function is the intended hook target for sub_0801D948 (ROM address 0x0801D948):
//   intercept the CollectShard(var->unk218) call site, call this instead, and let AP
//   item delivery (SHARD_N) grant the actual shard progression.
static void ap_set_boss_defeat_flag(uint32_t boss_index) {
    if (boss_index < 8u) {
        AP_BOSS_DEFEAT_FLAGS |= (1u << boss_index);
    }
}

static void ap_set_major_chest_flag(uint32_t area_id) {
    if (area_id < 32u) {
        AP_MAJOR_CHEST_FLAGS |= (1u << area_id);
    }
}

static void ap_set_vitality_chest_flag(uint32_t chest_index) {
    if (chest_index < 32u) {
        AP_VITALITY_CHEST_FLAGS |= (1u << chest_index);
    }
}

static void ap_set_sound_player_chest_flag(uint32_t chest_index) {
    if (chest_index < 32u) {
        AP_SOUND_PLAYER_CHEST_FLAGS |= (1u << chest_index);
    }
}

static void ap_set_hub_switch_flag(uint32_t door_index) {
    if (door_index < 15u) {
        AP_HUB_SWITCH_FLAGS |= (1u << door_index);
    }
}

static void ap_set_vitality_chest_flag_for_room(uint16_t room_id) {
    switch (room_id) {
        case 739u: // Carrot Castle 5-23 Big Chest
            ap_set_vitality_chest_flag(0u);
            break;
        case 815u: // Olive Ocean 6-21 Big Chest
            ap_set_vitality_chest_flag(1u);
            break;
        case 610u: // Radish Ruins 8-4 Big Chest
            ap_set_vitality_chest_flag(2u);
            break;
        case 403u: // Candy Constellation 9-8 Big Chest
            ap_set_vitality_chest_flag(3u);
            break;
        default:
            break;
    }
}

static void ap_unlock_area_map(uint32_t area_id) {
    if (area_id < 32u) {
        KIRBY_BIG_CHEST_FLAGS |= (1u << area_id);
    }
}

// Hook target for the original boss shard grant call. The game passes the boss's
// shard index in r0 (same value passed to CollectShard(var->unk218) in sub_0801D948).
// Records the AP boss-defeat transport flag for client polling AND replicates the
// native CollectShard behavior (writing KIRBY_SHARD_FLAGS + SRAM persistence) so
// that the post-cutscene state machine can continue the screen transition correctly.
// AP SHARD_N delivery (ap_apply_item) performs the same KIRBY_SHARD_FLAGS write,
// making native and AP grants idempotent when both occur on the same shard index.
// Fixes Issue #380: native shard state left stale caused a permanent white screen
// after the shard-to-hub-mirror cutscene.
__attribute__((used)) void ap_on_boss_defeat_collect_shard(uint32_t boss_index) {
    ap_set_boss_defeat_flag(boss_index);
    // Replicate CollectShard(boss_index): update native EWRAM shard bitfield and
    // persist to SRAM so the game's post-cutscene transition sees valid shard state.
    if (boss_index < 8u) {
        uint8_t mask = (uint8_t)(1u << boss_index);
        uint8_t new_shard_flags = (uint8_t)(KIRBY_SHARD_FLAGS | mask);
        KIRBY_SHARD_FLAGS = new_shard_flags;
        AP_SHARD_BITFIELD |= (uint32_t)mask;
        persist_shard_to_sram(new_shard_flags);
        // Issue #478: Hold off the per-frame shard scrub so the post-cutscene
        // state machine can read the temporary native write without white-screening.
        AP_SHARD_SCRUB_DELAY = SHARD_BOSS_CUTSCENE_FRAMES;
        AP_BOSS_TEMP_SHARD_BITFIELD |= (uint32_t)mask;
    }
}

// Hook target for native big chest reward collection. The game passes the area ID
// in r0; record the major chest AP check and intentionally do not unlock the
// native map here. Native maps are granted only when the corresponding AP map
// item is delivered through ap_apply_item().
__attribute__((used)) void ap_on_collect_big_chest(uint32_t area_id) {
    ap_set_major_chest_flag(area_id);
}

// Hook target for native vitality big chest reward collection. This callsite does
// not pass a stable argument in r0, so read the live chest object from r5 and
// map its roomId to a dedicated vitality-chest transport bit.
__attribute__((used)) void ap_on_collect_vitality_chest(void) {
    register uint32_t chest_obj_ptr asm("r5");
    uint16_t room_id = *(volatile uint16_t*)(chest_obj_ptr + 0x60u);
    ap_set_vitality_chest_flag_for_room(room_id);
}

typedef void (*KirbyCollectSoundPlayerFn)(uint32_t reward_index);
#define KIRBY_COLLECT_SOUND_PLAYER_FN ((KirbyCollectSoundPlayerFn)0x08019E69u)

typedef void (*KirbyRequestAbilityTransitionFn)(void*, uint32_t);
#define KIRBY_REQUEST_ABILITY_TRANSITION_FN ((KirbyRequestAbilityTransitionFn)0x080547C5u)

typedef void (*KirbyGiveInvincibilityFn)(void *kirby, uint16_t duration);
#define KIRBY_GIVE_INVINCIBILITY_FN ((KirbyGiveInvincibilityFn)0x0808324Du)

#define ABILITY_RANDOMIZATION_MODE_COMPLETELY_RANDOM 2u
#define KIRBY_ABILITY_MASK 0x1Fu
#define KIRBY_ABILITY_CHANGE_IS_ABILITY_STAR 0x20u
#define ENEMY_ABILITY_TABLE_BASE_ADDR 0x35164Eu
#define ENEMY_ABILITY_TABLE_STRIDE 0x18u

static uint32_t ap_mix_u32(uint32_t x) {
    x ^= x >> 16;
    x *= 0x7FEB352Du;
    x ^= x >> 15;
    x *= 0x846CA68Bu;
    x ^= x >> 16;
    return x;
}

static uint32_t ap_next_rng_u32(void) {
    uint32_t state = AP_ABILITY_RANDOMIZATION_RNG_STATE;
    if (state == 0u) {
        uint32_t seed_lo = AP_ABILITY_RANDOMIZATION_SEED_LO;
        uint32_t seed_hi = AP_ABILITY_RANDOMIZATION_SEED_HI;
        state = ap_mix_u32(seed_lo ^ (seed_hi * 0x9E3779B9u) ^ 0xA5C39E21u);
        if (state == 0u) {
            state = 0x6D2B79F5u;
        }
    }

    // xorshift32
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    if (state == 0u) {
        state = 0x6D2B79F5u;
    }
    AP_ABILITY_RANDOMIZATION_RNG_STATE = state;
    return state;
}

static uint8_t ap_select_random_allowed_ability(uint32_t allowed_mask, uint32_t random_u32) {
    uint8_t ids[32];
    uint32_t count = 0u;
    uint32_t i;
    for (i = 1u; i <= KIRBY_ABILITY_MASK; i++) {
        if ((allowed_mask & (1u << i)) != 0u) {
            ids[count++] = (uint8_t)i;
        }
    }

    if (count == 0u) {
        return 0u;
    }
    return ids[random_u32 % count];
}

// Hook target for all callsites that request Kirby ability transition.
// In completely-random mode, this rerolls a fresh ability for each request.
__attribute__((used)) void ap_on_request_copy_ability_transition(void *kirby, uint32_t ability_flags) {
    uint32_t mode = AP_ABILITY_RANDOMIZATION_MODE;
    uint32_t rewritten_flags = ability_flags;

    if (mode == ABILITY_RANDOMIZATION_MODE_COMPLETELY_RANDOM
        && (ability_flags & KIRBY_ABILITY_CHANGE_IS_ABILITY_STAR) == 0u) {
        register uint32_t source_obj_ptr asm("r5");
        uint32_t no_ability_weight = AP_ABILITY_RANDOMIZATION_NO_ABILITY_WEIGHT;
        uint32_t allowed_mask = AP_ABILITY_RANDOMIZATION_ALLOWED_MASK;
        uint32_t random_roll = ap_next_rng_u32();
        uint8_t selected_ability;
        uint32_t source_addr = 0u;

        if (no_ability_weight >= 100u) {
            selected_ability = 0u;
        } else if (no_ability_weight > 0u && (random_roll % 100u) < no_ability_weight) {
            selected_ability = 0u;
        } else {
            selected_ability = ap_select_random_allowed_ability(allowed_mask, ap_next_rng_u32());
        }

        rewritten_flags = (ability_flags & ~KIRBY_ABILITY_MASK) | (uint32_t)(selected_ability & KIRBY_ABILITY_MASK);

        if (source_obj_ptr >= 0x02000000u && source_obj_ptr < 0x02040000u) {
            uint16_t source_type = *(volatile uint16_t*)(source_obj_ptr + 0u);
            source_addr = ENEMY_ABILITY_TABLE_BASE_ADDR + ((uint32_t)source_type * ENEMY_ABILITY_TABLE_STRIDE);
        }

        AP_ABILITY_REROLL_SOURCE_ADDR = source_addr;
        AP_ABILITY_REROLL_ABILITY_ID = (uint32_t)(selected_ability & KIRBY_ABILITY_MASK);
        AP_ABILITY_REROLL_EVENT_COUNTER++;
    }

    KIRBY_REQUEST_ABILITY_TRANSITION_FN(kirby, rewritten_flags);
}

// Hook target for native Sound Player chest reward collection. Reward index 0 is
// the Sound Player unlock and should become AP-owned; all other native rewards on
// this call path should keep vanilla behavior.
__attribute__((used)) void ap_on_collect_sound_player_chest(uint32_t reward_index) {
    if (reward_index == 0u) {
        ap_set_sound_player_chest_flag(0u);
        return;
    }

    KIRBY_COLLECT_SOUND_PLAYER_FN(reward_index);
}

typedef void (*WorldMapUnlockFn)(void);

// Hook target for the world-map unlock dispatcher call in sub_08039ED4.
// r0 contains the selected unlock function pointer from gUnk_0834BD94 and r4
// holds the task pointer whose +0x08 halfword stores the WorldMapDoor index.
__attribute__((used)) void ap_on_world_map_unlock_call(WorldMapUnlockFn unlock_fn) {
    register uint32_t task_ptr asm("r4");
    uint16_t door_index = *(volatile uint16_t*)(task_ptr + 0x08u);
    ap_set_hub_switch_flag((uint32_t)door_index);
    unlock_fn();
}

static void ap_sync_active_kirby_health_from_vitality(void) {
    uint8_t player = KIRBY_CURRENT_PLAYER;
    uint32_t kirby_addr = KIRBY_STRUCTS_ADDR + ((uint32_t)player * KIRBY_STRUCT_STRIDE);
    uint16_t vitality_total_u16 = (uint16_t)(KIRBY_VITALITY_COUNTER + 6u);
    int8_t vitality_total = (vitality_total_u16 > 0x7Fu) ? 0x7F : (int8_t)vitality_total_u16;

    *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_HP_OFFSET) = vitality_total;
    *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_MAX_HP_OFFSET) = vitality_total;
}

static uint8_t ap_starting_kirby_color_applied = 0u;

static void ap_apply_starting_kirby_color_config(void) {
    uint32_t desired_color;
    uint8_t current_transition_color;

    if (ap_starting_kirby_color_applied != 0u) {
        return;
    }

    desired_color = AP_STARTING_KIRBY_COLOR_ID;

    // 0xFFFFFFFF means client has not synced the runtime config yet.
    if (desired_color == 0xFFFFFFFFu) {
        return;
    }

    // Supported native color IDs: 0..13. Value 0 (Pink) is intentionally a no-op.
    if (desired_color > 13u) {
        return;
    }
    if (desired_color == 0u) {
        ap_starting_kirby_color_applied = 1u;
        return;
    }

    // KIRBY_TRANSITION_COLOR (0x02020FBF) is the variable the game reads on each screen
    // transition to apply the active palette. If it already equals our desired color we
    // are done. Otherwise enforce the configured starting color unconditionally: the
    // spec requires "beginning of the game and on future starts", so we always apply
    // once per boot/EWRAM session regardless of what a save file or prior session left.
    current_transition_color = KIRBY_TRANSITION_COLOR;

    if ((uint32_t)current_transition_color == desired_color) {
        ap_starting_kirby_color_applied = 1u;
        return;
    }

    // Write to the transition variable so the color takes effect on the next screen change,
    // and also to the boot-time state variable in case this hook fires early enough.
    KIRBY_TRANSITION_COLOR = (uint8_t)desired_color;
    KIRBY_ACTIVE_COLOR = (uint8_t)desired_color;
    ap_starting_kirby_color_applied = 1u;
}

static uint32_t ap_get_active_kirby_addr(void) {
    return KIRBY_STRUCTS_ADDR + ((uint32_t)KIRBY_CURRENT_PLAYER * KIRBY_STRUCT_STRIDE);
}

static void ap_grant_heal_amount(uint8_t amount) {
    uint32_t kirby_addr = ap_get_active_kirby_addr();
    int8_t hp = *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_HP_OFFSET);
    int8_t max_hp = *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_MAX_HP_OFFSET);

    // Preserve dead/invalid negative HP states; mailbox healing items should not revive Kirby.
    if (hp <= 0) {
        return;
    }

    if (hp > max_hp) {
        *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_HP_OFFSET) = max_hp;
        return;
    }

    if (hp < max_hp) {
        uint16_t healed_hp = (uint16_t)((uint8_t)hp + (uint16_t)amount);
        if (healed_hp > (uint16_t)((uint8_t)max_hp)) {
            healed_hp = (uint16_t)((uint8_t)max_hp);
        }
        *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_HP_OFFSET) = (int8_t)healed_hp;
    }
}

static void ap_grant_small_food(void) {
    ap_grant_heal_amount(1u);
}

static void ap_grant_energy_drink(void) {
    ap_grant_heal_amount(2u);
}

static void ap_grant_hunk_of_meat(void) {
    ap_grant_heal_amount(3u);
}

static void ap_grant_battery(void) {
    uint32_t kirby_addr = ap_get_active_kirby_addr();
    uint8_t battery = *(volatile uint8_t*)(kirby_addr + KIRBY_STRUCT_BATTERY_OFFSET);

    if (battery <= 2u) {
        *(volatile uint8_t*)(kirby_addr + KIRBY_STRUCT_BATTERY_OFFSET) = (uint8_t)(battery + 1u);
    }
}

static void ap_grant_max_tomato(void) {
    uint32_t kirby_addr = ap_get_active_kirby_addr();
    int8_t hp = *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_HP_OFFSET);
    int8_t max_hp = *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_MAX_HP_OFFSET);

    // Preserve dead/invalid negative HP states; mailbox healing items should not revive Kirby.
    if (hp <= 0) {
        return;
    }

    *(volatile int8_t*)(kirby_addr + KIRBY_STRUCT_HP_OFFSET) = max_hp;
}

static void ap_grant_invincibility_candy(void) {
    uint32_t kirby_addr = ap_get_active_kirby_addr();

    *(volatile uint8_t*)(kirby_addr + KIRBY_STRUCT_INVINCIBILITY_RESET_OFFSET) = 0u;
    *(volatile uint8_t*)(kirby_addr + KIRBY_STRUCT_INVINCIBILITY_KIND_OFFSET) = KIRBY_INVINCIBILITY_KIND;
    *(volatile uint8_t*)(kirby_addr + KIRBY_STRUCT_INVINCIBILITY_STATE_OFFSET) = KIRBY_EFFECT_ACTIVE_COUNTDOWN;
    *(volatile uint16_t*)(kirby_addr + KIRBY_STRUCT_INVINCIBILITY_DURATION_OFFSET) = KIRBY_INVINCIBILITY_DURATION;
    KIRBY_GIVE_INVINCIBILITY_FN((void*)kirby_addr, KIRBY_INVINCIBILITY_DURATION);
}

static void ap_grant_vitality_counter(void) {
    uint16_t vitality_counter = KIRBY_VITALITY_COUNTER;

    if (vitality_counter > KIRBY_MAX_VITALITY_COUNTERS) {
        vitality_counter = KIRBY_MAX_VITALITY_COUNTERS;
    }
    if (vitality_counter < KIRBY_MAX_VITALITY_COUNTERS) {
        vitality_counter = (uint16_t)(vitality_counter + 1u);
    }

    KIRBY_VITALITY_COUNTER = vitality_counter;
    ap_sync_active_kirby_health_from_vitality();
}

static void ap_grant_lives(uint8_t amount) {
    uint8_t lives = KIRBY_LIVES;

    if (lives >= 255u) {
        return;
    }

    if ((uint16_t)lives + amount > 255u) {
        KIRBY_LIVES = 255u;
        return;
    }

    KIRBY_LIVES = (uint8_t)(lives + amount);
}

// Returns 1 if item was successfully processed, 0 if unrecognized
static uint8_t ap_apply_item(uint32_t ap_item_id) {
    // 1_UP = BASE+1
    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 1u)) {
        ap_grant_lives(1u);
        return 1u;
    }

    // SHARD_1..SHARD_8 = BASE+2 .. BASE+9
    if (ap_item_id >= (KIRBY_ITEM_ID_BASE_OFFSET + 2u) && ap_item_id <= (KIRBY_ITEM_ID_BASE_OFFSET + 9u)) {

        uint32_t shard_index = ap_item_id - (KIRBY_ITEM_ID_BASE_OFFSET + 2u); // 0..7
        uint8_t mask = (uint8_t)(1u << shard_index);

        // Issue #478: Record AP-delivered authority so the per-frame scrub knows
        // which shard bits are legitimately AP-owned.
        AP_DELIVERED_SHARD_BITFIELD |= (uint32_t)mask;

        // Update EWRAM (volatile, temporary)
        uint8_t new_shard_flags = (uint8_t)(KIRBY_SHARD_FLAGS | mask);
        KIRBY_SHARD_FLAGS = new_shard_flags;

        // Optional: keep hack mirror for AP client polling/debugging
        AP_SHARD_BITFIELD |= (uint32_t)mask;

        // Issue #109: Persist to SRAM to survive reset without room change
        persist_shard_to_sram(new_shard_flags);

        return 1u;
    }

    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 24u)) {
        ap_unlock_area_map(1u);
        return 1u;
    }

    if (ap_item_id >= (KIRBY_ITEM_ID_BASE_OFFSET + 10u) && ap_item_id <= (KIRBY_ITEM_ID_BASE_OFFSET + 17u)) {
        static const uint8_t map_area_ids[8] = {4u, 2u, 9u, 6u, 7u, 3u, 5u, 8u};
        uint32_t map_index = ap_item_id - (KIRBY_ITEM_ID_BASE_OFFSET + 10u);
        ap_unlock_area_map(map_area_ids[map_index]);
        return 1u;
    }

    // VITALITY_COUNTER_1..VITALITY_COUNTER_4 = BASE+18 .. BASE+21
    if (ap_item_id >= (KIRBY_ITEM_ID_BASE_OFFSET + 18u) && ap_item_id <= (KIRBY_ITEM_ID_BASE_OFFSET + 21u)) {
        uint32_t vitality_index = ap_item_id - (KIRBY_ITEM_ID_BASE_OFFSET + 18u);  // 0..3
        uint32_t vitality_mask = (1u << vitality_index);
        if ((AP_DELIVERED_VITALITY_ITEM_BITS & vitality_mask) == 0u) {
            AP_DELIVERED_VITALITY_ITEM_BITS |= vitality_mask;
            ap_grant_vitality_counter();
        }
        return 1u;
    }

    // SOUND_PLAYER = BASE+25
    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 25u)) {
        KIRBY_COLLECT_SOUND_PLAYER_FN(0u);
        return 1u;
    }

    // SMALL_FOOD, BATTERY, MAX_TOMATO, INVINCIBILITY_CANDY = BASE+26 .. BASE+29
    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 26u)) {
        ap_grant_small_food();
        return 1u;
    }

    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 27u)) {
        ap_grant_battery();
        return 1u;
    }

    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 28u)) {
        ap_grant_max_tomato();
        return 1u;
    }

    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 29u)) {
        ap_grant_invincibility_candy();
        return 1u;
    }

    // ENERGY_DRINK, HUNK_OF_MEAT = BASE+30 .. BASE+31
    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 30u)) {
        ap_grant_energy_drink();
        return 1u;
    }

    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 31u)) {
        ap_grant_hunk_of_meat();
        return 1u;
    }

    // Unhandled item - return 0 to signal that the flag should NOT be cleared
    return 0u;
}


void ap_poll_mailbox_c(void) {

    // Hook liveness diagnostic counter; increments on every AP hook entry.
    AP_HOOK_HEARTBEAT++;

    // Always tick a monotonic frame counter so the Python client can perform
    // deterministic, frame-based testing without relying on wall-clock time.
    AP_FRAME_COUNTER++;

    // Initialize mailbox-owned shard scrub state once per fresh EWRAM session.
    // This avoids acting on stale/garbage transport values after soft reset.
    if (AP_MAILBOX_INIT_COOKIE != AP_MAILBOX_INIT_COOKIE_VALUE) {
        uint8_t native_shards_boot = KIRBY_SHARD_FLAGS;
        AP_DELIVERED_SHARD_BITFIELD = (uint32_t)native_shards_boot;
        AP_SHARD_SCRUB_DELAY = 0u;
        AP_BOSS_DEFEAT_FLAGS = 0u;
        AP_BOSS_TEMP_SHARD_BITFIELD = 0u;
        AP_DELIVERED_VITALITY_ITEM_BITS = 0u;
        AP_HUB_SWITCH_FLAGS = 0u;
        AP_STARTING_KIRBY_COLOR_ID = 0xFFFFFFFFu;
        ap_starting_kirby_color_applied = 0u;
        AP_ABILITY_RANDOMIZATION_MODE = 0u;
        AP_ABILITY_RANDOMIZATION_SEED_LO = 0u;
        AP_ABILITY_RANDOMIZATION_SEED_HI = 0u;
        AP_ABILITY_RANDOMIZATION_NO_ABILITY_WEIGHT = 0u;
        AP_ABILITY_RANDOMIZATION_ALLOWED_MASK = 0u;
        AP_ABILITY_RANDOMIZATION_RNG_STATE = 0u;
        AP_ABILITY_REROLL_EVENT_COUNTER = 0u;
        AP_ABILITY_REROLL_SOURCE_ADDR = 0u;
        AP_ABILITY_REROLL_ABILITY_ID = 0u;
        AP_MAILBOX_INIT_COOKIE = AP_MAILBOX_INIT_COOKIE_VALUE;
    }

    uint8_t ap_delivered = (uint8_t)(AP_DELIVERED_SHARD_BITFIELD & 0xFFu);
    uint8_t native_shards = KIRBY_SHARD_FLAGS;
    uint8_t pending_boss_temp = (uint8_t)(AP_BOSS_TEMP_SHARD_BITFIELD & 0xFFu);

    // Cold-boot/soft-reset guard: before any local boss-defeat hook activity,
    // align AP-delivered authority to the current native shard save state.
    // This prevents scrub from acting on stale/uninitialized transport values.
    if (pending_boss_temp == 0u && AP_SHARD_SCRUB_DELAY == 0u) {
        if (ap_delivered != native_shards) {
            AP_DELIVERED_SHARD_BITFIELD = (uint32_t)native_shards;
        }
    } else {
        // Issue #505: keep temporary native shard visibility during post-boss
        // cutscene, but scrub to AP-owned authority as soon as gameplay resumes.
        uint32_t ai_state = AI_KIRBY_STATE;
        uint8_t gameplay_active = 0u;
        if (ai_state >= AI_STATE_NORMAL
            && ai_state != AI_STATE_DARK_MIND_CLEAR
            && ai_state != AI_STATE_FULL_CLEAR) {
            gameplay_active = 1u;
        }
        if (gameplay_active && ai_state == AI_STATE_NORMAL) {
            uint32_t demo_flags = DEMO_PLAYBACK_FLAGS;
            if ((demo_flags & DEMO_PLAYBACK_ACTIVE_FLAG) != 0u) {
                gameplay_active = 0u;
            }
        }

        if (!gameplay_active) {
            if (AP_SHARD_SCRUB_DELAY > 0u) {
                AP_SHARD_SCRUB_DELAY--;
            }
        } else {
            uint8_t scrub_mask = (uint8_t)(pending_boss_temp & (uint8_t)(~ap_delivered));
            uint8_t clamped = (uint8_t)(native_shards & (uint8_t)(~scrub_mask));
            if (clamped != native_shards) {
                KIRBY_SHARD_FLAGS = clamped;
                persist_shard_to_sram(clamped);
            }
            AP_BOSS_TEMP_SHARD_BITFIELD = 0u;
            AP_SHARD_SCRUB_DELAY = 0u;
        }
    }

    ap_apply_starting_kirby_color_config();

    // Check if there's an item to process
    uint32_t flag = AP_IN_FLAG;
    if (flag != 1u) return;

    // Receive an item from a player - read IMMEDIATELY after confirming flag
    uint32_t item = AP_IN_ITEM_ID;
    uint32_t from = AP_IN_PLAYER;

    // Debug: confirm delivery
    AP_DEBUG_LAST_ITEM_ID = item;
    AP_DEBUG_LAST_FROM = from;

    // Apply the received item
    // Returns 1 if item was recognized and processed, 0 if unrecognized.
    uint8_t item_was_processed = ap_apply_item(item);

    // Acknowledge / consume: clear flag to signal completion.
    // We ONLY clear the flag after successfully processing a valid item.
    // If the item was unrecognized (item_was_processed==0), the flag is NOT cleared,
    // allowing the client to detect a protocol mismatch and retry/stall appropriately.
    if (item_was_processed) {
        AP_ITEM_RCVD_COUNTER++;
        AP_IN_FLAG = 0u;
    }
}
