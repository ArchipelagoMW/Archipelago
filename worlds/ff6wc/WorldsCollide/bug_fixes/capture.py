from ..memory.space import Bank, Reserve, Write
from ..instruction import asm as asm
from .. import args as args

class Capture:
    def __init__(self):
        if args.fix_capture:
            self.weapon_special_mod()
            self.multisteal_mod()

    def multisteal_mod(self):
        # Fixes issue with multiple steals caused by Genji Glove and/or Offering Capture.
        # Issues resolved:
        #    1) the stolen items are not all added to your inventory (only the last successful steal is actually added)
        #    2) the message display window does not clear in between steal animations, 
        #        meaning that the first item name is the one that is displayed for all subsequent successful steals. 
        # Based in part on https://www.angelfire.com/al2/imzogelmo/patches.html#patches's Multi-Steal Fix
        #       and Bropedio's Multi-Steal fix (https://www.ff6hacking.com/forums/thread-4124-post-40232.html#pid40232)
        
        # Custom variable locations
        STOLEN_ITEM_ARRAY_START = 0x2f35
        STOLEN_ITEM_ARRAY_INDEX = 0x2f3b

        # Make the "Steal <item>" text go through the array
        src = [
            asm.REP(0x20),              #Set A to 16 bits
            asm.LDA(0x76, asm.DIR_16),  #Load first two bytes of current animation entry 
            asm.CMP(0x0302, asm.IMM16), #Check for animation opcode 2 (upper text box) and text message 3 (Steal <item>)
            asm.SEP(0x20),              #Set A back to 8 bits 
            asm.BEQ("GET_STEAL_ITEM"),  #If the above condition was true, branch
            asm.LDA(0x2f35, asm.ABS),   #Else, perform the displaced command (Note: it's unclear if this will ever get called)
            asm.RTS(),                  #      and return
            "GET_STEAL_ITEM",           
            asm.SEP(0x10),              #Set X to 8 bits
            asm.LDX(STOLEN_ITEM_ARRAY_INDEX, asm.ABS),   # Load the index to the stolen item array
            asm.LDA(STOLEN_ITEM_ARRAY_START, asm.ABS_X), # Put the item from index into A
            asm.REP(0x10),              # Set X back to 16 bits
            asm.INC(STOLEN_ITEM_ARRAY_INDEX, asm.ABS),   # Increment the array index
            asm.RTS()
        ]
        space = Write(Bank.C1, src, "Multisteal Fix: steal <item> text")
        c1_steal_print_addr = space.start_address

        # Call our new subroutine
        space = Reserve(0x15f06, 0x15f08, "Multisteal Fix: call new C1 subroutine to load stolen item into A", asm.NOP())
        space.write(
            asm.JSR(c1_steal_print_addr, asm.ABS)
        )

        #These two subroutines reset the stolen item index
        src = [
            asm.JSR(0x1429, asm.ABS),                   # displaced instruction
            asm.STZ(STOLEN_ITEM_ARRAY_INDEX, asm.ABS),  # zero the index
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Multisteal fix: reset stolen item array index routine")
        stolen_item_index_reset = space.start_address

        space = Reserve(0x2140f, 0x21411, "Multisteal Fix: reset stolen item index")
        space.write(
            asm.JSR(stolen_item_index_reset, asm.ABS)
        )

        src = [
            asm.LDA(0xb5, asm.DIR),                     # displaced instruction
            asm.ASL(),                                  # displaced instruction
            asm.STZ(STOLEN_ITEM_ARRAY_INDEX, asm.ABS),  # zero the index
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Multisteal fix: reset stolen item array index routine")
        stolen_item_index_reset = space.start_address

        space = Reserve(0x213fa, 0x213fc, "Multisteal Fix: reset stolen item index")
        space.write(
            asm.JSR(stolen_item_index_reset, asm.ABS)
        )



        # New subroutine for storing acquired item
        src = [
            asm.TSB(0x3a8c, asm.ABS),   # set character's reserve item to be added
            asm.LDA(0x32f4, asm.ABS_X), # load current reserve item
            asm.PHA(),                  # save reserve item on stack
            asm.XBA(),                  # get new item in A
            asm.STA(0x32f4, asm.ABS_X), # store new item in reserve byte
            # Store item in array for textbox
            asm.PHX(),                  # save X
            asm.LDX(STOLEN_ITEM_ARRAY_INDEX, asm.ABS),   # Load the index for the array
            asm.STA(STOLEN_ITEM_ARRAY_START, asm.ABS_X), # Store the item number into the array
            asm.INC(STOLEN_ITEM_ARRAY_INDEX, asm.ABS),   # Increment the index for highest variable stored
            asm.PLX(),                  # restore X
            # Done storing item in array for textbox
            asm.PHX(),                  # save X
            asm.JSR(0x62C7, asm.ABS),   # add reserve to obtained-items buffer
            asm.PLX(),                  # restore X
            asm.PLA(),                  # restore previous reserve item
            asm.STA(0x32f4, asm.ABS_X), # store in reserve item byte again
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Multisteal Fix: store acquired item")
        store_acquired_addr = space.start_address

        # Update steal formula where it stores the acquired item
        space = Reserve(0x239e9, 0x239f4, "Multisteal Fix: call new subroutine", asm.NOP())
        space.write(
            asm.XBA(),                             # store acquired item in B
            asm.LDA(0x3018, asm.ABS_X),            # character's unique bit
            asm.JSR(store_acquired_addr, asm.ABS), # save new item to buffer
        )

        # Fix Item Return Buffer
        space = Reserve(0x112d5, 0x112d7, "Multisteal Fix: avoid item return buffer overrun")
        space.write(
            asm.CPX(0x50, asm.IMM16) # the game only clears #$40 for item buffer, but it expects #$50
        )

    def weapon_special_mod(self):
        # http://assassin17.brinkster.net/patches.htm#anchor18
        NEW_SPECIAL_EFFECT_VAR = 0x2f3d

        #####
        # New subroutines
        #####
        # Null the dog block [displaced Square code], and clear my custom special effect byte.
        src = [
            asm.STA(0x3a83, asm.ABS),                 #Null Dog block
            asm.STZ(NEW_SPECIAL_EFFECT_VAR, asm.ABS), #Clear new special effect variable
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Capture Fix: null dog block")
        null_dog_block_addr = space.start_address

        #Call Square's per-target special effect function as normal.  Then call it again with
        # a secondary variable so the Capture command can steal, unless the first function call
        # already handled stealing.
        src = [
            asm.PHP(),
            asm.A8(),  # Set 8 bit accumulator
            asm.LDA(0x11a9, asm.ABS), # Load A with the current attack special effect -- based on table at c2/3dcd
            asm.PHA(),
            asm.JSR(0x387e, asm.ABS), # Call special effect function once for value in 11a9
            asm.LDA(NEW_SPECIAL_EFFECT_VAR, asm.ABS),
            asm.CMP(0x1, asm.S), # does the custom match the original?
            asm.BEQ("SKIP_IT"),  # branch if so
            asm.STA(0x11a9, asm.ABS),
            asm.JSR(0x387e, asm.ABS), # Call special effect function again for our special effect var
            "SKIP_IT",
            asm.PLA(),
            asm.STA(0x11a9, asm.ABS),
            asm.PLP(),
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Capture Fix: new special effect function")
        new_special_effect_addr = space.start_address

        ##### 
        # Modify data in "Character Executes One Hit" function to use new subroutines and variable
        #####
        space = Reserve(0x23185, 0x23187, "Capture Fix: call new null dog block subroutine")#, asm.NOP())
        space.write(
            asm.JSR(null_dog_block_addr, asm.ABS) #(Null Dog block, then clear my custom special effect
                                                   # variable for Capture)
        )
        space = Reserve(0x231b0, 0x231b2, "Capture Fix: Save Special Effect to new byte")
        space.write(
            asm.STA(NEW_SPECIAL_EFFECT_VAR, asm.ABS) #save special effect in our fancy new byte, so we won't
                                                     # overwrite the weapon's special effect.
        )
        space = Reserve(0x2345c, 0x2345e, "Capture Fix: call new special effect function")
        space.write(
            asm.JSR(new_special_effect_addr, asm.ABS) #Special effect code for target .. customized
        )

        ####
        # Dice Effect
        ####
        # FF6WC note: Rather than transfering Assassin's extensive changes made to the Dice Effect subroutine (C2/4168 - C2/41E5),
        #  which were seemingly made just to save space, I'm just transfering the main change as a subroutine:
        #  replacing the Capture animation with Dice with that of Fight starting at C2/41D9
        src = [ 
            asm.A8(),                 # Set 8 bit accumulator
            asm.LDA(0xb5, asm.DIR),   # Load Command Index
            asm.CMP(0x00, asm.IMM8),  # Maybe unnecessary? Compare Command with Fight
            asm.BEQ("SET_ANIMATION"), # Branch if Fight command
            asm.CMP(0x06, asm.IMM8),  # Compare Command with Capture
            asm.BNE("NO_CHANGE"),     # Branch if not Capture command
            "SET_ANIMATION",
            asm.LDA(0x26, asm.IMM8),
            asm.STA(0xb5, asm.DIR),   # Store a dice toss animation
            "NO_CHANGE",
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Capture Fix: new dice toss animation")
        dice_toss_animation_addr = space.start_address

        space = Reserve(0x241d9, 0x241e5, "Capture Fix: replace dice toss animation", asm.NOP())
        space.write(
            asm.JSR(dice_toss_animation_addr, asm.ABS), #Jump to our new routine
            asm.RTS()                                   #Done
        )

