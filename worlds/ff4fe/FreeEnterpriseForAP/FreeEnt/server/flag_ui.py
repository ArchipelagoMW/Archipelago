import re
import os
import json

class Section:
    def __init__(self):
        self.title = None
        self.items = []

class Item:
    def __init__(self):
        self.flag = None
        self.text = None
        self.type = None
        self.hide = False
        self.hard = False
        self.subsection = Section()

class CachedResult:
    def __init__(self, *src_files):
        self._mtimes = { p : None for p in src_files }
        self._result = None

    def is_valid(self):
        if self._result is None:
            return False

        for p in self._mtimes:
            if self._mtimes[p] is None:
                return False
            if os.path.getmtime(p) > self._mtimes[p]:
                return False

        return True

    def update_result(self, result):
        self._result = result
        for p in self._mtimes:
            self._mtimes[p] = os.path.getmtime(p)

    def get_result(self):
        return self._result

UISPEC_PATH = os.path.join(os.path.dirname(__file__), "uispec.txt")
UISPEC_FLAGDESCRIPTIONS_PATH = os.path.join(os.path.dirname(__file__), "uispec_flagdescriptions.txt")
UISPEC_PRESETS_PATH = os.path.join(os.path.dirname(__file__), "uispec_presets.txt")

_cached_section_data = CachedResult(UISPEC_PATH)
_cached_flag_html = CachedResult(UISPEC_PATH)
_cached_flag_descriptions = CachedResult(UISPEC_FLAGDESCRIPTIONS_PATH)
_cached_preset_json = CachedResult(UISPEC_PRESETS_PATH)

def _load_flag_descriptions():
    if _cached_flag_descriptions.is_valid():
        return

    flag_descriptions = {}
    with open(UISPEC_FLAGDESCRIPTIONS_PATH, 'r') as infile:
        cur_buffer = None
        for line in infile:
            m = re.search(r'^\s*\[(?P<flag>.+)\]\s*$', line)
            if m:
                cur_buffer = []
                flag_descriptions[m['flag']] = cur_buffer
            elif cur_buffer is not None:
                if line.strip():
                    cur_buffer.append(line.strip())

    for flag in flag_descriptions:
        flag_descriptions[flag] = '\n'.join([f'<p>{line}</p>' for line in flag_descriptions[flag]])

    _cached_flag_descriptions.update_result(flag_descriptions)

def _build_items_html(items, parent_id, indent=0):
    output_lines = []
    in_select = False

    flag_descriptions = _cached_flag_descriptions.get_result()

    for item in items:
        if item.type == 'select':
            if not in_select:
                in_select = True
                output_lines.append(f'<select id="control_select_{parent_id}">')
            output_lines.append(f'<option value="{item.flag}">{item.text}</option>')
            continue

        if in_select:
            in_select = False
            output_lines.append('</select>')

        if item.type == 'separator':
            #output_lines.append('<div class="separator"></div>')
            output_lines.append('</div><div class="flag-list">')
        else:
            if item.flag.startswith('@'):
                flag_display = '&#8230;'
            else:
                flag_display = item.flag

            class_name = ('hard' if item.hard else '')

            update_func = f"onControlChanged('{item.flag}');"

            if item.type == 'checkbox':
                output_lines.append(f'<input type="checkbox" id="control-{item.flag}" onchange="{update_func}">')
                output_lines.append(f'<label class="flag-checkbox {class_name}" for="control-{item.flag}">{flag_display}</label>')
            else:
                output_lines.append(f'<input type="radio" id="control-{item.flag}" name="control-radio-{parent_id}" value="{item.flag}" onchange="{update_func}">')
                output_lines.append(f'<label class="flag-radio-button {class_name}" for="control-{item.flag}">{flag_display}</label>')

            class_name = ('auto-hide' if item.hide else '')

            output_lines.append(f'<div class="flag-body {class_name}">')
            output_lines.append(f'  <label for="control-{item.flag}">{item.text}</label>')

            if item.flag in flag_descriptions and flag_descriptions[item.flag]:
                output_lines.append(f'  <div class="flag-details" id="flag-details-{item.flag}">')
                output_lines.append(flag_descriptions[item.flag])
                output_lines.append(f'  </div>')

            if item.subsection.items:
                output_lines.append(f'<div id="subsection-{item.flag}" class="flag-list">')
                output_lines.append(_build_items_html(item.subsection.items, item.flag, indent + 2))
                output_lines.append(f'</div>')

            output_lines.append(f'</div>')

    if in_select:
        in_select = False
        output_lines.append('</select>')

    return '\n'.join([(' ' * indent + line) for line in output_lines])

def _build_html():
    if _cached_flag_html.is_valid():
        return

    section_header_regex = re.compile(r'^\s*==\s*(?P<title>.*?)\s*$')
    widget_regex = re.compile(r'''
        ^\s*
        (?P<depth>\.*)
        (?P<widget>
            \[(@?[A-Za-z0-9!\-:]*)\]
           |\((@?[A-Za-z0-9!\-:]*)\)
           |\<([A-Za-z0-9!\-:]*)\>
        )
        (?P<nohide>\@?)
        (?P<hard>\!?)
        \s*
        (?P<text>.*?)
        \s*$
        ''', re.VERBOSE)

    widget_type_map = {
        '[' : 'checkbox',
        '(' : 'radio',
        '<' : 'select'
        }

    sections = []

    with open(UISPEC_PATH, 'r') as infile:
        section_stack = []
        anonymous_counter = 0
        pending_separator = False

        for line in infile:
            if not line.strip():
                pending_separator = True
                continue

            if line.strip().startswith('#'):
                # comment line, ignore
                continue

            m = section_header_regex.search(line)
            if m:
                new_section = Section()
                new_section.title = m.group('title')
                section_stack = [new_section]
                pending_separator = False
                sections.append(new_section)
                continue

            m = widget_regex.search(line)
            if m:
                depth = len(m.group('depth'))
                section_stack = section_stack[:depth + 1]

                if pending_separator:
                    separator = Item()
                    separator.type = 'separator'
                    section_stack[depth].items.append(separator)
                    pending_separator = False

                item = Item()
                item.flag = m.group('widget')[1:-1]
                if not item.flag:
                    item.flag = f"@{anonymous_counter}"
                    anonymous_counter += 1
                item.text = m.group('text')
                item.type = widget_type_map[m.group('widget')[0]]
                item.hide = not bool(m.group('nohide'))
                item.hard = bool(m.group('hard'))

                section_stack[depth].items.append(item)
                section_stack.append(item.subsection)

    _load_flag_descriptions()

    cached_results = {
        'sections' : sections,
        'controls_html' : _build_flag_controls_html(sections),
        'preview_html' : _build_flag_preview_html(sections)
    }

    _cached_flag_html.update_result(cached_results)

def _build_flag_controls_html(sections):
    # Step 1: build flag UI
    output_lines = []
    for i,section in enumerate(sections):
        output_lines.append('<div class="flag-section">')
        output_lines.append(f'  <h1>{ section.title }</h1>')
        output_lines.append('  <div class="flag-list">')
        output_lines.append(_build_items_html(section.items, f'section-{i}', 4))
        output_lines.append('  </div>')
        output_lines.append('</div>')

    flag_hierarchy = {}
    def _build_hierarchy(section, target_dict):
        for item in section.items:
            if item.flag is not None:
                target_dict[item.flag] = {}
                _build_hierarchy(item.subsection, target_dict[item.flag])

    for section in sections:
        _build_hierarchy(section, flag_hierarchy)

    output_lines.append('<script>')
    output_lines.append(f'  var FLAG_HIERARCHY = {json.dumps(flag_hierarchy)};')
    output_lines.append('</script>')

    return '\n'.join(output_lines)

def _build_flag_preview_html(sections):
    output_lines = []
    for section in sections:
        if section.title:
            slug = _section_to_slug(section.title)
            output_lines.append(f'<div id="SECTION_{slug}" class="section SECTION_{slug}_STATUS">')
            output_lines.append(f'<div class="title">{section.title}</div>')
        else:
            output_lines.append(f'<div class="section">')

        for item in section.items:
            if item.type == 'separator':
                continue

            description = _cached_flag_descriptions.get_result().get(item.flag, '')

            output_lines.append(f'<div class="flag_container FLAG_{item.flag}_STATUS" id="flag_container_{item.flag}">')
            output_lines.append(f'<div class="flag {"with_description" if description else ""}" id="flag_{item.flag}" onclick="toggleFlagDescription(\'{item.flag}\');">')
            if item.flag and not item.flag.startswith('@'):
                output_lines.append(f'<span class="flag {"hard" if item.hard else ""}">{item.flag}</span>')
                if item.text:
                    output_lines.append(item.text)
            elif item.text:
                output_lines.append(f'<span class="anonymous">{item.text}</span>')
            output_lines.append(f'</div>')

            if description or item.subsection.items:
                output_lines.append(f'<div class="flag_subsection">')
                if description:
                    output_lines.append(f'<div class="flag_description" id="flag_description_{item.flag}">{description}</div>')

                if item.subsection.items:
                    output_lines.append(_build_flag_preview_html([item.subsection]))
                
                output_lines.append('</div>')

            output_lines.append('</div>')

        output_lines.append('</div>')

    return '\n'.join(output_lines)


def _build_presets_json():
    if _cached_preset_json.is_valid():
        return _cached_preset_json.get_result()

    with open(UISPEC_PRESETS_PATH, 'r') as infile:
        file_content = infile.read()

    presets = []

    for section in file_content.split('---'):
        lines = section.split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        name = lines[0]
        flags = lines[1]

        presets.append({
            'name' : lines[0],
            'flags' : lines[1],
            'description' : ' '.join(lines[2:])
            })

    result = json.dumps(presets)
    _cached_preset_json.update_result(result)
    return result

def get_flag_controls_html():
    _build_html()
    return _cached_flag_html.get_result()['controls_html']

def _section_to_slug(section_title):
    return '_'.join(section_title.split()).lower()

def _calculate_nested_flag_visibility(enabled_flags, sections):
    result = {}
    for section in sections:
        section_result = {}
        for item in section.items:
            subresult = _calculate_nested_flag_visibility(enabled_flags, [item.subsection])
            if item.flag is not None:
                section_result[item.flag] = (item.flag in enabled_flags) or (True in subresult.values())
            section_result.update(subresult)

        if section.title:
            result['SECTION_' + _section_to_slug(section.title)] = (True in section_result.values())
        result.update(section_result)

    return result

def get_flag_preview_html(enabled_flags):
    _build_html()
    result = _cached_flag_html.get_result()['preview_html']

    # customize HTML by walking the section metadata and showing/hiding accordingly
    nested_flag_visibility = _calculate_nested_flag_visibility(
        enabled_flags,
        _cached_flag_html.get_result()['sections']
        )

    disabled_element_ids = []
    for f in nested_flag_visibility:
        visibility = ('enabled' if nested_flag_visibility[f] else 'disabled')
        if f.startswith('SECTION_'):
            result = result.replace(f'{f}_STATUS', visibility)
            if not nested_flag_visibility[f]:
                disabled_element_ids.append(f)
        else:
            result = result.replace(f'FLAG_{f}_STATUS', visibility)
            if not nested_flag_visibility[f]:
                disabled_element_ids.append(f'flag_container_{f}')

    result += (
        '\n<script> var DISABLED_FLAG_ELEMENT_IDS = [' 
        + ','.join([f"'{i}'" for i in disabled_element_ids]) 
        + '];</script>'
        )

    return result

def get_presets_json():
    return _build_presets_json()


if __name__ == '__main__':
    print(compile_uispec())

