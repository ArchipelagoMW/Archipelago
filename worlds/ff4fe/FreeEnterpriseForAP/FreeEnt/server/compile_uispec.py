import re
import os
import json

import objective_data

def format_description(description):
    lines = description.split('\n')
    is_list = True
    for line in lines:
        if line.strip() and not line.startswith('- '):
            is_list = False
    
    if is_list:
        return '<ul>' + ''.join([f'<li>{line[2:]}</li>' for line in lines]) + '</ul>'
    else:   
        return description

with open("srcdata/flagspec.js", "r") as infile:
    flagspec_json = infile.read()
    flagspec_json = re.sub(r'^.*?\{', '{', flagspec_json)
    flagspec_json = re.sub(r'\}[^}]*$', '}', flagspec_json)
    flagspec = json.loads(flagspec_json)

# Load flag description text
with open("uispec_flagdescriptions.txt", "r") as infile:
    descriptions_raw = infile.read()

descriptions_parts = re.split(r'^\s*\[(.*?)\]\s*$', descriptions_raw, flags=re.MULTILINE)
descriptions = {}
while descriptions_parts:
    part = descriptions_parts.pop(0).strip()
    if part:
        descriptions[part] = descriptions_parts.pop(0).strip()

# Load, parse and build ui spec
with open("uispec.txt", "r") as infile:
    uispec_raw = infile.read()

section_regex = re.compile(r'^\s*(==.*)$', flags=re.MULTILINE)
section_parts = section_regex.split(uispec_raw)

sections = []
anonymous_id_counter = 0

flag_control_map = {}

while section_parts:
    section_part = section_parts.pop(0).strip()
    if not section_part:
        continue

    m = re.search(r'^==\s*(?P<title>.*)$', section_part)
    if not m:
        raise Exception(f"Extraneous part: {section_part}")

    section = {'title' : m['title'], 'controls' : []}
    sections.append(section)
    section_lines = section_parts.pop(0).strip().split('\n')

    branch = []
    for line in section_lines:
        line = line.strip()
        if not line:
            continue

        m = re.search(r'^\.*', line)
        level = len(m[0])
        if len(branch) < level:
            raise Exception(f'Hierarchy depth error at line {line}')

        line = line[level:]

        m = re.search(r'^\((.*?)\)', line)
        control_type = "radio"
        if not m:
            m = re.search(r'^\[(.*?)\]', line)
            control_type = "check"
        if not m:
            m = re.search(r'^\<(.*?)\>', line)
            control_type = "select"
        if not m:
            m = re.search(r'^-+$', line)
            control_type = 'separator'

        if not m:
            print(f"Parse error on line {line}")

        try:
            flag = m[1].strip()
        except IndexError:
            flag = ''

        if flag.startswith('ECHO:'):
            echo_flag = flag[len('ECHO:'):]
            subcontrols = flag_control_map[echo_flag].get('subcontrols', [])
            branch = branch[:level]
            if branch:
                branch[-1].setdefault('subcontrols', []).extend(subcontrols)
            else:
                section['controls'].extend(subcontrols)
        else:
            modifiers = set()
            flags = []
            if flag.endswith('*'):
                prefix = flag[:-1]
                for f in flagspec['order']:
                    if not f.startswith(prefix):
                        continue

                    slug = f.split(':')[1]
                    for oid in objective_data.OBJECTIVES:
                        o = objective_data.OBJECTIVES[oid]
                        if slug == o['slug']:
                            flags.append((f, o['desc']))
            else:
                if not flag:
                    flag = f"@anon{anonymous_id_counter}"
                    anonymous_id_counter += 1

                line = line[len(m[0]):]
                m = re.search(r'^[!#\-*]+', line)
                if m:
                    modifiers = set(m[0])
                    line = line[len(m[0]):].strip()
                else:
                    line = line.strip()

                flags.append((flag, line))

            for flag_info in flags:
                flag,title = flag_info
                flag_control = {'flag' : flag, 'title' : title}
                if flag in descriptions:
                    flag_control['description'] = format_description(descriptions[flag])
                if '!' in modifiers:
                    flag_control['hard'] = True
                if '#' in modifiers:
                    flag_control['compact'] = True
                if '-' in modifiers:
                    flag_control['null'] = True
                if '*' in modifiers:
                    flag_control['important'] = True

                if control_type in ["select", "separator"]:
                    flag_control['type'] = control_type

                branch = branch[:level]
                if branch:
                    branch[-1].setdefault('subcontrols', []).append(flag_control)
                else:
                    section['controls'].append(flag_control)

                branch.append(flag_control)
                flag_control_map[flag] = flag_control

with open('script/uispec.js', 'w') as outfile:
    outfile.write("// This file is generated by compile_uispec.py\n")
    outfile.write("var FLAG_UISPEC = ")
    outfile.write(json.dumps(sections, indent=2))
    outfile.write(";\n")
