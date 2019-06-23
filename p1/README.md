# Code Check for Project 1

## Usage

```bash
codestyle.py [-v/--verbose] <project_dir>
```

Use the verbose option to print detailed information about the checks

## Checks and Grading Policy

### clang-check [6 marks]

`clang-check` is used to generate the ast tree from the source file `p1.cpp` and 
check general style 1) and 4).

First, we use the `-ast-dump` argument to find the existence of subroutines (functions)
and their range.

Second, based on the ranges, we try to find whether there are informative comments 
at the head of each function (or in the body of the function).

The detailed grading policy is:
+ there are 2-3 subroutines [1 mark]
+ there are 4+ subroutines [1 mark]
+ there is at least one line of comment in any function [at most 4 marks]

For those who only have 0-1 subroutines:
+ there are 5+ lines of comments in any function [1 mark]

For example, if you only have a `main` function, with 5 lines of comments in it, 
you will get 2 marks for this part.


### clang-tidy [4 marks]

`clang-tidy` is used to check general style 3). A report consists of intolerable warnings 
is generated and we will count the numbers and types of the warnings and give a deduction.

The detailed grading policy is:




## Contributors

Designed by Yihao Liu ([tc-imba](https://github.com/tc-imba))

`clang-tidy` tested by Xiaohan Fu ([Reapor-Yurnero](https://github.com/Reapor-Yurnero))
