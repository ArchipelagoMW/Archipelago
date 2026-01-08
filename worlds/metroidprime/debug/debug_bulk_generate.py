import os

from Generate import main

fail = 0
times_to_try = 30

for time in range(times_to_try):
    os.environ["skip_output"] = "true"
    try:
        main()
    except Exception as e:
        print(e.with_traceback())
        fail += 1
        continue
print("Failures: ", fail)
