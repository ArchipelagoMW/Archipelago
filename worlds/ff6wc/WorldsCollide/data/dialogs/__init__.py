def __init__():
    from ...data.dialogs.dialogs import Dialogs
    dialogs = Dialogs()

    import sys, inspect
    module = sys.modules[__name__]
    for name, member in inspect.getmembers(dialogs, inspect.ismethod):
        if not name.startswith('_'):
            setattr(module, name, member)

    module.OBJECTIVES = Dialogs.OBJECTIVES
    module.BATTLE_OBJECTIVES = Dialogs.BATTLE_OBJECTIVES
__init__()
