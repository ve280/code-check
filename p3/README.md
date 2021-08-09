# Project 3 Grading Criteria
This grading policy is adapted and revised from project 2.

## Running `codestyle.py`
This script is for checking 4 files: `deck.cpp`, `hand.cpp`, `player.cpp` and `blackjack.cpp`. Do not worry about errors like "card.h not found". This is just cerr output of clang-check which will not lead to any deduction (since we will not check the already implemented files). If you want to mute those errors, run with
```bash
python3 codestyle.py <directory> 2>/dev/null
```

## Composition
1. Correctness: 85%
2. Coding style: 15%


## Correctness [85 points]
The correctness score depends on how many test cases you pass on JOJ.

#### JOJ Test Cases
There are in total 340 cases, each one is worth 0.25.


## Coding style [15 points]

#### clang-check [5 points]
* **Length of functions** [2 point]

  Your main functions should be no longer than 100 lines and non-main functions should be no more than 150 lines.

  1. No long functions [2 point]
  2. 1 long functions [1 points]
  3. 2 or more long functions [0 points]

* **Specification comments (REQUIRES, MODIFIES, EFFECTS)** [1.5 points]

  Your functions declarations should always contain specification comments.

  1. All declarations are well specified [1.5 points]
  2. 1 declaration are poorly specified [1 point]
  3. 2 declarations are poorly specified [0.5 points]
  4. 3 or more declarations are poorly specified [0 points]

* **Body comments** [1.5 points]

  You should have your functions well commented. The length of function // the number of comments < 50.

  1. All function are well commented [1.5 points]
  2. 1 function are poorly commented [1 point]
  3. 2 function are poorly commented [0.5 points]
  4. 3 or more function are poorly commented [0 points]

The total clang-check score will round **down** to the nearest integer, *i.e.* 3.5 will round down to 3.

#### clang-tidy [5 points]
* **Number of warning types** [3 points]
  1. 0-5 types [3 points]
  2. 5-10 types [2 points]
  3. 10-25 types [1 point]
  4. More than 25 types [0 points]

* **Number of warnings** [2 points]
  1. 0-2 warnings [2 points]
  2. 2-5 warnings [1 point]
  3. More than 5 warnings [0 points]

#### Header file usage check [5 points]

Deduction is applied for usage of some header files that are not allowed.

- One point deduction for each appearance of a header file that is not allowed
- Allowed header file: 

See clang-tidy flags in https://github.com/ve280/code-check/blob/master/clang/tidy.py
