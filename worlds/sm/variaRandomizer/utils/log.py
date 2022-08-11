import logging, sys

# store the debug flag at module level
debug = False

def init(pdebug):
    global debug
    debug = pdebug

    if debug == True:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

def get(name):
    return logging.getLogger(name)
