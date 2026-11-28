# Development setup

Using PyCharm is advised. Otherwise, you're on your own.

## Installing dev dependencies

This installs the dependencies to run the tests faster and formatting the code.

```shell
pip install -r requirements-dev.txt
```

If you run multiple venv with different python version, you will need to run this on every environment.

## Formatter/linting

Use _ruff_ as formatter and linter. Why? It is much, much faster than the default formatter of PyCharm and now it integrates seamlessly. We use the same rule as the rest of core, just with longer lines.

Once installed, make sure PyCharm recognizes it and uses it. Go in _Settings..._ > _Python_ > _Tools_ > _Ruff_ and enable everything. Make sure it runs on save so you can forget about it.  Go in _Settings..._ again, then _Tools_ (not _Python_ here) > _Actions on save_, enable _Reformat code_ and _Optimize imports_. **Make sure to choose _Changed lines_ for _Reformat code_**. This will minimize the chances of conflicts. Some files do not exactly follow this format just yet.

## Running the tests

Most of the time to will only need to run the unit tests.

```shell
python -m pytest -n auto
```

To run the long tests along with them, use

```shell
# For unix
export long=True; python -m pytest -n auto
```

```shell
# For powershell
set-content env:long True; python -m pytest -n auto
```

To add the base fill tests to the unit tests, use 

```shell
# For unix
export base=True; python -m pytest -n auto
```

```shell
# For powershell
set-content env:base True; python -m pytest -n auto
```

Or to run every test, use

```shell
# For unix
export base=True; export long=True; python -m pytest -n auto
```

```shell
# For powershell
set-content env:base True; set-content env:base True; python -m pytest -n auto
```
