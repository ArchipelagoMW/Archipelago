# Copied this from FE.
import csv

def _coerce(src_value, value_type):
    if type(value_type) is tuple:
        value_type, default_value = value_type
    else:
        default_value = value_type()

    try:
        converted_value = value_type(src_value)
    except Exception:
        converted_value = default_value

    return converted_value


def HexInt(src_value='0'):
    if type(src_value) is str and src_value.strip().startswith('0x'):
        src_value = src_value.strip()[2:]
    return int(src_value, 16)

def NullableHexInt(src_value=''):
    if type(src_value) is str and src_value.strip() == '':
        return None
    else:
        return HexInt(src_value)

def List(delimiter, value_type=str, filter_func=None):
    def fn(src_value=''):
        parts = src_value.split(delimiter)
        results = [_coerce(p, value_type) for p in parts]
        if filter_func is not None:
            results = list(filter(filter_func, results))
        return results
    return fn

class Row:
    def __init__(self, src_row, header_row, column_types):
        self._data = {}
        for i,value in enumerate(src_row):
            try:
                column = header_row[i].strip()
            except IndexError:
                continue

            if not column:
                continue

            try:
                column_type = column_types[column]
            except KeyError:
                column_type = str

            self._data[column] = _coerce(value, column_type)

    def __getattr__(self, name):
        return self._data[name]

    def __str__(self):
        return str(self._data)

class CsvDb:
    def __init__(self, infile, column_types={}):
        self._rows = []
        reader = csv.reader(infile)

        header_row = next(reader)
        self._rows = [Row(src_row, header_row, column_types) for src_row in reader]

    def create_view(self):
        return View(self)

class View:
    def __init__(self, csvdb):
        self._csvdb = csvdb
        self._filters = []

    def refine(self, filter_lambda):
        self._filters.append(filter_lambda)

    def get_refined_view(self, filter_lambda):
        refined_view = View(self._csvdb)
        refined_view._filters.extend(self._filters)
        refined_view._filters.append(filter_lambda)
        return refined_view

    def find_one(self, criteria_lambda):
        for row in self:
            if criteria_lambda(row):
                return row
        return None

    def find_all(self, criteria_lambda = None):
        return [row for row in self if (criteria_lambda is None or criteria_lambda(row))]

    def __iter__(self):
        for row in self._csvdb._rows:
            passed = True
            for f in self._filters:
                if not f(row):
                    passed = False
                    break

            if passed:
                yield row

