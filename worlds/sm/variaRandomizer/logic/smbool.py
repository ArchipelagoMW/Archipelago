def flatten(l):
    if type(l) is list:
        return [ y for x in l for y in flatten(x) ]
    else:
        return [ l ]

# super metroid boolean
class SMBool:
    __slots__ = ('bool', 'difficulty', '_knows', '_items')
    def __init__(self, boolean, difficulty=0, knows=[], items=[]):
        self.bool = boolean
        self.difficulty = difficulty
        self._knows = knows
        self._items = items

    @property
    def knows(self):
        self._knows = list(set(flatten(self._knows)))
        return self._knows

    @knows.setter
    def knows(self, knows):
        self._knows = knows

    @property
    def items(self):
        self._items = list(set(flatten(self._items)))
        return self._items

    @items.setter
    def items(self, items):
        self._items = items

    def __repr__(self):
        # to display the smbool as a string
        return 'SMBool({}, {}, {}, {})'.format(self.bool, self.difficulty, sorted(self.knows), sorted(self.items))

    def __getitem__(self, index):
        # to acces the smbool as [0] for the bool and [1] for the difficulty.
        # required when we load a json preset where the smbool is stored as a list,
        # and we add missing smbools to it, so we have a mix of lists and smbools.
        if index == 0:
            return self.bool
        elif index == 1:
            return self.difficulty

    def __bool__(self):
        # when used in boolean expressions (with and/or/not) (python3)
        return self.bool

    def __eq__(self, other):
        # for ==
        return self.bool == other

    def __ne__(self, other):
        # for !=
        return self.bool != other

    def __lt__(self, other):
        # for <
        if self.bool and other.bool:
            return self.difficulty < other.difficulty
        else:
            return self.bool

    def __copy__(self):
        return SMBool(self.bool, self.difficulty, self._knows, self._items)

    def __deepcopy__(self, memodict):
        # `bool` and `difficulty` are a `bool` and `int`, so do not need to be copied.
        # The `_knows` list is never mutated, so does not need to be copied.
        # The `_items` list is a `list[str | list[str]]` (copied to a flat `list[str]` when accessed through the `items`
        # property) that is mutated by code in helpers.py, so needs to be copied. Because there could be lists within
        # the list, it is copied using the `flatten()` helper function.
        return SMBool(self.bool, self.difficulty, self._knows, flatten(self._items))

    def json(self):
        # as we have slots instead of dict
        return {'bool': self.bool, 'difficulty': self.difficulty, 'knows': self.knows, 'items': self.items}

    def wand(*args):
        # looping here is faster than using "if ... in" construct
        for smb in args:
            if not smb.bool:
                return smboolFalse

        difficulty = 0

        for smb in args:
            difficulty += smb.difficulty

        return SMBool(True,
                      difficulty,
                      [ smb._knows for smb in args ],
                      [ smb._items for smb in args ])

    def wandmax(*args):
        # looping here is faster than using "if ... in" construct
        for smb in args:
            if not smb.bool:
                return smboolFalse

        difficulty = 0

        for smb in args:
            if smb.difficulty > difficulty:
                difficulty = smb.difficulty

        return SMBool(True,
                      difficulty,
                      [ smb._knows for smb in args ],
                      [ smb._items for smb in args ])

    def wor(*args):
        # looping here is faster than using "if ... in" construct
        for smb in args:
            if smb.bool:
                return min(args)

        return smboolFalse

    # negates boolean part of the SMBool
    def wnot(a):
        return smboolFalse if a.bool else SMBool(True, a.difficulty)

    __and__ = wand
    __or__ = wor
    __not__ = wnot

smboolFalse = SMBool(False)
