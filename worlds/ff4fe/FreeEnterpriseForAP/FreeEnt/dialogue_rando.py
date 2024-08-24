import re
import csv
import os

from .flatfilecache import FlatFileCache

TEXT_DB_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'db', 'text_db.csv')
OCCUPATIONS_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'db', 'occupations.txt')
ZEROMUS_WIN_GAME_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'db', 'zeromus_win_game.txt')

class MapMessage:
    def __init__(self):
        self.area = None
        self.map = None
        self.number = None
        self.text = None

    def get_id(self):
        return (self.map, self.number)

def _build_hint_text(content_spec, position_spec):
    text = position_spec.text.replace('*', content_spec.text)
    text = text[0].upper() + text[1:]
    return text


CHARACTER_NAMES = ['cecil', 'kain', 'rydia', 'tellah', 'edward', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya']

class SymbolAwareString:
    def __init__(self, word=None):
        self._chars = []
        while word:
            if word[0] == '[':
                symbol = word[:word.index(']')+1]
                word = word[len(symbol):]
                symbol_name = symbol[1:-1]
                if symbol_name.startswith('name') or symbol_name.lower() in CHARACTER_NAMES:
                    self._chars.append( (symbol, 6) )
                else:
                    self._chars.append( (symbol, 1) )
            else:
                self._chars.append( (word[0], 1) )
                word = word[1:]

    def __len__(self):
        return sum([c[1] for c in self._chars])

    def __str__(self):
        return ''.join([c[0] for c in self._chars])

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        result = SymbolAwareString()
        result._chars.extend(self._chars)
        if isinstance(other, SymbolAwareString):
            result._chars.extend(other._chars)
        else:
            result._chars.extend(SymbolAwareString(other)._chars)
        return result

    def split_at(self, index):
        front = SymbolAwareString()
        back = SymbolAwareString()
        back._chars.extend(self._chars)
        
        cumulative_index = 0
        while back._chars:
            c = back._chars[0]
            if cumulative_index + c[1] <= index:
                front._chars.append(c)
                back._chars.pop(0)
            else:
                break

            cumulative_index += c[1]

        return (front, back)


def _format_text(text):
    TEXT_BOX_WIDTH = 26
    TEXT_BOX_HEIGHT = 4
    text_sections = text.split('|')
    lines = []
    while text_sections:
        section = text_sections.pop(0)
        section_lines = []

        unwrapped_lines = section.split('\\')
        for unwrapped_line in unwrapped_lines:
            wrapped_lines = []

            words = unwrapped_line.split()
            while words:
                word = words.pop(0).replace('~', ' ')
                try:
                    word = SymbolAwareString(word)
                except Exception as e:
                    print(text)
                    raise e

                if len(word) > TEXT_BOX_WIDTH:
                    while len(word) > TEXT_BOX_WIDTH:
                        front, back = word.split_at(TEXT_BOX_WIDTH)
                        wrapped_lines.append(front)
                        word = back
                    wrapped_lines.append(word)
                elif not wrapped_lines or len(wrapped_lines[-1] + ' ' + word) > TEXT_BOX_WIDTH:
                    wrapped_lines.append(word)
                else:
                    wrapped_lines[-1] += ' '
                    wrapped_lines[-1] += word

            section_lines.extend(wrapped_lines)
        
        if text_sections:
            while len(section_lines) % TEXT_BOX_HEIGHT != 0:
                section_lines.append('')

        lines.extend([str(l) for l in section_lines])

    return '\n'.join(lines)


def apply(env):
    if env.options.cache_path:
        if not os.path.isdir(os.path.join(env.options.cache_path, 'db')):
            os.makedirs(os.path.join(env.options.cache_path, 'db'))
        cache = FlatFileCache(os.path.join(env.options.cache_path, 'db', 'dialogue.cache'))
        cache_data = cache.load(__file__, TEXT_DB_PATH, OCCUPATIONS_PATH, ZEROMUS_WIN_GAME_PATH)
    else:
        cache = None
        cache_data = None
    
    if cache_data:
        map_messages = cache_data['map_messages']
        occupations = cache_data['occupations']
        zeromus_win_game = cache_data['zeromus_win_game']
    else:
        map_messages = []

        with open(TEXT_DB_PATH, 'r') as infile:
            reader = csv.reader(infile)

            header_row = next(reader)
            idx = {header_row[i].lower() : i for i in range(len(header_row)) if header_row[i]}

            while True:
                try:
                    row = next(reader)
                except StopIteration:
                    break

                msg_type = row[idx['type']].strip()
                msg_text = row[idx['text']].strip()

                if msg_type == 'training':
                    continue

                msg = MapMessage()
                msg.area = row[idx['area']]
                msg.map = row[idx['map']]
                msg.number = int(row[idx['index']][2:], 16)

                if msg_type == 'unused':
                    msg.text = 'x'
                elif msg_text:
                    msg.text = msg_text
                    
                map_messages.append(msg)

        with open(OCCUPATIONS_PATH, 'r') as infile:
            occupations = [line.strip() for line in infile if line.strip()]
        
        with open(ZEROMUS_WIN_GAME_PATH, 'r') as infile:
            zeromus_win_game = [line.strip() for line in infile if line.strip()]

        if cache:
            cache.save(
                map_messages=map_messages, 
                occupations=occupations,
                zeromus_win_game=zeromus_win_game
                )

    # generate output text replacement script
    script_parts = []
    for msg in map_messages:
        if msg.text is None:
            continue

        msg_text = msg.text
        if '-a random occupation-' in msg_text:
            occupation = env.rnd.choice(occupations)
            if occupations[0].lower() in 'aeiou':
                occupation = 'an ' + occupation
            else:
                occupation = 'a ' + occupation

            msg_text = msg_text.replace('-a random occupation-', occupation)
        elif '-random zeromus message-' in msg_text:
            zeromus_msg = env.rnd.choice(zeromus_win_game)
            msg_text = msg_text.replace('-random zeromus message-', zeromus_msg)

        msg_text = _format_text(msg_text)

        if '\n' in msg_text:
            script_parts.append(f'text(map {msg.map} message ${msg.number:02X}) {{')
            script_parts.append(msg_text)
            script_parts.append('}')
        else:
            script_parts.append(f'text(map {msg.map} message ${msg.number:02X}) {{{msg_text}}}')

    env.add_script('\n'.join(script_parts))
