"""Helper module for managing Linux ptrace scope permissions."""

import os
import platform
import subprocess

IS_LINUX = platform.system() == "Linux"

try:
    from CommonClient import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


def check_and_fix_ptrace_scope() -> bool:
    """Check if ptrace scope is restrictive and attempt to fix it.

    Returns:
        True if ptrace is available (either already set or successfully fixed)
        False if ptrace restrictions couldn't be fixed
    """
    if not IS_LINUX:
        return True

    ptrace_scope_path = "/proc/sys/kernel/yama/ptrace_scope"

    # Check if ptrace scope file exists
    if not os.path.exists(ptrace_scope_path):
        # No ptrace restrictions on this system
        return True

    try:
        # Read current ptrace scope
        with open(ptrace_scope_path, "r") as f:
            scope = int(f.read().strip())

        # 0 = classic ptrace (no restrictions)
        # 1 = restricted ptrace (default on many distros)
        # 2 = admin-only attach
        # 3 = no attach allowed
        if scope == 0:
            return True

        # Need to set ptrace scope to 0
        logger.info(f"Detected restrictive ptrace scope ({scope}). Attempting to enable memory access...")
        logger.info("You may be prompted for your sudo password.")

        # Try to set ptrace scope using sudo
        try:
            result = subprocess.run(["sudo", "tee", ptrace_scope_path], input=b"0\n", timeout=30)
            if result.returncode == 0:
                logger.info("Successfully enabled ptrace access.")
                return True
            else:
                logger.warning("Failed to set ptrace scope. You may need to run manually:")
                logger.warning(f"  echo 0 | sudo tee {ptrace_scope_path}")
                return False
        except subprocess.TimeoutExpired:
            logger.warning("Sudo prompt timed out.")
            return False
        except Exception as e:
            logger.warning(f"Failed to set ptrace scope: {e}")
            logger.warning(f"You may need to run manually: echo 0 | sudo tee {ptrace_scope_path}")
            return False

    except Exception as e:
        logger.warning(f"Could not check ptrace scope: {e}")
        return True  # Assume it's fine if we can't check
