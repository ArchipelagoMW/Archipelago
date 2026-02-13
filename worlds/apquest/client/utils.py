from pathlib import Path

from Utils import user_path


def make_data_directory(dir_name: str) -> Path:
    root_directory = Path(user_path())
    if not root_directory.exists():
        raise FileNotFoundError(f"Unable to find AP directory {root_directory.absolute()}.")

    data_directory = root_directory / "data"

    specific_data_directory = data_directory / "apquest" / dir_name
    specific_data_directory.mkdir(parents=True, exist_ok=True)

    gitignore = specific_data_directory / ".gitignore"

    with open(gitignore, "w") as f:
        f.write(
            """*
!.gitignore
"""
        )

    return specific_data_directory
