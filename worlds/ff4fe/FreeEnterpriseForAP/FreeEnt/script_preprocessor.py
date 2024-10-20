import re

from .errors import BuildError

_SUBSTITUTION_DELIMITER_REGEX = re.compile(r'\s*//\s*%(?P<identifier>[^%]*)%\s*$')
_LEGACY_FLAG_REGEX = re.compile(r'^\s*flag\s+(?P<flag>[A-Za-z0-9_]+)\s+(?P<state>on|off)\s*$')
_LEGACY_MULTIFLAG_REGEX = re.compile(r'^\s*flags:(?P<flags>.*)$')
_LEGACY_TEST_REGEX = re.compile(r'^\s*test_setting\s*(?P<setting>.+?)\s*$')
_INLINE_SUBSTITUTION_REGEX = re.compile(r'\{%(?P<identifier>.+?)(?P<default>:.*?)?%\}')

_KEYWORDS = ['if', 'elif', 'else', 'flag', 'flags:', 'test_setting', 'end']


class _PreprocessState:
    def __init__(self):
        self.is_blanking = False
        self.is_substitution_open = False
        self.is_conditional_open = False
        self.is_conditional_already_satisfied = False
        self.is_conditional_ending = False

class ScriptPreprocessor:
    def __init__(self, env):
        self._env = env

    def inline_substitution_func(self, m):
        identifier = m.group('identifier').strip()
        if identifier in self._env.substitutions:
            return self._env.substitutions[identifier]
        elif m.group('default') is not None:
            return m.group('default')[1:].strip()
        else:
            raise BuildError(f"Inline substitution {identifier} has no value or default value specified.")
        
    def preprocess(self, script):
        src_lines = script.split('\n')
        lines = []

        state = _PreprocessState()
        for line_number,line in enumerate(src_lines):
            def get_error_context():
                return '\n'.join(src_lines[max(0, line_number - 2):(line_number + 3)])
            
            line += '\n'

            delimiter_match = _SUBSTITUTION_DELIMITER_REGEX.search(line)
            if delimiter_match:
                identifier = delimiter_match.group('identifier').strip()

                if identifier.split(maxsplit=1)[0] in _KEYWORDS:
                    try:
                        self.handle_keyword_identifier(identifier, state)
                    except BuildError as e:
                        raise BuildError(f"{str(e)}; context:\n{get_error_context()}")

                elif identifier in self._env.substitutions:
                    # direct substitution by exact name match
                    substitution_value = self._env.substitutions[identifier]
                    state.is_substitution_open = True
                    state.is_blanking = True
                    lines.append(substitution_value)
                    if not substitution_value.endswith('\n'):
                        lines.append('\n')
                else:
                    # no match; allow existing text to continue
                    state.is_substitution_open = True
                    state.is_blanking = False


            elif not state.is_blanking:
                if '{%' in line:
                    line = _INLINE_SUBSTITUTION_REGEX.sub(self.inline_substitution_func, line)
                lines.append(line)
        
        return ''.join(lines)

    def handle_keyword_identifier(self, identifier, state):
        identifier_parts = identifier.split(maxsplit=1)
        keyword = identifier_parts[0]

        if keyword == 'end':
            if not state.is_substitution_open:
                raise BuildError(f"Encountered %end% while not inside substitution")
            state.is_blanking = False
            state.is_substitution_open = False
            state.is_conditional_open = False
            state.is_conditional_ending = False
            return

        if keyword == 'else':
            if (not state.is_conditional_open) or state.is_conditional_ending:
                raise BuildError(f"Encountered unexpected conditional keyword %{identifier}%")
            state.is_substitution_open = True
            state.is_blanking = state.is_conditional_already_satisfied
            state.is_conditional_ending = True
            return

        # Convert legacy conditional formats to "if" format
        if keyword == 'flag':
            m = _LEGACY_FLAG_REGEX.search(identifier)
            if not m:
                raise BuildError(f"Encountered malformed keyword identifier %{identifier}%")
            flag = m.group('flag')
            compare = (m.group('state') == 'on')
            keyword = 'if'
            identifier_parts = [keyword, 'flags: ' + ('' if compare else '~') + flag]
        elif keyword == 'flags:':
            m = _LEGACY_MULTIFLAG_REGEX.search(identifier)
            if not m:
                raise BuildError(f"Encountered malformed keyword identifier %{identifier}%")
            keyword = 'if'
            identifier_parts = [keyword, identifier]
        elif keyword == 'test_setting':
            m = _LEGACY_TEST_REGEX.search(identifier)
            if not m:
                raise BuildError(f"Encountered malformed keyword identifier %{identifier}%")
            keyword = 'if'
            identifier_parts = [keyword, f"test: {m.group('setting')}"]
        
        if keyword in ['if', 'elif']:
            if state.is_conditional_ending or (keyword == 'if' and state.is_substitution_open) or (keyword == 'elif' and not state.is_conditional_open):
                raise BuildError(f"Encountered unexpected conditional keyword %{identifier}%")

            state.is_substitution_open = True
            state.is_conditional_open = True
            state.is_conditional_ending = False

            if keyword == 'if':
                state.is_conditional_already_satisfied = False
            
            if state.is_conditional_already_satisfied:
                state.is_blanking = True
            else:
                condition_string = identifier_parts[1].strip()
                condition_satisfied = False
                if condition_string.startswith('flags:'):
                    flags = condition_string.split(':', maxsplit=1)[1].strip().split()
                    all_matched = True
                    for flag in flags:
                        if flag.startswith('~'):
                            all_matched = (all_matched and not self._env.options.flags.has(flag[1:]))
                        else:
                            all_matched = (all_matched and self._env.options.flags.has(flag))
                    condition_satisfied = all_matched
                elif condition_string.startswith('test:'):
                    setting = condition_string.split(':', maxsplit=1)[1].strip()
                    condition_satisfied = self._env.options.test_settings.get(setting, False)
                else:
                    toggle = condition_string
                    if toggle.startswith('~'):
                        condition_satisfied = (not self._env.toggles.get(toggle[1:], False))
                    else:
                        condition_satisfied = self._env.toggles.get(toggle, False)

                if condition_satisfied:
                    state.is_blanking = False
                    state.is_conditional_already_satisfied = True
                else:
                    state.is_blanking = True
