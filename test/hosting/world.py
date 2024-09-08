import re
import shutil
from pathlib import Path
from typing import Dict


__all__ = ["copy", "delete"]


_new_worlds: Dict[str, str] = {}


def copy(src: str, dst: str) -> None:
    from Utils import get_file_safe_name
    from worlds import AutoWorldRegister

    assert dst not in _new_worlds, "World already created"
    if '"' in dst or "\\" in dst:  # easier to reject than to escape
        raise ValueError(f"Unsupported symbols in {dst}")
    dst_folder_name = get_file_safe_name(dst.lower())
    src_cls = AutoWorldRegister.world_types[src]
    src_folder = Path(src_cls.__file__).parent
    worlds_folder = src_folder.parent
    if (not src_cls.__file__.endswith("__init__.py") or not src_folder.is_dir()
            or not (worlds_folder / "generic").is_dir()):
        raise ValueError(f"Unsupported layout for copy_world from {src}")
    dst_folder = worlds_folder / dst_folder_name
    if dst_folder.is_dir():
        raise ValueError(f"Destination {dst_folder} already exists")
    shutil.copytree(src_folder, dst_folder)
    _new_worlds[dst] = str(dst_folder)
    with open(dst_folder / "__init__.py", "r", encoding="utf-8-sig") as f:
        contents = f.read()
    contents = re.sub(r'game\s*=\s*[\'"]' + re.escape(src) + r'[\'"]', f'game = "{dst}"', contents)
    with open(dst_folder / "__init__.py", "w", encoding="utf-8") as f:
        f.write(contents)


def delete(name: str) -> None:
    assert name in _new_worlds, "World not created by this script"
    shutil.rmtree(_new_worlds[name])
    del _new_worlds[name]
