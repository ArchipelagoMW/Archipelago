# Vendored dependencies

Pure-Python packages bundled so the world works on frozen Archipelago installs, which
cannot pip-install anything. Compiled extensions cannot live here: zipimport cannot
load `.pyd`/`.so` files from a zipped `.apworld`.

This directory is added to `sys.path` (appended, so environment installs win) by
`worlds/cvaos/_vendor.py`, on demand from `worlds/cvaos/_pydantic_compat.py` and
`worlds/cvaos/_bytemaker_compat.py`.

Note: the directory is named `vendor` rather than `lib` because the repo .gitignore
excludes any `lib/` directory as a build artifact.

| Package | Version | Source | License |
|---|---|---|---|
| pydantic | 1.10.26 | `pydantic-1.10.26-py3-none-any.whl` from PyPI, unmodified | MIT (see `pydantic/LICENSE`) |
| bytemaker | 0.11.0 | `bytemaker-0.11.0-py3-none-any.whl` from PyPI, unmodified | MIT (see `bytemaker/LICENSE`) |

Without bitarray installed (frozen installs), bytemaker uses its pure-Python
`bitvector_native` BitVector; with bitarray (`pip install bytemaker[speedups]`) it
uses the C-backed fast path automatically.

To update: download the new `py3-none-any` wheel from PyPI, extract, and replace the
package directory wholesale. Stay on the 1.10.x line — pydantic v2 requires the
compiled `pydantic_core`.
