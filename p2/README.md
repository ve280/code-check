# Project 2 Grading Criteria


## Composition
1. Correctness: 85%
2. Coding style: 15%


## Correctness [85 points]
The correctness score depends on how many test cases you pass on JOJ.

## Coding style [15 points]
### clang-check [6 points]

- **Number of non-main functions** [3 points]
  - Your program should be split into at least 12 non-main functions.
    1. 12 or more subroutines [3 points]
    2. 8-11 subroutines [2 points]
    3. 4-7 subroutine [1 point]
    4. 0-3 subroutine [0 point]

- **Length of functions** [3 points]
    - Your main functions should be no longer than 100 lines and non-main functions should be no more than 150 lines.
        - 1 point deduction for each function that exceeds 100 lines
 
### clang-tidy [4 points]

`clang-tidy` is used to check general style. A report made up of intolerable warnings 
will be generated and we will count the numbers and types of the warnings and give a deduction.

- **Warning types (2 pts)**
    - For the types of warnings generated,
        + 0-3 types of warnings generated [2 points]
        + 4-6 types of warnings generated [1 mark]
        + 7+ types of warnings generated [0 mark]
- **Warning counts (2 pts)**
    -   For the number of warnings generated,
        + 0-10 warnings generated [2 points]
        + 11-25 warnings generated [1 mark]
        + 26+ warnings generated [0 mark]

See clang-tidy flags in https://github.com/ve280/code-check/blob/master/clang/tidy.py

### header file usage check [5 points]
Deduction is applied for usage of some header files that are not allowed.
- one point deduction for each appearance of a header file that is not allowed