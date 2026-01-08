from ..memory.space import Reserve
from ..instruction import asm as asm
from .. import args as args

class EnemyDamageCounter:
    def __init__(self):
        if args.fix_enemy_damage_counter:
            self.mod()

    def mod(self):
        # masterzed, https://masterzed.cavesofnarshe.com/ff3.html
        #
        # on the first attack, the fc 05 enemy ai conditional only triggers if the attack reduces hp
        # after the first attack, the condition will always trigger because $327c is not reset back to 0xff
        # fix the fc 05 conditional to only trigger if the enemy's hp is reduced by an attack
        space = Reserve(0x21c76, 0x21c7d, "enemy damage counter bug fix", asm.NOP())
        space.add_label("LOAD_ATTACKER_MASK", 0x21c55)
        space.write(
            asm.LDA(0xff, asm.IMM8),
            asm.STA(0x327c, asm.ABS_X),     # reset last character/enemy to do damage
            asm.BRA("LOAD_ATTACKER_MASK"),  # branch to original code
        )
