OpenJudge
=========

**Refactored!**

OpenJudge has been refactored to be faster and easier to set up! This
repository was about quick contests for small groups of 20-30 people. Somewhere
along the way, I faltered and it became bloated. It's back now in a form which
is fast and light.


Screenshot
----------

![OpenJudge mainscreen screenshot](screen.png)


Requirements
------------

- Python 3.5 `There is some subprocessing work which is only available 3.5 onwards`
- bottle.py ` This is the new website framework instead of Django`
- paste ` This is the new website server`


Why?
----

Explaining to other people how this is supposed to work was a pain. The philosophy now is

```bash
$ pip install openjudge
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

The `ContestData` folder must follow this tree:

```
▾ ContestData/
  ▾ 1/
      i1
      o1
      statement
  ▾ 2/
      i1
      o1
      statement
    intro.txt
    wrappers.json
```


**A sample `ContestData` is provided in this repository**


All the contest data is stored in a file called `contest.json` for ease of reading.


Scoring
-------

This is still the same. The score is determined by `(total - correct_valid) / total` attempts on a question by everyone at any given time. Only the first correct attempt by a person on a question counts for the `correct_valid`. Subsequent correct answers are considered wrong.

This leads to very few ties.


Todo
----

- [x] pip install
- [x] one command runnability
- [x] minimize dependencies
- [x] keep contest history
- [x] Login/Logout user system
- [x] Score Calculation
- [x] Leaderboard
- [ ] Contest Analysis


Benchmarks
----------

On running `siege -c 100 -t 1M -b http://127.0.0.1:8080` we get the following
results. Keep in mind that tis is over localhost with 100 concurrent users
hitting the site simultaneously without any delay.


```
Transactions:                  16403 hits
Availability:                 100.00 %
Elapsed time:                  59.44 secs
Data transferred:             112.46 MB
Response time:                  0.36 secs
Transaction rate:             275.96 trans/sec
Throughput:                     1.89 MB/sec
Concurrency:                   98.65
Successful transactions:       16404
Failed transactions:               0
Longest transaction:            7.52
Shortest transaction:           0.06

```
