  
def get_manifest(flags = None, hash = None, seed_id = None):
  from ..version import __version__
  properties = [('version', __version__)]

  if flags:
    properties.append(('flags', flags))
  if hash:
    properties.append(('hash', hash))
  if seed_id:
    properties.append(('seed_id', seed_id))
    
  return {key: value for (key, value) in properties}

if __name__ == '__main__':
  import os
  import sys
  sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
  print(get_manifest('foo'))
  print(get_manifest(hash = 'foo', seed_id = 'bar'))