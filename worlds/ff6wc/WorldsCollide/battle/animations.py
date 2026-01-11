from ..memory.space import Bank, Reserve, Read, Write
from ..data import battle_animation_scripts as battle_animation_scripts
from ..instruction import asm as asm
from .. import args as args

class Animations:
    def __init__(self):
        self.health_animation_reflect_mod()
        self.stray_flash_mod()

        # Flash removal
        replace_flash_animation = [] # The background flash to replace with monster flashes
        remove_flash_animation = [] # The background flash addresses to remove

        if args.flashes_remove_most:
            # Replace Boss Death and Final Kefka
            replace_flash_animation.extend(["Boss Death", "Final KEFKA Death"])
            # And remove the rest
            remove_flash_animation.extend(battle_animation_scripts.BATTLE_ANIMATION_FLASHES.keys())
            # Also removing critical flash
            self.remove_critical_flash()
        elif args.flashes_remove_worst:
            replace_flash_animation.extend(["Boss Death"])
            remove_flash_animation.extend(["Ice 3", "Fire 3", "Bolt 3", "Schiller", "R.Polarity", "X-Zone",
                               "Muddle", "Dispel", "Shock", "Bum Rush", "Quadra Slam", "Slash", "Flash", 
                               "Step Mine", "Rippler", "WallChange", "Ultima", "ForceField"])

        # Replace any specified above
        flash_address_arrays = [battle_animation_scripts.BATTLE_ANIMATION_FLASHES[name] for name in replace_flash_animation]
        if flash_address_arrays:
            self.replace_bg_flash_with_monster_flash_mod(flash_address_arrays)
        
        # Remove any remainder specified above
        flash_address_arrays = [battle_animation_scripts.BATTLE_ANIMATION_FLASHES[name] for name in remove_flash_animation if name not in replace_flash_animation]
        if flash_address_arrays:
            self.remove_battle_flashes_mod(flash_address_arrays)

    def remove_critical_flash(self):
        space = Reserve(0x23410, 0x23413, "Critical hit screen flash", asm.NOP())

    def replace_bg_flash_with_monster_flash_mod(self, flash_address_arrays):
        REPLACEMENTS = {
            0xAF: 0xB9, # Set background palette color subtraction (absolute) -> Set monster palettes color subtraction (absolute)
            0xB0: 0xBA, # Set background palette color addition (absolute) -> Set monster palettes color addition (absolute)
            0xB5: 0xBB, # Add color to background palette (relative) -> Add color to monster palettes (relative)
            0xB6: 0xBC, # Subtract color from background palette (relative) -> Subtract color from monster palettes (relative)
        }
        for flash_addresses in flash_address_arrays:
            # For each address in its array
            for flash_address in flash_addresses:
                # Read the current animation command at the address
                animation_cmd = Read(flash_address, flash_address+1)
                if(animation_cmd[0] in REPLACEMENTS.keys()):
                    Write(flash_address, REPLACEMENTS[animation_cmd[0]], "BG flash to monster flash")
                else:
                    # This is an error, reflecting a difference between the disassembly used to generate BATTLE_ANIMATION_FLASHES and the ROM
                    raise ValueError(f"Battle Animation Script Command at 0x{flash_address:x} (0x{animation_cmd[0]:x}) did not match an expected value.")

    def remove_battle_flashes_mod(self, flash_address_arrays):
        ABSOLUTE_CHANGES = [0xb0, 0xaf]
        RELATIVE_CHANGES = [0xb5, 0xb6]
        # For each battle animation command
        for flash_addresses in flash_address_arrays:
            # For each address in its array
            for flash_address in flash_addresses:
                # Read the current animation command at the address
                animation_cmd = Read(flash_address, flash_address+1)
                if(animation_cmd[0] in ABSOLUTE_CHANGES):
                    # This is an absolute color change. To remove flashing effects, set the value to E0 to cause no background change
                    Write(flash_address+1, 0xE0, "Background color change (absolute)")
                elif(animation_cmd[0] in RELATIVE_CHANGES):
                    # This is a relative color change. To remove flash effects, set the value to F0 to cause no background change
                    Write(flash_address+1, 0xF0, "Background color change (relative)")
                else:
                    # This is an error, reflecting a difference between the disassembly used to generate BATTLE_ANIMATION_FLASHES and the ROM
                    raise ValueError(f"Battle Animation Script Command at 0x{flash_address:x} (0x{animation_cmd[0]:x}) did not match an expected value.")

    def stray_flash_mod(self):
        # port of https://www.romhacking.net/hacks/6740/
        Write(0x10784b, 0xa7, "Flash tool position") #default: 0xaf

    def health_animation_reflect_mod(self):
        # Ref: https://www.ff6hacking.com/forums/thread-4145.html
        # Banon's Health command casts Cure 2 on the party with a unique animation.
        # Because the animation is unique, it has the step-forward component built into it.  
        # And because Cure 2 can be reflected, if the command hits a mirrored target it will bounce and make Banon step forward again.  
        # Note: this only occurs if the whole party doesn't have reflect, only a subset.
        # Used over and over, Banon can be made to walk completely off-screen.
        # 
        # Fix:
        # We tell the HEALTH animation to ignore block graphics, which prevents the reflect animation from playing.  
        # When encountering a reflection, the regular green Cure 2 animation will follow on the reflect recipient.
        src = [
            asm.INC(0x62C0, asm.ABS), #Makes the animation ignore blocking graphics
            asm.JSR(0xBC35, asm.ABS), #Call the subroutine that got displaced to inject the block override
            asm.RTS()
        ]
        space = Write(Bank.C1, src, "Health animation fix")
        jsrAddr = space.start_address

        # Replace the existing jump with one to our new service routine
        space = Reserve(0x1BB67, 0x1BB69, "Health animation JSR")
        space.write(asm.JSR(jsrAddr, asm.ABS))