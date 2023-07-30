// Written by Moisés
#include "print.h"
#include <textbox.h>
#include <memory.h>

#define counter_X_pos 30
#define counter_Y_pos 40
#define counter_number_of_digits 2
#define GOLD_JEWEL_FONT 0x14

extern u8 bytes[13];

u16* number_text_buffer = NULL;
textbox* txtbox = NULL;

void begin_print() {
    // Allocate memory for the number text
    number_text_buffer = (u16*) malloc(0, 12);
    
    // Assuming that 0x80342814 = HUD Module
    txtbox = print_number(0, number_text_buffer, counter_X_pos, counter_Y_pos, counter_number_of_digits, 0x08600000, GOLD_JEWEL_FONT, (void*) 0x80342814);
}

void update_print(u8 i) {
    update_printed_number(txtbox, (s32) bytes[i], number_text_buffer, counter_number_of_digits, GOLD_JEWEL_FONT);
}
