# Project 5 Grading Criteria - 20FA


## Composition
1. Correctness: 90%
2. Cleaner code style: 5%
3. Call center code style: 5%


## Correctness [90 points]

The correctness score depends on how many test cases you pass on JOJ.


## Code Style [5 points]

Same for both *cleaner.cpp* and *call.cpp*, each 5 points, in total 10 points.

#### clang-check [5 points]
* **Number of non-main functions** [1 point]  
  Your program should be split into at least 2 non-main functions.
  1. \>=2 subroutines [1 point]
  2. <2 subroutine [0 point]

* **Length of functions** [2 point]  
  Your main function should be < 100 lines and non-main functions should be < 150 lines.
  1. =0 long functions [2 point]
  2. \>=1 long functions [0 point]

* **Body comments** [2 point]  
  You should have your subroutines well commented. The length of subroutines // (the number of comments + 1) < 50.
  1. =0 poorly commented function [2 point]
  2. =1 poorly commented function [1 point]
  2. \>=2 poorly commented functions [0 point]


<!-- 20 SU
# Project 5 Grading Criteria


## Composition
1. Correctness: 90%
2. RPN code style: 5%
3. Cache code style: 5%


## Correctness [90 points]
The correctness score depends on how many test cases you pass on JOJ.


## Code Style [5 points]

Same for both *rpn.cpp* and *cache.cpp*, each 5 points, in total 10 points.

#### clang-check [3 points]
* **Number of non-main functions** [1 point]  
  Your program should be split into at least 2 non-main functions.
  1. \>=2 subroutines [1 point]
  2. <2 subroutine [0 point]

* **Length of functions** [1 point]  
  Your main function should be < 100 lines and non-main functions should be < 150 lines.
  1. =0 long functions [1 point]
  2. \>=1 long functions [0 point]

* **Body comments** [1 point]  
  You should have your subroutines well commented. The length of subroutines // (the number of comments + 1) < 50.
  1. =0 poorly commented function [1 point]
  2. \>=1 poorly commented functions [0 point]

#### clang-tidy [2 points]
* **Number of warning types** [1 point]
  1. 0-5 types [1 point]
  1. 6-10 types [0.5 point]
  2. \>10 types [0 point]

* **Number of warnings** [1 point]
  1. 0-2 warnings [1 point]
  2. 3-5 warnings [0.5 point]
  3. \>5 warnings [0 point]

See clang-tidy flags in https://github.com/ve280/code-check/blob/master/clang/tidy.py

-->

<!-- 
# Project 5 Grading Criteria


## Composition
1. Correctness: 90%
2. RPN coding style: 6%
2. Cache coding style: 4%


## Correctness [90 points]
The correctness score depends on how many test cases you pass on JOJ.


## RPN Coding Style [6 points]

For *rpn.cpp*

#### clang-check [4 points]
* **Number of non-main functions** [1 point]

  Your program should be split into at least 2 non-main functions.

  1. \>=2 subroutines [1 point]
  3. <2 subroutine [0 point]

* **Length of functions** [1 point]

  Your main function should be <= 50 lines and non-main functions should be <= 150 lines.

  1. No long functions [1 point]
  3. \>=1 long functions [0 point]

* **Specification comments (REQUIRES, MODIFIES, EFFECTS)** [1 point]

  Your functions declarations should always contain specification comments.

  1. All declarations are well specified [1 point]
  2. \>=1 declarations that are poorly specified [0 point]

* **Body comments** [1 point]

  You should have your functions well commented. The length of function / the number of comments < 50.

  1. All functions are well commented [1 point]
  2. \>=1 functions that are poorly commented [0 point]

#### clang-tidy [2 points]
* **Number of warning types** [1 point]
  1. 0-5 types [1 point]
  1. 6-10 types [0.5 point]
  2. \>10 types [0 point]

* **Number of warnings** [1 point]
  1. 0-2 warnings [1 point]
  2. 3-5 warnings [0.5 point]
  3. \>5 warnings [0 point]


## Cache Coding style [4 points]

For *cache.cpp*

#### clang-check [2 points]

- **Number of non-main functions** [0.5 point]

  Your program should be split into at least 2 non-main functions for *cache.cpp*.

  1. \>=2 subroutines [0.5 point]
  2. <2 subroutine [0 point]

- **Length of functions** [0.5 point]

  Your main functions should be no longer than 90 lines and non-main functions should be no more than 100 lines.

  1. No long functions [0.5 point]
  2. \>=1 long functions [0 point]

- **Specification comments (REQUIRES, MODIFIES, EFFECTS)** [0.5 point]

  Your functions declarations should always contain specification comments.

  1. All declarations are well specified [0.5 point]
  2. \>=1 declarations are poorly specified [0 point]

- **Body comments** [0.5 point]

  You should have your functions well commented. The length of all functions / the number of comments < 50.

  1. Functions are well commented [0.5 point]
  2. \>=1 functions that are poorly commented [0 point]

#### clang-tidy [2 points]

- **Number of warning types** [1 point]
  1. 0-5 types [1 point]
  1. 6-10 types [0.5 point]
  2. \>10 types [0 point]
- **Number of warnings** [1 point]
  1. 0-2 warnings [1 point]
  2. 3-5 warnings [0.5 point]
  3. \>5 warnings [0 point]



See clang-tidy flags in https://github.com/ve280/code-check/blob/master/clang/tidy.py -->