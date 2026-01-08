import collections
import yaml

class CounterDumper(yaml.SafeDumper):
    """A SafeDumper that knows how to serialize collections.Counter."""
    pass

# whenever we hit a Counter, just treat it as a dict
CounterDumper.add_representer(
    collections.Counter,
    lambda dumper, data: dumper.represent_dict(dict(data))
)
CounterDumper.add_multi_representer(
    collections.Counter,
    lambda dumper, data: dumper.represent_dict(dict(data))
)

def restricted_safe_dump(data, **kwargs):
    """
    Like yaml.safe_dump, but will also turn any Counter into a plain mapping.
    Passes all other kwargs through to yaml.dump().
    """
    return yaml.dump(data, Dumper=CounterDumper, **kwargs)