class _CachedFunction:
    def __init__(self, *args, **kwargs):
        self.arg_string = ' '.join(str(arg) for arg in args) + " " + ' '.join(str(kwarg) for kwarg in kwargs.values())
        if not hasattr(type(self), "addresses"):
            type(self).addresses = {}

    def address(self, *args, **kwargs):
        # if two instances of the same type have the same arguments then return the same address for both instances
        # prevent writing the same function multiple times
        if self.arg_string in type(self).addresses:
            self.space = type(self).addresses[self.arg_string]
            return self.space.start_address

        self.space = self.write(*args, **kwargs)
        type(self).addresses[self.arg_string] = self.space
        return self.space.start_address

    def write(self, *args, **kwargs):
        raise NotImplementedError(self.__class__.__name__ + " write")

    def __str__(self):
        return super().__str__() + " " + self.arg_string
