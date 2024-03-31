# Brython AOT

Module to provide a way to pre-transpile brython .py files to .js server-side.

Creating the AST and then dumping it to JS is the slowest part of Brython and client-side caching does not solve the
delay on first load.

## Usage

```py

from brython_aot import BrythonAOT


aot = BrythonAOT()

with open("file.py") as fin:
    with open("file.py.js", "w") as fout:
        fout.write(aot.transpile(fin.read(), "file"))
```
