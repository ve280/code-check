# Code Check

This repository includes all static code analysis of projects in ve280. 
`clang` and its tools are used to perform the various code checks.
We are planing to embed these checks into JOJ (in the future).


## Prerequisite

We use `Python>=3.6` and `Clang>=6` to develop the tests.

On Ubuntu, install them with

```bash
sudo apt install python3 python3-pip
sudo apt install clang clang-tools clang-format clang-tidy
pip3 install -r requirements.txt
```

## Usage

### For Students

Directly run the code check by (p1 as example):

```bash
PYTHONPATH=. python3 p1/codestyle.py <your_project_dir>
```

### For TAs

First, download the zip of all submission of the project from JOJ, for example, `p1_records.zip`.

Second, uncompress the file with `preprocess/uncompress.py`.

```bash
python3 preprocess/uncompress.py p1_records.zip
```

At last, use the `checkall.py` to generate the result in a csv file (`p1_code_check.csv`):

```bash
python3 checkall.py p1 -j 1
```

NOTICE: there's a multi-thread bug in checkall.py so run with [-j 1]

## Clang Tidy Arguments

You can directly test `clang-tidy` warnings by
```bash
clang-tidy -config='{"Checks": "*,-android-*,-bugprone-bool-pointer-implicit-conversion,-bugprone-exception-escape,-cert-*,-cppcoreguidelines-*,-fuchsia-*,-google-*,google-default-arguments,google-explicit-constructor,google-runtime-operator,-hicpp-*,-llvm-*,-objc-*,-readability-else-after-return,-readability-implicit-bool-conversion,-readability-magic-numbers,-readability-named-parameter,-readability-simplify-boolean-expr,-readability-braces-around-statements,-readability-identifier-naming,-readability-function-size,-readability-redundant-member-init,-readability-isolate-declaration,-readability-redundant-control-flow,-misc-bool-pointer-implicit-conversion,-misc-definitions-in-headers,-misc-unused-alias-decls,-misc-unused-parameters,-misc-unused-using-decls,-modernize-*,-clang-diagnostic-*,-clang-analyzer-*,-zircon-*", "CheckOptions": [{"key": "misc-throw-by-value-catch-by-reference.CheckThrowTemporaries", "value": "0"}]}'  *.cpp  --
```


## General Styles

1) Appropriate use of indenting and white space
2) Program appropriately split into subroutines
3) Variable and function names that reflect their use
4) Informative comments at the head of each function.


