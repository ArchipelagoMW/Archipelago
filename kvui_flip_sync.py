"""
Moves the vsync wait off the GIL (kivy/kivy#9411). Kivy releases the GIL only
around the buffer swap, but some drivers return from the swap at
once and stalls the next frame's first GL call, made with the GIL held, until
vblank. After each swap this clears and finishes through ctypes, which releases
the GIL for each call, so the wait lands there. Config graphics.sync_after_flip.
"""
from __future__ import annotations

__all__ = ("flip_sync_state", "install_flip_sync")

import configparser
import ctypes
import os
import re
import sys
from collections.abc import Callable

from kivy.config import Config
from kivy.core.window import Window
from kivy.core.window.window_sdl2 import WindowSDL
from kivy.graphics.cgl import cgl_get_initialized_backend_name
from kivy.graphics.opengl import GL_VENDOR, glGetString
from kivy.logger import Logger

_GL_COLOR_BUFFER_BIT = 0x4000

_state = "off"


def flip_sync_state() -> str:
    """One of "off", "pending" (installed, no flip yet), "on" or "unavailable (<reason>)"."""
    return _state


def _loaded_sdl() -> ctypes.CDLL:
    """The SDL2 Kivy already initialised (not win32); a second copy has no video subsystem."""
    if sys.platform == "darwin":
        dyld = ctypes.CDLL(None)
        dyld._dyld_get_image_name.restype = ctypes.c_char_p
        paths = [os.fsdecode(dyld._dyld_get_image_name(i)) for i in range(dyld._dyld_image_count())]
    else:
        with open("/proc/self/maps") as maps:
            paths = [line.split(maxsplit=5)[-1].strip() for line in maps]
    return ctypes.CDLL(next(
        path for path in paths if re.fullmatch(r"(lib)?SDL2([-.].*)?", os.path.basename(path))))


def _gl_function(address: int, *argtypes) -> Callable[..., None]:
    """The void GL function at `address` (APIENTRY: stdcall on win32). ctypes
    releases the GIL for each call, which a PYFUNCTYPE prototype would not."""
    prototype = ctypes.WINFUNCTYPE if sys.platform == "win32" else ctypes.CFUNCTYPE
    return prototype(None, *argtypes)(address)


def _gl_clear_and_finish() -> tuple[Callable[[int], None], Callable[[], None]]:
    """glClear and glFinish of the current GL context."""
    if sys.platform == "win32":
        # GL 1.1 entry points are opengl32 exports; SDL_GL_GetProcAddress asks
        # wglGetProcAddress, which some drivers answer with bogus 1/2/3/-1 pointers.
        opengl32 = ctypes.WinDLL("opengl32")
        clear, finish = (ctypes.cast(getattr(opengl32, name), ctypes.c_void_p).value
                         for name in ("glClear", "glFinish"))
    else:
        sdl = _loaded_sdl()
        sdl.SDL_GL_GetProcAddress.restype = ctypes.c_void_p
        sdl.SDL_GL_GetProcAddress.argtypes = (ctypes.c_char_p,)
        clear, finish = map(sdl.SDL_GL_GetProcAddress, (b"glClear", b"glFinish"))
        if not (clear and finish):
            raise LookupError("SDL_GL_GetProcAddress returned NULL")
    return _gl_function(clear, ctypes.c_uint), _gl_function(finish)


def _sync_enabled() -> bool:
    try:
        return Config.getboolean("graphics", "sync_after_flip")
    except (ValueError, configparser.Error):
        return False


def _disable(reason: str) -> None:
    global _state
    _state = f"unavailable ({reason})"
    Logger.warning("FlipSync: off for this session, %s", reason)


def install_flip_sync() -> bool:
    """Patch WindowSDL.flip once, when graphics.sync_after_flip is on and the
    window has an NVIDIA desktop GL context; the GL functions resolve on the
    first flip."""
    global _state
    if _state != "off" or not _sync_enabled() or not isinstance(Window, WindowSDL):
        return False
    backend = cgl_get_initialized_backend_name()
    print("FlipSync: backend %s,", backend )
    if backend == "mock":  # no GL context at all
        return False
    if backend == "angle_sdl2":
        _state = "unavailable (ANGLE renders through Direct3D)"
        return False
    # everything else is sdl2 - flip them.
    original = WindowSDL.flip
    gl = None

    def flip(self):
        global _state
        nonlocal gl
        original(self)
        if _state == "pending":
            try:
                gl = _gl_clear_and_finish()
            except Exception as error:
                _disable(f"GL lookup failed: {error!r}")
            else:
                _state = "on"
        if _state == "on":
            clear, finish = gl
            try:
                clear(_GL_COLOR_BUFFER_BIT)
                finish()
            except OSError as error:
                _disable(f"GL call failed: {error}")

    WindowSDL.flip = flip
    _state = "pending"
    return True