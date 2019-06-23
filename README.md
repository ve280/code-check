# Code Check

This repository includes all static code analysis of projects in ve280. `clang` and its tools are used to perform the various code checks

## Prerequisite

We use `Python>=3.6` and `Clang>=8` to develop the tests.

On Ubuntu, install them with

```bash
sudo apt install python3 python3-pip
sudo apt install clang-8 clang-tools-8 clang-format-8 clang-tidy-8
pip3 install -r requirements.txt
```

## General Styles

1) appropriate use of indenting and white space
2) program appropriately split into subroutines
3) variable and function names that reflect their use
4) informative comments at the head of each function.


