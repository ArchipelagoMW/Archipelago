# lingo data

The source of truth for the Lingo randomizer is (currently) the LL1.yaml and ids.yaml files located here. These files are used by the generator, the game client, and the tracker, in order to have logic that is consistent across them all.

The generator does not actually read in the yaml files. Instead, a compiled datafile called generated.dat is also located in this directory. If you update LL1.yaml and/or ids.yaml, you must also regenerate the datafile using `python worlds/lingo/utils/pickle_static_data.py`. A unit test will fail if you don't.
