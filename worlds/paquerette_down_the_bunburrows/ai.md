AI usage disclosure
===================

- AI was used in a limited way.
- AI tooling used (Comprehensive, but only to the best of our knowledge):
  - Claude
- Logic, regions, rules and options are generally designed and written by hand.
- AI has so far been used for:
  - Minor revisions and bugfixes.
  - Better understanding of Archipelago conventions and the API.
  - Documentation updates.
  - Automated / AI code reviews.
    - Note: Automated review is exclusively for faster iteration, and NEVER replaces manual review, testing, etc.
- All AI based changes have been reviewed and tested by maintainers before release.
- No AI-generated media (e.g. art, sound, or music) is included.


Contributing with AI
--------------------

Contributors should keep these rules in mind, to limit what is considered acceptable AI usage.

- Acceptable:
  - Minor edits and trivial / menial updates.
  - Debugging, bug hunting and bug fixing.
  - Self-initiated AI code review.
  - Dispatching automated tests.
  - Generating minor and manually reviewed documentation updates.
  - Research into this AP World's contents and behaviors.
  - Features when carefully and intentionally directed by developers.
- Unacceptable:
  - AI dictating design and architecture
  - Fully undirected feature implementations
  - Being unable to describe and defend the reasoning of your proposed changes, from a code level not a feature level.
  - AI-generated media (e.g. art, sound, or music).
  - Large, sweeping AI-generated refactors.
- Developers making changes that include AI-generated content or have used AI tooling must abide the following:
  - The pull request should describe which tools were involved, and how.
  - The pull request should update the above AI usage disclosure if any usage is not currently listed
  - You are responsible for reviewing and testing everything you submit.
  - All new logic must be checked against the actual game.
