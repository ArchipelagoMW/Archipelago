# Triage Role Expectations

Users with Triage-level access are selected contributors who can and wish to proactively label/triage issues and pull 
requests without being granted write access to the Archipelago repository.

Triage users are not necessarily official members of the Archipelago organization, for the list of core maintainers,
please reference [ArchipelagoMW Members](https://github.com/orgs/ArchipelagoMW/people) page.

## Access Permissions

Triage users have the following permissions:

* Apply/dismiss labels on all issues and pull requests.
* Close, reopen, and assign all issues and pull requests.
* Mark issues and pull requests as duplicate.
* Request pull request reviews from repository members.
* Hide comments in issues or pull requests from public view.
    * Hidden comments are not deleted and can be reversed by another triage user or repository member with write access.
* And all other standard permissions granted to regular GitHub users.

For more details on permissions granted by the Triage role, see 
[GitHub's Role Documentation](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization).

## Expectations

Users with triage-level permissions have no expectation to review code, but, if desired, to review pull requests/issues 
and apply the relevant labels and ping/request reviews from any relevant [code owners](./CODEOWNERS) for review. Triage 
users are also expected not to close others' issues or pull requests without strong reason to do so (with exception of 
`meta: invalid` or `meta: duplicate` scenarios, which are listed below). When in doubt, defer to a core maintainer.

Triage users are not "moderators" for others' issues or pull requests. However, they may voice their opinions/feedback 
on issues or pull requests, just the same as any other GitHub user contributing to Archipelago.

## Labeling

As of the time of writing this document, there are 15 distinct labels that can be applied to issues and pull requests.

### Affects

These labels notate if certain issues or pull requests affect critical aspects of Archipelago that may require specific 
review. More than one of these labels can be used on a issue or pull request, if relevant.

* `affects: core` is to be applied to issues/PRs that may affect core Archipelago functionality and should be reviewed 
with additional scrutiny.
    * Core is defined as any files not contained in the `WebHostLib` directory or individual world implementations 
    directories inside the `worlds` directory, not including `worlds/generic`.
* `affects: webhost` is to be applied to issues/PRs that may affect the core WebHost portion of Archipelago. In 
general, this is anything being modified inside the `WebHostLib` directory or `WebHost.py` file.
* `affects: release/blocker` is to be applied for any issues/PRs that may either negatively impact (issues) or propose 
to resolve critical issues (pull requests) that affect the current or next official release of Archipelago and should be
given top priority for review.

### Is

These labels notate what kinds of changes are being made or proposed in issues or pull requests. More than one of these 
labels can be used on a issue or pull request, if relevant, but at least one of these labels should be applied to every 
pull request and issue.

* `is: bug/fix` is to be applied to issues/PRs that report or resolve an issue in core, web, or individual world 
implementations.
* `is: documentation` is to be applied to issues/PRs that relate to adding, updating, or removing documentation in 
core, web, or individual world implementations without modifying actual code.
* `is: enhancement` is to be applied to issues/PRs that relate to adding, modifying, or removing functionality in 
core, web, or individual world implementations.
* `is: refactor/cleanup` is to be applied to issues/PRs that relate to reorganizing existing code to improve 
readability or performance without adding, modifying, or removing functionality or fixing known regressions.
* `is: maintenance` is to be applied to issues/PRs that don't modify logic, refactor existing code, change features.
This is typically reserved for pull requests that need to update dependencies or increment version numbers without 
resolving existing issues.
* `is: new game` is to be applied to any pull requests that introduce a new game for the first time to the `worlds` 
directory. 
    * Issues should not be opened and classified with `is: new game`, and instead should be directed to the 
    #future-game-design channel in Archipelago for opening suggestions. If they are opened, they should be labeled 
    with `meta: invalid` and closed.
    * Pull requests for new games should only have this label, as enhancement, documentation, bug/fix, refactor, and 
    possibly maintenance is implied.

### Meta

These labels allow additional quick meta information for contributors or reviewers for issues and pull requests. They 
have specific situations where they should be applied.

* `meta: duplicate` is to be applied to any issues/PRs that are duplicate of another issue/PR that was already opened. 
    * These should be immediately closed after leaving a comment, directing to the original issue or pull request.
* `meta: invalid` is to be applied to any issues/PRs that do not relate to Archipelago or are inappropriate for 
discussion on GitHub.
    * These should be immediately closed afterwards.
* `meta: help wanted` is to be applied to any issues/PRs that require additional attention for whatever reason.
    * These should include a comment describing what kind of help is requested when the label is added.
    * Some common reasons include, but are not limited to: Breaking API changes that require developer input/testing or 
    pull requests with large line changes that need additional reviewers to be reviewed effectively.
    * This label may require some programming experience and familiarity with Archipelago source to determine if 
    requesting additional attention for help is warranted.
* `meta: good first issue` is to be applied to any issues that may be a good starting ground for new contributors to try 
and tackle.
    * This label may require some programming experience and familiarity with Archipelago source to determine if an 
    issue is a "good first issue".
* `meta: wontfix` is to be applied for any issues/PRs that are opened that will not be actioned because it's out of 
scope or determined to not be an issue. 
    * This should be reserved for use by a world's code owner(s) on their relevant world or by core maintainers.
