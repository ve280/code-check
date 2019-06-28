#!/usr/bin/python3

import os
import argparse
from pprint import pprint

import clang.check
import clang.tidy


def main(project_dir, silent=False):
    main_cpp_name = 'p1.cpp'
    main_cpp_path = os.path.join(project_dir, main_cpp_name)
    clang_check_score = 0

    functions = clang.check.parse_functions(main_cpp_name, main_cpp_path, silent=silent)
    clang.check.parse_comments(functions, silent=silent)

    subroutine_count = 0
    one_line_comment_count = 0
    five_line_comment_count = 0

    for func_prototype, func in functions.items():
        comment_count = func.prototype_comments + func.body_comments

        if func.name != 'main':
            subroutine_count += 1
        if comment_count >= 1:
            one_line_comment_count += 1
        if comment_count >= 5:
            five_line_comment_count += 1

    if subroutine_count <= 1:
        if five_line_comment_count > 0:
            clang_check_score += 1
        clang_check_score += min(2, one_line_comment_count)
    else:
        clang_check_score += 1
        if subroutine_count >= 4:
            clang_check_score += 1
        clang_check_score += min(4, one_line_comment_count)

    if not silent:
        print('\nclang-check score: %d' % clang_check_score)

    clang_tidy_warnings, clang_tidy_warnings_count = clang.tidy.parse_warnings(main_cpp_path, silent=silent)
    clang_tidy_score = 0

    if clang_tidy_warnings_count <= 5:
        clang_tidy_score += 2
    elif clang_tidy_warnings_count <= 11:
        clang_tidy_score += 1
    if len(clang_tidy_warnings) <= 2:
        clang_tidy_score += 2
    elif len(clang_tidy_warnings) <= 5:
        clang_tidy_score += 1
    if not silent:
        pprint(clang_tidy_warnings)
        print('\nclang-tidy score: %d' % clang_tidy_score)

    if silent:
        print('%d,%d' % (clang_check_score, clang_tidy_score))


parser = argparse.ArgumentParser(description='Project 1 Code Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)
