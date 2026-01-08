from ...objectives.results._objective_result import *
from ...objectives.results._apply_characters_party import ApplyToParty
from ...instruction.field import entity as field_entity

class Field(field_result.Result):
    def src(self):
        status_effects = field.Status.DARKNESS | field.Status.POISON | field.Status.IMP
        return [
            field.AddStatusEffects(field_entity.PARTY0, status_effects),
            field.AddStatusEffects(field_entity.PARTY1, status_effects),
            field.AddStatusEffects(field_entity.PARTY2, status_effects),
            field.AddStatusEffects(field_entity.PARTY3, status_effects),
        ]

class Battle(battle_result.Result):
    def src(self):
        character_status_start = 0x1614
        effect_mask = 0x25

        return ApplyToParty([
            asm.LDA(character_status_start, asm.ABS_Y), # load character's current status effect bits
            asm.ORA(effect_mask, asm.IMM8),             # apply sour mouth status effects
            asm.STA(character_status_start, asm.ABS_Y), # save status effects
        ])

class Result(ObjectiveResult):
    NAME = "Sour Mouth"
    def __init__(self):
        super().__init__(Field, Battle)
