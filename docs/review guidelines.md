# Review Guidelines

[Quick link to the checklist](#review-checklist).

These guidelines apply to suggested changes to core Archipelago and WebHost. That is everything besides /worlds/ but
including /worlds/generic/. Worlds may define their own guidelines in the respective source directory.

A full review should go through the checklist. The author of a Pull Request should self-review either before or right
after opening a Pull Request.

## Review Checklist

1.  If it's a draft only look at the sections the author asked about.
    [Details](#1-draft-prs)
2.  Does the contribution change program structure or strongly impacts maintainability?
    If so, was this brought up and approved on Discord or another earlier discussion?
    [Details](#2-structure--maintainability--risks)
3.  Does the PR have tests, explain how to test or is the change trivial? Are the tests complete?
    [Details](#3-testing)
4.  Does the PR meet requirements without introducing unnecessary complication?
    [Details](#4-unnecessary-complication)
5.  Is the PR too big?
    [Details](#5-pr-size)
6.  Is the change self-documenting or adds documentation? Does it have surprising (side) effects?
    [Details](#6-documentation--naming)
7.  Looking at the surrounding code, are there missed refactoring opportunities?
    [Details](#7-surrounding-code)
8.  Look at static analyzer results (i.e. linters and type errors/warnings unless required by CI).
    [Details](#8-static-analyzers)
9.  Does the code change follow the style guide?
    [Details](#9-style-guide)
10. Does the change introduce bad practices, insecure functions or unnecessary (arithmetic) complexity?
    Are there cases where the code may not finish running / is stuck in an endless loop?
    [Details](#10-code--implementation-quality)
11. Clarify which change requests / PR comments are nitpicks and which are critical.
    [Details](#11-change-requests-and-nitpicks)

## Examples and Details

### 1. Draft PRs

If there are no question in a draft PR, or they are unclear, point to *draft Pull Requests* section in
[contributing.md](contributing.md).

### 2. Structure / Maintainability / Risks

Things like new dependencies, shuffling big portions of code around, adding big portions of code, adding new entry
points, adding new endpoints or extending "bad" legacy code may introduce new bugs and/or impact future maintainability
of the code.

Changing those after opening the PR may invalidate all existing reviews, and should be considered before a full review.

If such changes were not discussed beforehand, consider discussion in the PR or pointing them to Discord before looking
at details.

Ideally if this was pre-approved, there is a note like "as discussed on Discord".

### 3. Testing

Ideally all non-trivial code changes, including corner cases, are covered by unit tests.
If tests are incomplete, consider asking the author to add tests.
If the PR mentions how to test the change (manually), check if that appears to be complete.
If it's not a trivial change, nor does it add (complete) tests, nor does it explain how to test, request a change and
don't continue with the review.

For code changes that could affect multiple worlds or that could have changes in unexpected code paths, manual testing
or checking if all code paths are covered by automated tests is desired. The original author may not have been able to
test all possibly affected worlds, or didn't know it would affect another world. In such cases, it is helpful to state
which games or settings were rolled, if any.
If testing the PR depends on other PRs, please state what you merged into what for testing.

### 4. Unnecessary Complication

Code that is too complicated where there is a simpler solution should be pointed out as such.

It may hurt both the review and future maintenance of the code.

### 5. PR Size

In most cases, if a PR fixes a bug, it should not add features or change existing behavior that is unrelated.

If a PR is big already, consider if parts should be split out into a separate PR. It's harder to review big PRs.

### 6. Documentation / Naming

Do function and variable names match what the function is actually doing?
Relying on comments is not great because they can be outdated.

For functions that are hard to describe in few words, consider if a doc string should be required.

### 7. Surrounding Code

If existing code can be adapted without lumping together functionality or if a common part can be extracted, this
should be done. Depending on the size of the change and number of duplicated lines this may be a nitpick or a
requirement for maintainability reasons.

### 8. Static Analyzers

Static analysis helps to find problems before they happen at runtime, such as mixing types or using unsafe features.

CI generates reports in "Analyze modified files" for Python code that can be used.
We recommend using mypy, pyright or basedpyright locally to check for type errors and
ruff or flake8 for general warnings.
See / use ruff.toml for agreed-on rules.

For other language we don't have a defined setup yet.

All new code should make use of type hints if possible.
Only critical problems should block a PR, but it should be pointed out as a nitpick if there are any typing or linter
problems in the new code.

Additionally, individual files can be made to require passing strict type checking by adding them to
`.github /pyright-config.json`.

*In the future, an ignore-list and list of extensions for flake8 may be specified.*

### 9. Style Guide

Style Guide is not just formatting, but may list *Dos and Don'ts* for each individual language.

If there are only formatting problems, this may be a nitpick. If the change adds a lot of *Don't*, a change should be
requested.

### 10. Code / Implementation Quality

Generate, Multiserver and WebHost are performance critical and are susceptible to DoS, so *code that works* may not
be good enough.

Code that may never finish (in edge cases) may not be acceptable.

### 11. Change Requests and Nitpicks

Use the "request changes" review feature if the changes are critical,
if it's only nitpicks use the "comment" review feature.

Try to use proper phrasing to signal if a change is deemed necessary or if it's up to the author.
The author should respond in either case, but any back and forth may delay the change getting merged.
