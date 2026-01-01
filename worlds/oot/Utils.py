import io, re, json
import os, sys
import subprocess
import Utils
from functools import lru_cache

__version__ = '7.1.0'


def data_path(*args):
    return os.path.join(os.path.dirname(__file__), 'data', *args)


@lru_cache
def read_json(file_path):
    json_string = ""
    with io.open(file_path, 'r') as file:
        for line in file.readlines():
            json_string += line.split('#')[0].replace('\n', ' ')
    json_string = re.sub(' +', ' ', json_string)
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as error:
        raise Exception("JSON parse error around text:\n" + \
                        json_string[error.pos - 35:error.pos + 35] + "\n" + \
                        "                                   ^^\n")


# From the pyinstaller Wiki: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
# Create a set of arguments which make a ``subprocess.Popen`` (and
# variants) call work with or without Pyinstaller, ``--noconsole`` or
# not, on Windows and Linux. Typical use::
#   subprocess.call(['program_to_run', 'arg_1'], **subprocess_args())
def subprocess_args(include_stdout=True):
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
    else:
        si = None
        env = None

    # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
    # So, add it only if it's needed.
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    # On Windows, running this from the binary produced by Pyinstaller
    # with the ``--noconsole`` option requires redirecting everything
    # (stdin, stdout, stderr) to avoid an OSError exception
    # "[Error 6] the handle is invalid."
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env})
    return ret


def get_version_bytes(a):
    version_bytes = [0x00, 0x00, 0x00]
    if not a:
        return version_bytes
    sa = a.replace('v', '').replace(' ', '.').split('.')

    for i in range(0, 3):
        try:
            version_byte = int(sa[i])
        except ValueError:
            break
        version_bytes[i] = version_byte

    return version_bytes


def compare_version(a, b):
    if not a and not b:
        return 0
    elif a and not b:
        return 1
    elif not a and b:
        return -1

    sa = get_version_bytes(a)
    sb = get_version_bytes(b)

    for i in range(0, 3):
        if sa[i] > sb[i]:
            return 1
        if sa[i] < sb[i]:
            return -1
    return 0

# https://stackoverflow.com/a/23146126
def find_last(source_list, sought_element):
    for reverse_index, element in enumerate(reversed(source_list)):
        if element == sought_element:
            return len(source_list) - 1 - reverse_index
