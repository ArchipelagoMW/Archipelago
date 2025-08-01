// Written by Moisés.
// NOTE: This is an earlier version to-be-replaced.
#include <memory.h>
#include <textbox.h>

// Helper function
// https://decomp.me/scratch/9H1Uy
u32 convertUTF8StringToUTF16(char* src, u16* buffer) {
    u32 string_length = 0;

    // If the source string starts with a null char (0), we assume the string empty.
    if (*src != 0) {
        // Copy the char from the source string into the bufferination.
        // Then advance to the next char until we find the null char (0).
        do {
            *buffer = *src;
            src++;
            buffer++;
            string_length++;
        } while (*src != 0);
    }
    // Make sure to add the null char at the end of the bufferination string,
    // and then return the length of the string.
    *buffer = 0;
    return string_length;
}

// Begin printing ASCII text stored in a char*
textbox* print_text(const char* message, const s16 X_pos, const s16 Y_pos, const u8 number_of_lines, const s16 textbox_width, const u32 txtbox_flags, const void* module) {
    textbox* (*ptr_textbox_create)(void*, void*, u32) = textbox_create;
    void (*ptr_textbox_setPos)(textbox*, u16, u16, s32) = textbox_setPos;
    void (*ptr_textbox_setDimensions)(textbox*, s8, s16, u8, u8) = textbox_setDimensions;
    void (*ptr_textbox_setMessagePtr)(textbox*, u16*, s32, s16) = textbox_setMessagePtr;
    u16* (*ptr_convertUTF16ToCustomTextFormat)(u16*) = convertUTF16ToCustomTextFormat;
    void* (*ptr_malloc)(s32, u32) = malloc;
    
    textbox* txtbox = NULL;
    
    // Allocate memory for the text buffer
    u16* text_buffer = (u16*) ptr_malloc(0, 100);
    
    // Create the textbox data structure
    if (module != NULL) {
        txtbox = ptr_textbox_create(module, HUD_camera, txtbox_flags);
    }

    if (txtbox != NULL && text_buffer != NULL && message != NULL) {
        // Set text position and dimensions
        ptr_textbox_setPos(txtbox, X_pos, Y_pos, 1);
        ptr_textbox_setDimensions(txtbox, number_of_lines, textbox_width, 0, 0);
        
        // Convert the ASCII message to the CV64 custom format
        convertUTF8StringToUTF16(message, text_buffer);
        ptr_convertUTF16ToCustomTextFormat(text_buffer);
        
        // Set the text buffer pointer to the textbox data structure
        ptr_textbox_setMessagePtr(txtbox, text_buffer, 0, 0);
    }
    // We return the textbox so that we can modify its properties once it begins printing
    // (say to show, hide the text)
    return txtbox;
}

// Begin printing signed integer
textbox* print_number(const s32 number, u16* text_buffer, const s16 X_pos, const s16 Y_pos, const u8 number_of_digits, const u32 txtbox_flags, const u32 additional_text_flag, const void* module) {
    textbox* (*ptr_textbox_create)(void*, void*, u32) = textbox_create;
    void (*ptr_textbox_setPos)(textbox*, u16, u16, s32) = textbox_setPos;
    void (*ptr_textbox_setDimensions)(textbox*, s8, s16, u8, u8) = textbox_setDimensions;
    void (*ptr_textbox_setMessagePtr)(textbox*, u16*, s32, s16) = textbox_setMessagePtr;
    void (*ptr_text_convertIntNumberToText)(u32, u16*, u8, u32) = text_convertIntNumberToText;
    
    textbox* txtbox = NULL;
    
    // Create the textbox data structure
    if (module != NULL) {
        txtbox = ptr_textbox_create(module, HUD_camera, txtbox_flags);
    }

    if (txtbox != NULL && text_buffer != NULL) {
        // Set text position and dimensions
        ptr_textbox_setPos(txtbox, X_pos, Y_pos, 1);
        ptr_textbox_setDimensions(txtbox, 1, 100, 0, 0);
        
        // Convert the number to the CV64 custom format
        ptr_text_convertIntNumberToText(number, text_buffer, number_of_digits, additional_text_flag);
        
        // Set the text buffer pointer to the textbox data structure
        ptr_textbox_setMessagePtr(txtbox, text_buffer, 0, 0);
    }
    // We return the textbox so that we can modify its properties once it begins printing
    // (say to show, hide the text)
    return txtbox;
}

// Update the value of a number that began printing after calling "print_number()"
void update_printed_number(textbox* txtbox, const s32 number, u16* text_buffer, const u8 number_of_digits, const u32 additional_text_flag) {
    void (*ptr_text_convertIntNumberToText)(u32, u16*, u8, u32) = text_convertIntNumberToText;
    
    if (text_buffer != NULL) {
        ptr_text_convertIntNumberToText(number, text_buffer, number_of_digits, additional_text_flag);
        txtbox->flags |= 0x1000000;     // Needed to make sure the number updates properly
    }
}

void display_text(textbox* txtbox, const u8 display_textbox) {
    if (txtbox != NULL) {
        if (display_textbox == TRUE) {
            // Show text
            txtbox->flags &= ~HIDE_TEXTBOX;
        }
        else {
            // Hide text
            txtbox->flags |= HIDE_TEXTBOX;
        }
    }
}
