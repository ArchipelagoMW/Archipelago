# This is a simplified rewrite of the FlagSet 
# utility class core functionality, for the purpose 
# of being transpiled into JS using javascripthon.
# As such, the following Python language features
# should be avoided:
#  - imports
#  - named built-in methods of objects
# Access to more advanced features should be provided
# through the lib object passed to FlagSetCore.

class FlagSetCore:
    # flagspec is a dictionary object that is generated
    #   by compile_flags.py for both Python and JS, and
    #   must be passed to the object on creation since
    #   they are not part of this transpiled file.
    # lib is an object exposing various utility functions,
    #   in order to abstract away that they cannot be
    #   transpiled directly:
    #     b64encode(array_of_byte_values)
    #     b64decode(string)
    #     re_test(expression, string)
    #       -> returns true/false
    #     re_search(expression, string)
    #       -> returns list of match groups, or null if no match
    #     re_sub(expression, replacement, string)
    #     push(list, value)
    #     remove(list, value)
    #     join(list, separator)
    #     min(a, b)
    #     is_string(obj)
    #     keys(dict)
    def __init__(self, flagspec, lib):
        self._flagspec = flagspec
        self._lib = lib
        self._flags = {}
        self._embedded_version = None

    def load(self, flag_string):
        self._load_text(flag_string)

    def _load_text(self, flag_string):
        self._flags = {}
        self._embedded_version = None
        index = 0
        superflag = None
        flag_string = self._lib.re_sub(r'\s', '', flag_string)

        while len(flag_string) > 0:
            m = self._lib.re_search(r'^[A-Z]', flag_string)
            if m:
                superflag = m[0]
                flag_string = flag_string[len(superflag):]
                continue

            m = self._lib.re_search(r'^-[a-z0-9_]+:?', flag_string)
            if m:
                superflag = m[0]
                flag_string = flag_string[len(superflag):]
                if not self._lib.re_test(r'\:$', superflag):
                    self.set(superflag)
                continue

            m = self._lib.re_search(r'^([a-z0-9_]+:)?([a-z0-9_]+(,[a-z0-9_]+)*)/?', flag_string)
            if m:
                if superflag is None:
                    raise Exception(f"Parse error: found subflag without superflag around '{m[0]}'")
                subflag_prefix = (m[1] if m[1] else '')
                subflags = m[2].split(',')
                for i in range(len(subflags)):
                    self.set(superflag + subflag_prefix + subflags[i])
                flag_string = flag_string[len(m[0]):]
                continue

            raise Exception(f"Parse error around '{flag_string}'")


    def get_list(self, regex=None):
        flags = []
        for flag in self._flagspec['order']:
            if self.has(flag):
                if regex is None or self._lib.re_test(regex, flag):
                    self._lib.push(flags, flag)
        return flags

    def get_suffix(self, flag_prefix):
        flag_regex = '^' + flag_prefix
        flags = self.get_list(flag_regex)
        if len(flags) > 0:
            return flags[0][len(flag_prefix):]
        else:
            return None

    def get_version(self):
        return self._embedded_version
        
    def has(self, flag):
        if flag not in self._flagspec['order']:
            raise Exception(f"Invalid flag {flag}")

        if flag in self._flagspec['implicit']:
            return self._evaluate_condition(self._flagspec['implicit'][flag])
        elif flag in self._flags:
            return True
        else:
            return False

    def has_any(self, *flags):
        for flag in flags:
            if self.has(flag):
                return True
        return False

    def has_all(self, *flags):
        for flag in flags:
            if not self.has(flag):
                return False
        return True

    def set(self, flag):
        if flag in self._flagspec['implicit']:
            # Cannot set implicit flags
            return

        for mutex_set in self._flagspec['mutex']:
            if flag in mutex_set:
                for other_flag in mutex_set:
                    if other_flag != flag:
                        self.unset(other_flag)
                break

        self._flags[flag] = True

    def unset(self, flag):
        if flag in self._flags:
            del self._flags[flag]

    def parse(self):
        results = []
        for flag in self._flagspec['order']:
            if not self.has(flag):
                continue

            if flag[0] == '-':
                m = self._lib.re_search(r'^(-[a-z0-9_]+:?)([a-z0-9_]+)?$', flag)
                superflag = m[1]
                subflag = m[2]
                subsubflag = None
            else:
                m = self._lib.re_search(r'^([A-Z])(([a-z0-9_]+:)?([a-z0-9_]+))?$', flag)
                superflag = m[1]
                subflag = (m[3] if m[3] else m[4])
                subsubflag = (m[4] if m[3] else None)

            superflag_obj = None
            for item in results:
                if item[0] == superflag:
                    superflag_obj = item
                    break
            if not superflag_obj:
                superflag_obj = [superflag, []]
                self._lib.push(results, superflag_obj)

            if subflag:
                subflag_obj = None
                for item in superflag_obj[1]:
                    if item[0] == subflag:
                        subflag_obj = item
                        break
                if not subflag_obj:
                    subflag_obj = [subflag, []]
                    self._lib.push(superflag_obj[1], subflag_obj)

                if subsubflag:
                    self._lib.push(subflag_obj[1], subsubflag)

        return results

    def _evaluate_condition(self, condition):
        if self._lib.is_string(condition):
            return self.has(condition)
        elif condition[0] == 'not':
            return not self._evaluate_condition(condition[1])
        elif condition[0] == 'and':
            for subcondition in condition[1:]:
                if not self._evaluate_condition(subcondition):
                    return False
            return True
        elif condition[0] == 'or':
            for subcondition in condition[1:]:
                if self._evaluate_condition(subcondition):
                    return True
            return False
        else:
            raise Exception(f"Unsupported condition type {condition[0]}")

    def _wrap(self, text, first_line_width, paragraph_width):
        line_width = first_line_width
        lines = []
        while len(text) > line_width:
            break_index = line_width
            for i in range(line_width - 1, -1, -1):
                if text[i] == ',' or text[i] == ')' or text[i] == ' ':
                    break_index = i + 1
                    break

            self._lib.push(lines, text[:break_index])
            text = text[break_index:]
            line_width = paragraph_width

        if len(text) > 0:
            self._lib.push(lines, text)

        return lines


    def to_string(self, pretty=False, wrap_width=None):
        parsed = self.parse()

        # in pretty mode, parts is the components of the current line being built
        # in not pretty mode, parts is the components of the full complete string
        parts = []

        # in pretty mode, as parts is converted into lines, they are added here
        lines = []

        last_superflag = None
        for superflag_obj in parsed:
            if not pretty and len(parts) > 0:
                self._lib.push(parts, ' ')
            elif pretty and len(lines) > 0 and last_superflag[0] != '-':
                self._lib.push(lines, '')

            superflag = superflag_obj[0]
            last_superflag = superflag
            superflag_last_index = len(superflag) - 1 # needed to workaround https://github.com/metapensiero/metapensiero.pj/issues/78
            superflag_prefix = superflag + (' ' if pretty and superflag[superflag_last_index] != ':' else '')
            self._lib.push(parts, superflag_prefix)

            if len(superflag_obj[1]) > 0:
                if superflag[0] == '-':
                    # for subflags of -switch style flags, we want them to be
                    # rendered in one comma-separated parentheses, so create
                    # an object with a blank subflag and with the original subflag
                    # list as subsubflags
                    subsubflags = []
                    for subflag_obj in superflag_obj[1]:
                        self._lib.push(subsubflags, subflag_obj[0])
                    subflag_obj_list = [ ['', subsubflags] ]
                else:
                    subflag_obj_list = superflag_obj[1]

                subflag_obj_index = 0
                for subflag_obj in subflag_obj_list:
                    if pretty and len(parts) == 0:
                        # indent new line
                        self._lib.push(parts, ' /')

                    segment = subflag_obj[0] + self._lib.join(subflag_obj[1], ',')
                    if pretty:
                        self._lib.push(parts, segment)
                        paragraph_indent = '   '
                        line = self._lib.join(parts, '')
                        if wrap_width is None:
                            sublines = [line]
                        else:
                            sublines = self._wrap(line, wrap_width, wrap_width - len(paragraph_indent))

                        prefix = ''
                        for subline in sublines:
                            self._lib.push(lines, prefix + subline)
                            prefix = paragraph_indent

                        parts = []
                    else:
                        if subflag_obj_index > 0:
                            self._lib.push(parts, '/')
                        self._lib.push(parts, segment)

                    subflag_obj_index += 1

            elif pretty:
                self._lib.push(lines, parts[0])
                parts = []

        if not pretty:
            line = self._lib.join(parts, '')
            if wrap_width is not None:
                line = self._lib.join(self._wrap(line, wrap_width, wrap_width), '\n')
            return line
        else:
            return self._lib.join(lines, '\n')


    def to_binary(self):
        byte_list = []
        for i in range(3):
            self._lib.push(byte_list, self._flagspec['version'][i])

        for flag_binary_info in self._flagspec['binary']:
            if not self.has(flag_binary_info['flag']):
                continue

            value = flag_binary_info['value']
            field_size = flag_binary_info['size']
            byte_index = (flag_binary_info['offset'] >> 3) + 3  # +3 to account for version bytes
            bit_index = (flag_binary_info['offset'] & 0x7)
            #print(f"{flag_binary_info['flag']:20} : {value}[{field_size}] @ {flag_binary_info['offset']} -> {byte_index}.{bit_index}")

            while field_size > 0:
                while byte_index >= len(byte_list):
                    self._lib.push(byte_list, 0)

                dst_byte = byte_list[byte_index]
                subfield_size = self._lib.min(field_size, 8 - bit_index)
                subvalue = value & ((1 << subfield_size) - 1)
                #print(f"  Apply {subvalue << bit_index:02X} to byte {byte_index}")
                byte_list[byte_index] = dst_byte | (subvalue << bit_index)

                value >>= subfield_size
                field_size -= subfield_size
                bit_index = 0
                byte_index += 1

        return 'b' + self._lib.b64encode(byte_list)


#----------------------------------------------------------------------------------------

# This class handles flagset verification and correction.

class FlagLogicCore:
    def __init__(self, flagspec, lib):
        self._flagspec = flagspec
        self._lib = lib

    def _simple_disable(self, flagset, log, prefix, flags_to_disable):
        for flag in flags_to_disable:
            if flagset.has(flag):
                flagset.unset(flag)
                self._lib.push(log, ['correction', prefix + '; removed ' + flag])

    def _simple_disable_regex(self, flagset, log, prefix, flags_regex):
        self._simple_disable(flagset, log, prefix, flagset.get_list(flags_regex))

    # alters the flagset in place
    # returns a list of 2-tuples describing errors found and fixes made:
    #             [ <cleanup | correction | error>, <string describing fix> ]
    def fix(self, flagset):
        log = []

        # NOTE: mutex flags ARE handled internally by FlagSet, don't worry about them here

        # key item flags
        if flagset.has_any('Ksummon', 'Kmoon', 'Kmiab') and not flagset.has('Kmain'):
            flagset.set('Kmain')
            self._lib.push(log, ['correction', 'Advanced key item randomizations are enabled; forced to add Kmain'])

        if flagset.has('Kvanilla'):
            self._simple_disable(flagset, log, 'Key items not randomized', ['Kunsafe'])

        if flagset.has('Cvanilla'):
            self._simple_disable_regex(flagset, log, 'Characters not randomized', r'^C(maybe|distinct:|only:|no:)')
        else:
            only_flags = flagset.get_list(r'^Conly:')
            if len(only_flags) > 0:
                self._simple_disable_regex(flagset, log, 'Conly:* flag(s) are specified', r'^Cno:')

        if flagset.has('Chero'):
            self._simple_disable_regex(flagset, log, 'Hero challenge includes smith weapon', r'^-smith:')

        start_include_flags = flagset.get_list(r'^Cstart:(?!not_)')
        start_exclude_flags = flagset.get_list(r'^Cstart:not_')
        if len(start_exclude_flags) > 0 and len(start_include_flags) > 0:
            self._simple_disable_regex(flagset, log, 'Inclusive Cstart:* flags are specified', r'^Cstart:not_')
        if len(start_include_flags) > 1 and flagset.has('Cstart:any'):
            self._simple_disable_regex(flagset, log, 'Cstart:any is specified', r'^Cstart:(?!any|not_)')

        if flagset.has('Tempty'):
            self._simple_disable_regex(flagset, log, 'Treasures are empty', r'^Tsparse:')

        if flagset.has_any('Tempty', 'Tvanilla', 'Tshuffle'):
            self._simple_disable_regex(flagset, log, 'Treasures are not random', r'^Tmaxtier:')

        if flagset.has_any('Svanilla', 'Scabins', 'Sempty'):
            self._simple_disable_regex(flagset, log, 'Shops are not random', r'^Sno:([^j]|j.)')
            self._simple_disable(flagset, log, 'Shops are not random', ['Sunsafe'])

        if flagset.has('Sshuffle'):
            self._simple_disable(flagset, log, 'Shops are only shuffled', ['Sno:life'])

        if flagset.has('Bvanilla'):
            self._simple_disable(flagset, log, 'Bosses not randomized', ['Bunsafe'])

        if flagset.has('Evanilla'):
            self._simple_disable(flagset, log, 'Encounters are vanilla', ['Ekeep:behemoths', 'Ekeep:doors', 'Edanger'])

        all_spoiler_flags = flagset.get_list(r'^-spoil:')
        sparse_spoiler_flags = flagset.get_list(r'^-spoil:sparse')
        if (len(all_spoiler_flags) > 0 and len(all_spoiler_flags) == len(sparse_spoiler_flags)):
            self._simple_disable_regex(flagset, log, 'No spoilers requested', r'^-spoil:sparse')

        # Objectives logic
        if flagset.has('Onone'):
            self._simple_disable_regex(flagset, log, 'No objectives set', r'^O(win|req):')
        else:
            # Force Oreq:all if a req: flag is not specified
            if not flagset.get_list(r'^Oreq:'):
                flagset.set('Oreq:all')
                self._lib.push(log, ['correction', 'Required number of objectives not specified; setting Oreq:all'])

            win_flags = flagset.get_list(r'^Owin:')
            # Force Owin:crystal if classicforge, otherwise force Owin:game if no win result specified
            if flagset.has('Omode:classicforge') and not flagset.has('Owin:crystal'):
                flagset.set('Owin:crystal')
                self._lib.push(log, ['correction', 'Classic Forge is enabled; forced to add Owin:crystal'])
            elif len(win_flags) == 0:
                flagset.set('Owin:game')
                self._lib.push(log, ['correction', 'Objectives set without outcome specified; added Owin:game'])

            # force Pkey if pass objective is set
            pass_quest_flags = flagset.get_list(r'^O\d+:quest_pass$')
            if len(pass_quest_flags) > 0 and flagset.has('Pnone'):
                flagset.set('Pkey')
                self._lib.push(log, ['correction', 'Pass objective is set without a pass flag; forced to add Pkey'])

            # check for conflict between objective required characters and available ones
            char_objective_flags = flagset.get_list(r'^O\d+:char_')
            if len(char_objective_flags) > 0:
                required_chars = []
                for f in char_objective_flags:
                    ch = self._lib.re_sub(r'^O\d+:char_', '', f)
                    self._lib.push(required_chars, ch)

                if flagset.has('Cvanilla'):
                    has_unavailable_characters = False
                    if 'cecil' in required_chars:
                        has_unavailable_characters = True
                    elif (flagset.has('Cnofree')):
                        if 'edward' in required_chars or 'tellah' in required_chars or 'palom' in required_chars or 'porom' in required_chars:
                            has_unavailable_characters = True
                    elif (flagset.has('Cnoearned')):
                        if 'rydia' in required_chars or 'kain' in required_chars or 'rosa' in required_chars or 'yang' in required_chars or 'cid' in required_chars or 'edge' in required_chars or 'fusoya' in required_chars:
                            has_unavailable_characters = True

                    if has_unavailable_characters:
                        self._lib.push(log, ['error', "Character objectives are set for characters that cannot be found in vanilla character assignment"])
                else:
                    only_flags = flagset.get_list(r'^Conly:')
                    pool = []
                    if len(only_flags) > 0:
                        for f in only_flags:
                            ch = self._lib.re_sub(r'^Conly:', '', f)
                            self._lib.push(pool, ch)
                    else:
                        pool = ['cecil', 'kain', 'rydia', 'edward', 'tellah', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya']
                        for f in flagset.get_list(r'^Cno:'):
                            ch = self._lib.re_sub(r'^Cno:', '', f)
                            self._lib.remove(pool, ch)

                    for ch in required_chars:
                        if ch not in pool:
                            self._lib.push(log, ['error', "Character objectives are set for characters excluded from the randomization."])
                            break

                    distinct_flags = flagset.get_list(r'^Cdistinct:')
                    if len(distinct_flags) > 0:
                        distinct_count = int(self._lib.re_sub(r'^Cdistinct:', '', distinct_flags[0]))
                        if distinct_count < len(required_chars):
                            self._lib.push(log, ['error', "More character objectives are set than distinct characters allowed in the randomization."])

                if flagset.has('Cnofree') and flagset.has('Cnoearned'):
                    self._lib.push(log, ['error', "Character objectives are set while no character slots will be filled"])

            if flagset.has('Orandom:char') and flagset.has('Cnoearned') and flagset.has('Cnofree'):
                flagset.unset('Orandom:char')
                self._lib.push(log, ['correction', 'Random character objectives in the pool while no character slots will be filled. Removed Orandom:char.'])
                    
            # remove random quest type specifiers if no random objectives specified
            if not flagset.get_list(r'^Orandom:\d'):
                self._simple_disable_regex(flagset, log, 'No random objectives specified', r'^Orandom:[^\d]')

        return log


