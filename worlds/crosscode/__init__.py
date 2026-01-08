import logging

cclogger = logging.getLogger(__name__)

# Because CrossCode's code generation is a submodule of the world module, this
# module must never fail to load, even if the code is malformed.
# I could easily be convinced this is a bad pattern, but I don't know what else
# to do about it currently.

try:
    from .world import CrossCodeWorld
except Exception as e:
    cclogger.fatal("Failed to import CrossCode world, probably due to faulty code generation.", exc_info=True)
