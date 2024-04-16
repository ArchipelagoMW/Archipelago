from pathlib import Path
import subprocess
import sys

config = Path(__file__).parent / "pyright-config.json"

command: int = ("pyright", "-p", str(config))
print(" ".join(command))

try:
    result = subprocess.run(
        ("pyright", "-p", str(config)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
except FileNotFoundError as e:
    print(f"{e} - Is pyright installed?")
    exit(1)

sys.stdout.write((result.stdout or b"").decode())
sys.stderr.write((result.stderr or b"").decode())

exit(result.returncode)
