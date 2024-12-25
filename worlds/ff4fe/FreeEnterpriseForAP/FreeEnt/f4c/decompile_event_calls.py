from . import ff4struct
from . import decompile_common
from . import event_common

def decompile_event_call(encoded_event_call, block_parameters=None, map_messages=None):
    lines = []

    if block_parameters:
        lines.append("eventcall({})".format(block_parameters))
        lines.append("{")
    else:
        lines.append("eventcall {")

    if encoded_event_call:
        event_call = ff4struct.event_call.decode(encoded_event_call)

        for case in event_call.cases:
            event_name = decompile_common.value_text(case.event, 'event')
            event_description = event_common.DEFAULT_EVENT_DESCRIPTIONS[case.event]
            if map_messages:
                #if case.event >= 0x01 and case.event <= 0x03:
                #    # in vanilla FF4 these events display messages from event call params
                #    event_description += ' - "{}"'.format(map_messages[event_call.parameters[case.event - 1]])
                if case.event >= 0x27 and case.event <= 0x2E:
                    # in vanilla FF4 these events display map messages
                    event_description += ' - "{}"'.format(map_messages[case.event - 0x27])

            if case.conditions:
                conditions = []
                for c in case.conditions:
                    flag_name = decompile_common.value_text(c.flag, 'flag')
                    if c.value:
                        conditions.append(flag_name)
                    else:
                        conditions.append('not {}'.format(flag_name))

                conditions = ', '.join(conditions)
                lines.append("    if {}:".format(conditions))
                lines.append("        {}   //{}".format(event_name, event_description))
            else:
                if len(event_call.cases) > 1:
                    lines.append("    else:")
                    lines.append("        {}   //{}".format(event_name, event_description))
                else:
                    lines.append("    {}   //{}".format(event_name, event_description))

        if event_call.parameters:
            lines.append('    messages:')
            for m in event_call.parameters:
                if map_messages and m < len(map_messages):
                    lines.append('        ${:02X}   // "{}"'.format(m, map_messages[m]))
                else:
                    lines.append('        ${:02X}'.format(m))

    lines.append('}')
    return '\n'.join(lines)


def decompile_event_calls(rom):
    lines = []
    for i,encoded_event_call in enumerate(rom.event_calls):
        if not encoded_event_call:
            continue

        lines.append(decompile_event_call(encoded_event_call, "${:02X}".format(i)))
        lines.append('')

    return "\n".join(lines)
