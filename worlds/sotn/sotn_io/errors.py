class SoftLock(Exception):
    """Raised when soft lock is generated"""
    pass


class PickLock(Exception):
    """Soft lock inside pick relic function"""
    pass