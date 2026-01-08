from ..data import enemy_script_commands as ai_instr

# parse until EndMainLoop or EndScript instructions found
def parse_section(script, index, InstructionTypes):
    blocks = [[]] # stack of instruction blocks
    instructions = []

    while True:
        instruction = None
        try:
            for InstructionType in InstructionTypes:
                if script[index] == InstructionType.OPCODE:
                    instruction = InstructionType(*script[index + 1 : index + InstructionType.SIZE])
                    index += len(instruction)
                    break
        except IndexError:
            # missing end statement, return instructions found
            return (index, blocks[0])

        if not instruction:
            instruction = ai_instr.Spell(script[index])
            index += len(instruction)

        instructions.append(instruction)
        if type(instruction) is ai_instr.EndMainLoop or type(instruction) is ai_instr.EndScript:
            break

    return (index, instructions)

def parse_script(script):
    CommonInstructionTypes = [ai_instr.RandomAttack, ai_instr.SetTarget, ai_instr.SetFormation, ai_instr.Message, ai_instr.RandomCommand, ai_instr.ChangeEnemies, ai_instr.RandomItem, ai_instr.Event, ai_instr.Arithmetic, ai_instr.Bits, ai_instr.Animate, ai_instr.Misc, ai_instr.If, ai_instr.EndTurn, ai_instr.EndIf]

    MainLoopInstructionTypes = CommonInstructionTypes + [ai_instr.EndMainLoop]
    CallbackInstructionTypes = CommonInstructionTypes + [ai_instr.EndScript]

    index, main_loop_instructions = parse_section(script, 0, MainLoopInstructionTypes)
    index, callback_instructions = parse_section(script, index, CallbackInstructionTypes)

    return main_loop_instructions + callback_instructions
