import json
from pathlib import Path
import subprocess
from typing import Any, Dict, List, Union

source_dir = Path(__file__).parent
config = source_dir / "pyright-config.json"


def run_pyright() -> int:
    """ returns process exit code """
    command = ("pyright", "-p", str(config))
    print(" ".join(command))

    try:
        pyright_result = subprocess.run(command)
    except FileNotFoundError as e:
        print(f"{e} - Is pyright installed?")
        exit(1)
    return pyright_result.returncode


def run_mypy() -> int:
    """ returns process exit code """
    with open(config) as config_file:
        config_data: Union[Dict[str, Any], Any] = json.load(config_file)

    assert isinstance(config_data, dict)
    file_list: Union[List[str], None, Any] = config_data.get("include")
    assert isinstance(file_list, list), f"unknown data in config file: {type(file_list)=}"
    file_list = [
        str(source_dir / file_name)
        for file_name in file_list
    ]
    params = [
        "mypy",
        "--strict",
        "--follow-imports=silent",
        "--no-warn-unused-ignore",
        "--install-types",
        "--non-interactive",
        "typings",
    ]

    command = params + file_list
    print(" ".join(params))

    try:
        mypy_result = subprocess.run(command)
    except FileNotFoundError as e:
        print(f"{e} - Is mypy installed?")
        exit(1)
    return mypy_result.returncode


if __name__ == "__main__":
    # mypy is first because of its --install-types feature
    mypy_ret = run_mypy()
    pyright_ret = run_pyright()
    exit(mypy_ret or pyright_ret)
