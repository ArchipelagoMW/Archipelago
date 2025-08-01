from pathlib import Path
import subprocess

config = Path(__file__).parent / "pyright-config.json"

command = ("pyright", "-p", str(config))
print(" ".join(command))

try:
    result = subprocess.run(command)
except FileNotFoundError as e:
    print(f"{e} - Is pyright installed?")
    exit(1)

exit(result.returncode)
