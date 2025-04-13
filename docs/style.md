# Style Guide

## Generic

* This guide can be ignored for data files that are not to be viewed in an editor.
* 120 character per line for all source files.
* Avoid white space errors like trailing spaces.

## Python Code

* We mostly follow [PEP8](https://peps.python.org/pep-0008/). Read below to see the differences.
* 120 characters per line. PyCharm does this automatically, other editors can be configured for it.
* Strings in core code will be `"strings"`. In other words: double quote your strings.
* Strings in worlds should use double quotes as well, but imported code may differ.
* Prefer [format string literals](https://peps.python.org/pep-0498/) over string concatenation,
  use single quotes inside them: `f"Like {dct['key']}"`
* Use type annotations where possible for function signatures and class members.
* Use type annotations where appropriate for local variables (e.g. `var: List[int] = []`, or when the
  type is hard or impossible to deduce.) Clear annotations help developers look up and validate API calls.
* If a line ends with an open bracket/brace/parentheses, the matching closing bracket should be at the
  beginning of a line at the same indentation as the beginning of the line with the open bracket.
  ```python
  stuff = {
      x: y
      for x, y in thing
      if y > 2
  }
  ```
* New classes, attributes, and methods in core code should have docstrings that follow
  [reST style](https://peps.python.org/pep-0287/).
* Worlds that do not follow PEP8 should still have a consistent style across its files to make reading easier.

## Markdown

* We almost follow [Google's styleguide](https://google.github.io/styleguide/docguide/style.html).
  Read below for differences.
* For existing documents, try to follow its style or ask to completely reformat it.
* 120 characters per line.
* One space between bullet/number and text.
* No lazy numbering.

## HTML

* Indent with 2 spaces for new code.
* kebab-case for ids and classes.

## CSS

* Indent with 2 spaces for new code.
* `{` on the same line as the selector.
* No space between selector and `{`.

## JS

* Indent with 2 spaces.
* Indent `case` inside `switch ` with 2 spaces.
* Use single quotes.
* Semicolons are required after every statement.
