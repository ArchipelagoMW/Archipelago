import enum

from .errors import *

_OBSCURED_FIELD = ' ??? '

class SpoilerRow:
    def __init__(self, *fields, public=True, obscurable=False, obscure_mask=1):
        self._fields = (list(fields[0]) if (len(fields) == 1 and type(fields[0]) in (list, tuple)) else list(fields))
        self._obscurable = obscurable
        self._obscure_mask = obscure_mask
        self._public = public
        self._obscured = False

    def is_obscurable(self):
        return self._obscurable

    def obscure(self):
        self._obscured = True

    def render(self, public=True):
        if public:
            if not self._public:
                return None
            elif self._obscured:
                processed_fields = []
                for i,field in enumerate(self._fields):
                    if not self.is_obscurable() or self._obscure_mask is None or self._obscure_mask is False:
                        processed_fields.append(field)
                    elif type(self._obscure_mask) is int:
                        processed_fields.append(field if i < len(self._fields) - self._obscure_mask else _OBSCURED_FIELD)
                    elif i >= len(self._obscure_mask):
                        processed_fields.append(field)
                    elif self._obscure_mask[i] == '!':
                        # ignore field entirely
                        pass
                    elif self._obscure_mask[i] in ('Y', 'y', True):
                        processed_fields.append(_OBSCURED_FIELD)
                    else:
                        processed_fields.append(field)

                return processed_fields
        
        return list(self._fields)


class _TableBlock:
    def __init__(self, heading, public=True, ditto_depth=0):
        self.heading = heading
        self.public = public
        self.ditto_depth = ditto_depth
        self.rows = []

    def render(self, public=True):
        if public and not self.public:
            return None

        lines = []
        if self.heading:
            lines.append(self.heading)
            lines.append("")

        filtered_rows = []
        compare_fields = None
        for row in self.rows:
            if type(row) in (list, tuple):
                row = SpoilerRow(*row)

            fields = row.render(public=public)
            if fields is None:
                continue

            in_ditto = True
            processed_fields = list(fields)
            for i in range(len(fields)):
                if in_ditto and (compare_fields is None or self.ditto_depth == 0 or i >= self.ditto_depth or i >= len(compare_fields) or compare_fields[i] != fields[i]):
                    in_ditto = False

                if in_ditto:
                    processed_fields[i] = None
            
            filtered_rows.append(processed_fields)
            compare_fields = fields

        field_widths = [max(map(lambda r: (len(r[i]) if (i < len(r) and r[i] is not None) else 0), filtered_rows)) for i in range(max(map(len, filtered_rows)))]

        for fields in filtered_rows:
            for i in range(len(fields) - 1):
                if fields[i] is None:
                    fields[i] = ' ' * (field_widths[i] + 4)
                else:
                    fields[i] += ' ..' + '.' * (field_widths[i] - len(fields[i])) + ' '
            lines.append(''.join(fields))

        return "\r\n".join(lines)


class _RawBlock:
    def __init__(self, public=True):
        self.public = public
        self.lines = []

    def render(self, public=True):
        if public and not self.public:
            return None
        else:
            return "\r\n".join(self.lines)

class SpoilerLog:
    def __init__(self):
        self._blocks = []

    def add_table(self, heading, rows, public=True, ditto_depth=0):
        block = None
        for existing_block in self._blocks:
            if isinstance(existing_block, _TableBlock) and heading == existing_block.heading:
                block = existing_block
                block.public = public               # will smash existing values,
                block.ditto_depth = ditto_depth     # needs to be better in 5.0.0
                break
        if block is None:
            block = _TableBlock(heading=heading, public=public, ditto_depth=ditto_depth)
            self._blocks.append(block)
        block.rows.extend(rows)

    def add_raw(self, *lines, public=True):
        block = _RawBlock(public=public)
        block.lines.extend(lines)
        self._blocks.append(block)

    def sparisfy(self, sparsity=100, rnd=None):
        obscurable_rows = []
        for block in self._blocks:
            try:
                rows = block.rows
            except AttributeError:
                continue
            
            for row in rows:
                try:
                    if row.is_obscurable():
                        obscurable_rows.append(row)
                except AttributeError:
                    continue
        
        for row in rnd.sample(obscurable_rows, len(obscurable_rows) * (100 - sparsity) // 100):
            row.obscure()

    def compile(self, public=True):
        lines = []
        for block in self._blocks:
            block_text = block.render(public)
            if block_text is not None:
                lines.append('-' * 80)
                lines.append('')
                lines.append(block_text)
                lines.append('')

        return '\r\n'.join(lines)
