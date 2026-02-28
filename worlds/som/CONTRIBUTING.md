# SoM APWorld Contribution Guidelines

The code may not be stable yet, so it may be better to just leave a suggestion in an issue or on the SoMR or Archipelago
Discord for now.

If you open a PR, please consider allowing me to switch licenses in the future by including this sentence:

> I hereby grant the original author of the SoM APWorld, black-sliver, permission to relicense (make available under a
> different license) my contributions under the terms of GNU Lesser General Public License 2.1 (LGPL2.1) or newer,
> or Eclipse Public License 2.0 (EPL2).

Other parts of the software stack may be (L)GPL or EPL2 and if an opportunity to merge or move code between parts
arises, I would like to be able to.

## Running Linters

We use `black -l120` for auto-formatting, `mypy --strict` for type checking and `codespell` to find typos.

## Tests

It's not easy to write or run tests outside "core-included" tests yet.

Currently, the vanilla game is required to run any tests.
