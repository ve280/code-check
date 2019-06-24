# Code Check for Project 1

## Usage

```bash
python3 codestyle.py [-h] [--silent] project_dir
python3 recursion.py [-h] [--silent] project_dir
```

Use the silent option to batch all of the submissions.

## Checks and Grading Policy

### clang-check [6 marks]

`clang-check` is used to generate the ast tree from the source file `p2.cpp` and 
check number of lines in each function.

For each function that exceeds 50 lines, 1 point is deducted, until 6 such functions are found.


### clang-tidy [4 marks]

`clang-tidy` is used to check general style 3). A report consists of intolerable warnings 
is generated and we will count the numbers and types of the warnings and give a deduction.

The detailed grading policy is:

For the types of warnings generated,
+ 0-2 types of warnings generated [2 marks]
+ 3-5 types of warnings generated [1 mark]
+ 6+ types of warnings generated [0 mark]

For the number of warnings generated,
+ 0-5 warnings generated [2 marks]
+ 6-11 warnings generated [1 mark]
+ 12+ warnings generated [0 mark]

### networkx

`networkx` is used to check if each function implementation contains recursion. 

Firstly, we extract the function declarations and all function calls inside function definitions 
from the ast tree of `p1.cpp`. Each pair of defined function and helper function called inside 
definition is added as an edge to `networkx`'s graph.

Secondly, we use `networkx.simple_cycles` to find all recursive functions. This handles both 
```
void func() { func(); }
```
and
```
void func1() { func2(); }
void func2() { func1(); }
```

Thirdly, we check whether each function listed in `p2.h` calls any recursive function directly or 
indirectly. This is done by using `networkx.all_simple_paths`, with the function to be 
implemented as the `source`, and any recursive function as the `target`. 

If any `p2.h` function definition is found to contain no recursion, all points of JOJ test cases 
related to this function will be deducted. Additionally, we deduct one point from the `clang-check` 
section, since its code style doesn't meet the requirements either.


## Contributors

Designed by Zian Ke ([zianke](https://github.com/zianke))

`clang-tidy` tested by Xiaohan Fu ([Reapor-Yurnero](https://github.com/Reapor-Yurnero))
