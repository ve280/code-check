# Project 5 Grading Criteria

## Composition
1. Correctness: 90%
2. Coding style: 10%


## Correctness [90 points]
The correctness score depends on how many test cases you pass on JOJ.

#### JOJ Test Cases
There are in total 14 pretest cases and some hidden cases.


## Coding style [10 points]

#### clang-check [3 points]
* **Length of functions** [3 point]

  Your main functions should be no longer than 100 lines and non-main functions should be no more than 150 lines.

  1. No long functions [3 point]
  2. 1 long functions [2 points]
  3. 2 long functions [1 points]
  4. 3 or more long functions [0 points]

#### clang-tidy [4 points]
* **Number of warning types** [2 points]
  1. 0-10 types [2 points]
  2. 10-25 types [1 point]
  3. More than 25 types [0 points]

* **Number of warnings** [2 points]
  1. 0-2 warnings [2 points]
  2. 2-5 warnings [1 point]
  3. More than 5 warnings [0 points]

#### Header file usage check [3 points]

Deduction is applied for usage of some header files that are not allowed.

- One point deduction for each appearance of a header file that is not allowed
- Allowed header file: 
  - \<iostream\>
  - \<string\>
  - \<sstream\>
  - \<cstdlib\>
  - \<algorithm\>
  - \<cassert\>


See clang-tidy flags in https://github.com/ve280/code-check/blob/master/clang/tidy.py
