OpenJudge
=========

**Refactored!**

OpenJudge has been refactored to be faster and easier to set up! This
repository was about quick contests for small groups of 20-30 people. Somewhere
along the way, I faltered and it became bloated. It's back now in a form which
is fast and light.


Requirements
------------

- Python 3.5
- bottle.py


Why?
----

Explaining to other people how this is supposed to work was a pain. The philosophy now is

```bash
$ openjudge
```

What's Changed
--------------

- Each contest requires a new instance of openjudge
- For every contest create a directory called `ContestData`. This must have the following files in it.
    - `intro.txt`: This is the introduction that is displayed on the home page
- Within `ContestData` folders are created named `1`, `2`, `3`, `4`, `5` denoting question numbers.
- Each question number folder contains the files:
    - `statement.txt`: This contains the statement of the question
    - `i1`: This is the input provided to the program
    - `o1`: This is the expected output.
    - Multiple input-output pairs can be set up to have multiple test cases.
- `ContestData` must contain a single file called `wrappers.json` which contains commands for different
  languages that the judge supports. This must be valid JSON
- After this folder is set up, you can run `openjudge` in that folder and it will run as expected.


**A sample `ContestData` is provided in this repository**
