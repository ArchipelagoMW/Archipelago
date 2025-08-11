from pathlib import Path


def make_data_directory(dir_name: str) -> Path:
    data_directory = Path() / "data"
    if not data_directory.exists():
        raise FileNotFoundError(f"Unable to find data directory {data_directory}")

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
