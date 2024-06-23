// Written by Moisés
#include "include/game/module.h"
#include "include/game/math.h"
#include "cv64.h"

extern vec3f player_pos;
extern vec3s player_angle;      // player_angle.y = Player's facing angle (yaw)
extern f32 player_height_with_respect_of_floor;     // Stored negative in-game

#define SHT_MAX 32767.0f
#define SHT_MINV (1.0f / SHT_MAX)

void spawn_item_behind_player(s32 item) {
    interactuablesModule* pickable_item = NULL;
    const f32 spawnDistance = 8.0f;
    vec3f player_backwards_dir;

    pickable_item = (interactuablesModule*)module_createAndSetChild(moduleList_findFirstModuleByID(ACTOR_CREATOR), ACTOR_ITEM);
    if (pickable_item != NULL) {
        // Convert facing angle to a vec3f
        // SHT_MINV needs to be negative here for the item to be spawned properly on the character's back
        player_backwards_dir.x = coss(-player_angle.y) * -SHT_MINV;
        player_backwards_dir.z = sins(-player_angle.y) * -SHT_MINV;
        // Multiply facing vector with distance away from the player
        vec3f_multiplyScalar(&player_backwards_dir, &player_backwards_dir, spawnDistance);
        // Assign the position of the item relative to the player's current position.
        vec3f_add(&pickable_item->position, &player_pos, &player_backwards_dir);
        // The Y position of the item will be the same as the floor right under the player
        // The player's height with respect of the flower under them is already stored negative in-game,
        // so no need to substract
        pickable_item->position.y = player_pos.y + 5.0f;
        pickable_item->height = pickable_item->position.y;

        // Assign item ID
        pickable_item->item_ID = item;
    }
}


const f32 droppingAccel = 0.05f;
const f32 maxDroppingSpeed = 1.5f;
f32 droppingSpeed = 0.0f;
f32 droppingTargetYPos = 0.0f;
u8 dropItemCalcFuncCalled = FALSE;

s32 drop_item_calc(interactuablesModule* pickable_item) {
    if (dropItemCalcFuncCalled == FALSE) {
        droppingTargetYPos = player_pos.y + player_height_with_respect_of_floor + 1.0f;
        if (pickable_item->item_ID == CROSS || pickable_item->item_ID == AXE ||
            pickable_item->item_ID == CROSS__VANISH || pickable_item->item_ID == AXE__VANISH) {
            droppingTargetYPos += 3.0f;
        }
        dropItemCalcFuncCalled = TRUE;
        return TRUE;
    }
    if (pickable_item->position.y <= droppingTargetYPos) {
        droppingSpeed = 0.0f;
        dropItemCalcFuncCalled = FALSE;
        return FALSE;
    }
    else {
        if (droppingSpeed < maxDroppingSpeed) {
            droppingSpeed += droppingAccel;
        }
        pickable_item->position.y -= droppingSpeed;
        pickable_item->height = pickable_item->position.y;
        return TRUE;
    }
}