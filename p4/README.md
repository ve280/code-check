# Project 4 Grading Criteria


## Composition
1. Correctness: 80%
2. General coding style: 10%
3. `BinaryTree.cpp` check (number of lines in each function definition): 10%


## Correctness [80 points]
The correctness score depends on how many test cases you pass on JOJ.


## Coding style [10 points]

#### clang-check [5 points]
* **Number of non-main functions** [1 point]

  Your program should be split into at least 3 non-main functions for *compress.cpp* and *decompress.cpp*.

  1. 2 or more subroutines [1 point]
  2. 1 subroutines [0.5 points]
  3. 0 subroutine [0 points]

* **Length of functions** [1 point]

  Your main functions should be no longer than 50 lines and non-main functions should be no more than 150 lines.

  1. No long functions [1 point]
  2. 1 long functions [0.5 points]
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

See clang-tidy flags in https://github.com/ve280/code-check/blob/master/clang/tidy.py
