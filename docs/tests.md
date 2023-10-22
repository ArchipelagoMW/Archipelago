# Archipelago Unit Testing API

This document covers some of the generic tests available using Archipelago's unit testing system, as well as some basic
steps on how to write your own.

## Generic Tests

Some generic tests are run on every World to ensure basic functionality with default options. The basic tests that are
run on every world are found in the [general test directory.](/test/general)

## Defining World Tests

In order to run tests from your World, you will need to create a `test` package within your World package. This can be
done by creating a `test` directory with a file named `__init__.py` inside it inside your world. By convention, a base
for your World tests can be created in this file that you can then import into other modules.

### WorldTestBase

In order to test basic functionality of varying options, as well as to test specific edge cases or that certain
interactions in the World interact as expected, you will want to use the [WorldTestBase.](/test/bases.py) This class
comes with the basics for test setup as well as a few preloaded tests that most worlds might want to check on varying
options combinations.

Example `/test/__init__.py`:

```python
from test.bases import WorldTestBase


class MyGameTestBase(WorldTestBase):
    game = "My Game"
```

The basic tests that WorldTestBase comes with, currently, are `test_all_state_can_reach_everything`,
`test_empty_state_can_reach_something`, and `test_fill`. These test that with all collected items everything is
reachable, with no collected items at least something is reachable, and that a valid MultiWorld can be completed with
all steps being called, respectively.

### Writing Tests

Adding runs for the basic tests for a different option combination is as easy as making a new module in the test
package, creating a class that inherits from your game's TestBase, and defining the options in a dict as a field on the
class. The new module should be named `test_<something>.py` and have at least one class inheriting from the base, or
define its own testing methods. Newly defined test methods should follow standard PEP8 snake_case format and also start
with `test_`

Example `/test/test_chest_access.py`:

```python
from . import MyGameTestBase


class TestChestAccess(MyGameTestBase):
    options = {
        "difficulty": "easy",
        "final_boss_hp": 4000,
    }

    def test_sword_chests(self) -> None:
        """Test locations that require a sword"""
        locations = ["Chest1", "Chest2"]
        items = [["Sword"]]
        # This tests that the provided locations aren't accessible without the provided locations, but can be once
        # obtained. This will also check that any locations not provided don't have the same dependency requirement.
        # Optionally, passing True to the method will only check the locations provided.
        self.assertAccessDependency(locations, items)
```

When tests are run, this class will create a World with the provided options, and run the basic tests, as well as the
new custom test. If you don't want to run tests on a base, `run_default_tests` can be overridden. For more information
on what methods are available to your class, check the [WorldTestBase definition](/test/bases.py).

## Running Tests

In PyCharm, running all tests can be done by right-clicking the root `test` directory and selecting `run tests`. If you
do not have pytest installed, you may get import failures. To solve this, edit the run configuration, and set the
working directory of the run to the Archipelago directory. If you only want to run your World's defined tests, repeat
the steps for the test directory within your World.
