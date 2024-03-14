# World Maintainer

A world maintainer is a person responsible for a world or part of a world in Archipelago.

If a world author does not want to take on the responsibilities of a world maintainer, they can release their world as
an unofficial [APWorld](/docs/apworld%20specification.md) or maintain their own fork instead.

All current world maintainers are listed in the [CODEOWNERS](/docs/CODEOWNERS) document.

## Responsibilities

Unless these are shared between multiple people, we expect the following from each world maintainer

* Be on our Discord to get updates on problems with and suggestions for the world.
* Decide if a feature (pull request) should be merged.
* Review contents of such pull requests or organize peer reviews or post that you did not review the content.
* Fix or point out issues when core changes break your code.
* Use the watch function on GitHub, the #github-updates channel on Discord or check manually from time to time for new
  pull requests. Core maintainers may also ping you if a pull request concerns your world.
* Test (or have tested) the world on the main branch from time to time, especially during RC (release candidate) phases
  of development.
* Let us know of long periods of unavailability.

## Becoming a World Maintainer

### Adding a World

When we merge your world into the core Archipelago repository, you automatically become world maintainer unless you
nominate someone else (i.e. there are multiple devs). You can define who is allowed to approve changes to your world
in the [CODEOWNERS](/docs/CODEOWNERS) document.

### Getting Voted

When a world is unmaintained, the [core maintainers](https://github.com/orgs/ArchipelagoMW/people)
can vote for a new maintainer if there is a candidate.
For a vote to pass, the majority of participating core maintainers must vote in the affirmative.
The time limit is 1 week, but can end early if the majority is reached earlier.
Voting shall be conducted on Discord in #archipelago-dev.

## Dropping out

### Resigning

A world maintainer can resign and have their username removed from the [CODEOWNERS](/docs/CODEOWNERS) document. If no
new maintainer takes over management of the world, the world becomes unmaintained.

### Getting Voted out

A world maintainer can be voted out by the [core maintainers](https://github.com/orgs/ArchipelagoMW/people),
for example when they become unreachable.
For a vote to pass, the majority of participating core maintainers must vote in the affirmative.
The time limit is 2 weeks, but can end early if the majority is reached earlier AND the world maintainer was pinged and
made their case or was pinged and has been unreachable for more than 2 weeks already.
Voting shall be conducted on Discord in #archipelago-dev. Commits that are a direct result of the voting shall include
date, voting members and final result in the commit message.

## Handling of Unmaintained Worlds

As long as worlds are known to work for the most part, they can stay included. Once a world becomes broken it shall be
moved from `worlds/` to `worlds_disabled/`.
