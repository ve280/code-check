# Project 4 Line Check
This part is for checking how many lines you have in each function of `binaryTree.cpp`.

## Grading
The line check part will count as `10 points` in your final score of project 4. Each function longer than 10 lines will lead to 2 points' deduction. If you have greater than or equal to 5 functions longer than 10 lines, all 10 points will be deducted.

We will count how many lines you have in each function by counting the number of `';'`s.

## Self-check

1. Please download **the new version of `clang` folder here** as well as the script `lineCheck.py`. (For the code style part, please use the old one.)

2. Your working directory should look like this:

    ``` bash
    $ ls
    clang lineCheck.py sol
    ```
    Here `sol` is the directory where your solutions are in.

3. Execution:

    ``` bash
    python3 lineCheck.py sol
    ```
4. results:

    If everything goes fine, the last 2 lines of the output should be like
    ```
    long functions: 0
    function length score: 10
    ``` 
