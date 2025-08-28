# -*- coding: utf-8 -*-
from enum import Enum


class StandardAccessRightsEnum(Enum):
    """
    Enum with of standard access rights that correspond to operations
    common to most types of securable objects.
    """
    # Required to delete the object.
    DELETE = 0x00010000

    # Required to read information in the security descriptor for the object, not including the
    # information in the SACL. To read or write the SACL, you must request the ACCESS_SYSTEM_SECURITY
    # access right. For more information, see SACL Access Right.
    READ_CONTROL = 0x00020000

    # The right to use the object for synchronization. This enables a thread to wait until the object
    # is in the signaled state.
    SYNCHRONIZE = 0x00100000

    # Required to modify the DACL in the security descriptor for the object.
    WRITE_DAC = 0x00040000

    # Required to change the owner in the security descriptor for the object.
    WRITE_OWNER = 0x00080000
