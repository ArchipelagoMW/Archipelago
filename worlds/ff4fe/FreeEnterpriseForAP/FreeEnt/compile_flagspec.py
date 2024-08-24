import re
import json
import math
import pickle
import f4c.lark

import version

CONDITIONAL_GRAMMAR = '''
    rule      : expr "=>" consequences
    implicit  : flag ":" expr

    ?expr     : or_expr

    ?or_expr  : and_expr
              | or_expr "|" and_expr

    ?and_expr : atom
              | and_expr "&" atom

    ?atom     : term
              | "~" atom         -> negate
              | "(" expr ")"

    ?term     : flag 
              | regex

    flag      : /[A-Z-][a-z0-9_]*:?[a-z0-9_]*/
    regex     : "/" /[^\/]*/ "/" regex_scope?
    !regex_scope : "any"
                 | "all"

    consequences : consequence+
    consequence  : term          -> consequence_enable
                 | "~" term      -> consequence_disable

    %import common.WS
    %ignore WS
'''

class ConditionalTransformer(f4c.lark.Transformer):
    def flag(self, n):
        f = str(n[0])
        if f not in flag_order:
            raise Exception(f"Unrecognized flag {f}")
        return f

    def regex(self, n):
        try:
            scope = str(n[1])
        except IndexError:
            scope = "any"

        matching_flags = list(filter(lambda f: re.search(str(n[0]), f), flag_order))
        return [
            ('or' if scope == 'any' else 'and'),
            *matching_flags
            ]

    def regex_scope(self, n):
        return str(n[0])

    def negate(self, n):
        return ['not', n[0]]

    def and_expr(self, n):
        if type(n[0]) is list and n[0][0] == 'and':
            return ['and'] + n[0][1:] + [n[1]]
        else:
            return ['and', n[0], n[1]]

    def or_expr(self, n):
        if type(n[0]) is list and n[0][0] == 'or':
            return ['or'] + n[0][1:] + [n[1]]
        else:
            return ['or', n[0], n[1]]

    def consequence_enable(self, n):
        if type(n[0]) is list:
            return ['enable'] + n[0][1:]
        else:
            return ['enable', n[0]]

    def consequence_disable(self, n):
        if type(n[0]) is list:
            return ['disable', n[0][1:]]
        else:
            return ['disable', n[0]]

    def consequences(self, n):
        return n



sections = {}
cur_section = None

with open('flagspec.txt', 'r') as infile:
    for line in infile:
        if line.strip().startswith('#'):
            continue
            
        m = re.search(r'^----- (?P<name>.*?)\s*$', line)
        if m:
            cur_section = []
            sections[m.group('name')] = cur_section
        elif cur_section is not None:
            cur_section.append(line)

flag_order = []
flag_mutex = []
flag_binary_data = []
flag_implicit = {}

#--------------------------------------------

binary_encoding_groups = []
for line in sections['SPEC']:
    line = line.strip()

    for piece in line.split():
        parts = piece.split('/')
        flag_order.extend(parts)
        if len(parts) > 1:
            flag_mutex.append(parts)

        binary_encoding_groups.append(parts)

#--------------------------------------------

implicit_parser = f4c.lark.Lark(CONDITIONAL_GRAMMAR, start='implicit')
transformer = ConditionalTransformer()
for line in sections['IMPLICIT']:
    line = line.strip()
    if not line:
        continue
    try:
        tree = implicit_parser.parse(line)
    except f4c.lark.common.ParseError:
        raise Exception(f"Error parsing implicit flag spec: {line}")
    tree = transformer.transform(tree)
    flag_implicit[tree.children[0]] = tree.children[1]


#--------------------------------------------

field_offset = 0
for parts in binary_encoding_groups:
    nonimplicit_parts = [p for p in parts if p not in flag_implicit]
    if not nonimplicit_parts:
        continue
        
    field_size = int(math.ceil(math.log(len(nonimplicit_parts) + 1, 2)))
    value = 0
    for part in nonimplicit_parts:
        value += 1
        flag_binary_data.append({
            'flag' : part,
            'offset' : field_offset, 
            'size' : field_size, 
            'value' : value
            })
    field_offset += field_size

#--------------------------------------------

flags_to_slugs = {}
slugs_to_flags = {}
for line in sections['SLUGS']:
    m = re.search(r'^\s*(?P<flag>.+?)\s+(?P<slug>[a-z_][a-z_0-9]*)\s*$', line)
    if m:
        flag = m.group('flag')
        if flag not in flag_order:
            raise Exception(f"Unrecognized flag {flag}")
        slug = m.group('slug')
        flags_to_slugs[flag] = slug
        slugs_to_flags[slug] = flag

#--------------------------------------------

spec_data = {
    'version' : list(version.NUMERIC_VERSION),
    'order' : flag_order,
    'mutex' : flag_mutex,
    'binary' : flag_binary_data,
    'implicit' : flag_implicit,
    'flags_to_slugs' : flags_to_slugs,
    'slugs_to_flags' : slugs_to_flags,
    }

with open('flagspec.pickle', 'wb') as outfile:
    pickle.dump(spec_data, outfile)

# remove slug data from JS export
del spec_data['flags_to_slugs']
del spec_data['slugs_to_flags']

with open('server/srcdata/flagspec.js', 'wb') as outfile:
    json_spec = 'const _FE_FLAGSPEC = ' + json.dumps(spec_data, indent=4) + ';'
    encoded_json_spec = json_spec.replace('\r', '').encode('utf-8')
    outfile.write(encoded_json_spec)
