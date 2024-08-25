import pkgutil
import re
import math
import base64
import os
import pickle

try:
    import flagsetcore
except ModuleNotFoundError:
    from . import flagsetcore

_flagspec = pickle.loads(pkgutil.get_data(__name__, 'flagspec.pickle'))

class FlagSetCoreLib:
    def b64encode(self, byte_list):
        encoded = base64.b64encode(bytes(byte_list), b'-_').decode('utf-8')
        encoded = re.sub(r'=*$', '', encoded)
        return encoded

    def b64decode(self, string):
        while len(string) % 4:
            string += '='
        return list(base64.b64decode(string, b'-_'))

    def re_test(self, expression, string):
        return bool(re.search(expression, string))

    def re_search(self, expression, string):
        return re.search(expression, string)

    def re_sub(self, expression, replacement, string):
        return re.sub(expression, replacement, string)

    def push(self, target_list, value):
        target_list.append(value)

    def remove(self, target_list, value):
        if value in target_list:
            target_list.remove(value)

    def join(self, string_list, separator):
        return separator.join(string_list)

    def min(self, a, b):
        return min(a, b)

    def is_string(self, obj):
        return type(obj) is str

    def keys(self, dictionary):
        return list(dictionary)

_corelib = FlagSetCoreLib()

class FlagSet(flagsetcore.FlagSetCore):
    def __init__(self, flag_str=None, strict=True):
        super().__init__(_flagspec, _corelib)
        if flag_str is not None:
            self.load(flag_str)

    def has(self, flag):
        if flag in _flagspec['slugs_to_flags']:
            return super().has(_flagspec['slugs_to_flags'][flag])
        else:
            return super().has(flag)

class FlagLogic(flagsetcore.FlagLogicCore):
    def __init__(self):
        super().__init__(_flagspec, _corelib)

if __name__ == '__main__':
    test = FlagSet()
    import random
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('flags', nargs='?')
    parser.add_argument('--max', action='store_true')
    parser.add_argument('--load', action='store_true')
    args = parser.parse_args()

    if args.max:
        # build max flag string
        for f in _flagspec['order']:
            test.set(f)
    elif args.load:
        test = FlagSet(strict=False)
        test.load(args.flags)
        for f in test._flags:
            print(f)
    else:
        if args.flags:
            test.load(args.flags)
        else:
            for f in random.sample(_flagspec['order'], random.randint(1, len(_flagspec['order']))):
                print(f)
                test.set(f)

    print('-------- Parse')
    print(test.parse())
    print('-------- ToString')
    print(test.to_string(pretty=True, wrap_width=28))
    print('-------- ToBinary')
    print(test.to_binary())
    print('-------- LoadString')
    test2 = FlagSet(test.to_string())
    print(test2.to_binary())
    print('-------- LoadBinary')
    test3 = FlagSet(test.to_binary())
    print(test3.to_binary())

    print('-------- Logic')
    logic = FlagLogic()
    result = logic.fix(test)
    if result:
        for log in result:
            print(f"{log[0]} : {log[1]}")
        print('-------- Post-text')
        print(test.to_string(pretty=True, wrap_width=28))
