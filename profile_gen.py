"""Quick profiling script for Pokepelago generation."""
import cProfile
import pstats
import io
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

sys.argv = ['Generate.py', '--player_files_path', 'Players',
            '--multi', '4', '--skip_output']

pr = cProfile.Profile()
pr.enable()

try:
    exec(open('Generate.py').read())
except SystemExit:
    pass
except Exception as e:
    print(f"Error: {e}")

pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats(30)
print(s.getvalue())
