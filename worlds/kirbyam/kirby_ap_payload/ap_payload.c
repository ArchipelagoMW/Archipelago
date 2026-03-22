#include <stdint.h>

// Kirby AP item ID base offset
#define KIRBY_ITEM_ID_BASE_OFFSET       3860000u  // must match worlds/kirbyam/data.py BASE_OFFSET

// AP Mailbox Registers
#define AP_BASE                 0x0202C000u
#define AP_IN_FLAG              (*(volatile uint32_t*)(AP_BASE + 0x04u))
#define AP_IN_ITEM_ID           (*(volatile uint32_t*)(AP_BASE + 0x08u))
#define AP_IN_PLAYER            (*(volatile uint32_t*)(AP_BASE + 0x0Cu))
#define AP_ITEM_RCVD_COUNTER    (*(volatile uint32_t*)(AP_BASE + 0x10u))
#define AP_DEBUG_LAST_ITEM_ID   (*(volatile uint32_t*)(AP_BASE + 0x14u))
#define AP_DEBUG_LAST_FROM      (*(volatile uint32_t*)(AP_BASE + 0x18u))

// Monotonic counter incremented every AP hook call (typically once per frame).
#define AP_FRAME_COUNTER        (*(volatile uint32_t*)(AP_BASE + 0x1Cu))

// Shard State Registers
#define AP_SHARD_BITFIELD       (*(volatile uint32_t*)(AP_BASE + 0x00u))
// Boss Defeat Transport Register (Issue #35: Boss-defeat locations with shard-delivery decoupling)
// Written by ROM payload when an area boss is defeated; polled by Python client for location checks.
// Bit N set <=> boss of area N was defeated (same bit ordering as shard_bitfield, bits 0-7 used).
// TODO: Call ap_set_boss_defeat_flag(boss_index) from the hook at sub_0801D948 (ROM addr 0x0801D948)
//       once the exact patch-site byte offset is confirmed via Issue #110 address verification.
#define AP_BOSS_DEFEAT_FLAGS    (*(volatile uint32_t*)(AP_BASE + 0x24u))
#define KIRBY_SHARD_FLAGS_ADDR  0x02038970u
#define KIRBY_SHARD_FLAGS       (*(volatile uint8_t*)(KIRBY_SHARD_FLAGS_ADDR))

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
// Until the ROM hook is installed, AP_BOSS_DEFEAT_FLAGS stays at zero; the Python
// client will receive no boss-defeat checks but will not regress any existing behavior.
static void ap_set_boss_defeat_flag(uint32_t boss_index) {
    if (boss_index < 8u) {
        AP_BOSS_DEFEAT_FLAGS |= (1u << boss_index);
    }
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

static void ap_apply_item(uint32_t ap_item_id) {
    // 1_UP = BASE+1
    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 1u)) {
        ap_grant_lives(1u);
        return;
    }

    // 2_UP = BASE+22
    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 22u)) {
        ap_grant_lives(2u);
        return;
    }

    // 3_UP = BASE+23
    if (ap_item_id == (KIRBY_ITEM_ID_BASE_OFFSET + 23u)) {
        ap_grant_lives(3u);
        return;
    }

    // SHARD_1..SHARD_8 = BASE+2 .. BASE+9
    if (ap_item_id >= (KIRBY_ITEM_ID_BASE_OFFSET + 2u) && ap_item_id <= (KIRBY_ITEM_ID_BASE_OFFSET + 9u)) {

        uint32_t shard_index = ap_item_id - (KIRBY_ITEM_ID_BASE_OFFSET + 2u); // 0..7
        uint8_t mask = (uint8_t)(1u << shard_index);

        // Update EWRAM (volatile, temporary)
        uint8_t new_shard_flags = (uint8_t)(KIRBY_SHARD_FLAGS | mask);
        KIRBY_SHARD_FLAGS = new_shard_flags;

        // Optional: keep hack mirror for AP client polling/debugging
        AP_SHARD_BITFIELD |= (uint32_t)mask;

        // Issue #109: Persist to SRAM to survive reset without room change
        persist_shard_to_sram(new_shard_flags);

        return;
    }

    // Unhandled item
}


void ap_poll_mailbox_c(void) {

    // Always tick a monotonic frame counter so the Python client can perform
    // deterministic, frame-based testing without relying on wall-clock time.
    AP_FRAME_COUNTER++;

    // Check if there's an item to process
    if (AP_IN_FLAG != 1u) return;

    // Debug count times mailbox items received
    AP_ITEM_RCVD_COUNTER++;

    // Receive an item from a player
    uint32_t item = AP_IN_ITEM_ID;
    uint32_t from = AP_IN_PLAYER;

    // Debug: confirm delivery
    AP_DEBUG_LAST_ITEM_ID = item;
    AP_DEBUG_LAST_FROM = from;

    // Apply the received item
    ap_apply_item(item);

    // Acknowledge / consume
    AP_IN_FLAG = 0u;
}
