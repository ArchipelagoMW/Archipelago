# the caching decorator for helpers functions
class VersionedCache(object):
    __slots__ = ( 'cache', 'masterCache', 'nextSlot', 'size')

    def __init__(self):
        self.cache = []
        self.masterCache = {}
        self.nextSlot = 0
        self.size = 0

    def reset(self):
        # reinit the whole cache
        self.masterCache = {}
        self.update(0)

    def update(self, newKey):
        cache = self.masterCache.get(newKey, None)
        if cache is None:
            cache = [ None ] * self.size
            self.masterCache[newKey] = cache
        self.cache = cache

    def decorator(self, func):
        return self._decorate(func.__name__, self._new_slot(), func)

    # for lambdas
    def ldeco(self, func):
        return self._decorate(func.__code__, self._new_slot(), func)

    def _new_slot(self):
        slot = self.nextSlot
        self.nextSlot += 1
        self.size += 1
        return slot

    def _decorate(self, name, slot, func):
        def _decorator(arg):
            #ret = self.cache[slot]
            #if ret is not None:
            #    return ret
            #else:
                ret = func(arg)
            #    self.cache[slot] = ret
                return ret
        return _decorator

Cache = VersionedCache()

class RequestCache(object):
    def __init__(self):
        self.results = {}

    def request(self, request, *args):
        return ''.join([request] + [str(arg) for arg in args])

    def store(self, request, result):
        self.results[request] = result

    def get(self, request):
        return self.results[request] if request in self.results else None

    def reset(self):
        self.results.clear()
