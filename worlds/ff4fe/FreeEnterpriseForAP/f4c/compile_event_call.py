from . import consts
from . import compile_common
from . import ff4struct

def compile_event_call(body):
    tree = compile_common.parse(body, 'event_call', 'eventcall_block_body')
    if not tree.children:
        return []

    event_call = ff4struct.event_call.EventCall()
    for node in tree.children:
        if node.data == 'messages':
            event_call.parameters.extend(node.children)
        else:
            case = ff4struct.event_call.EventCallCase()
            for condition in node.children[:-1]:
                condition = ff4struct.event_call.EventCallCondition(
                    flag = condition.children[0], 
                    value = (False if condition.data == 'not_condition' else True)
                    )
                case.conditions.append(condition)
            case.event = node.children[-1]
            event_call.cases.append(case)

    return event_call.encode()


def process_eventcall_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'event_call', 'eventcall_block_params')
    encoded_event_call = compile_event_call(block['body'])
    rom.event_calls[params_tree.children[0]] = encoded_event_call

if __name__ == "__main__":
    test = compile_event_call('''
            if not $22, $33:
                $19
            if not $44:
                $18
            else:
                $00
        ''')
    print(' '.join(['{:02X}'.format(x) for x in test]))
