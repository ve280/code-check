#!/usr/bin/python3

import os
import argparse
from pprint import pprint

import clang.check
import clang.tidy
import clang.format


def main(project_dir, silent=False):
    files = ['world_type.h', 'simulation.cpp', 'p3.cpp', 'simulation.h']
    format_dir = os.path.join(project_dir, 'formatted')

    clang.format.generate_formatted_files(project_dir, format_dir, files, silent=silent)

    clang_check_score = 0

    functions = clang.check.parse_functions_new(format_dir, files, silent=silent)
    clang.check.parse_comments(functions, silent=silent)

    subroutine_count = 0
    long_function_count = 0

    for func_prototype, func in functions.items():
        if func.name != 'main' and func.len >= 1:
            subroutine_count += 1
        if func.len >= 120:
            long_function_count += 1

    clang_check_score += min(3, subroutine_count // 5)
    clang_check_score += max(0, 3 - long_function_count)

    if not silent:
        print('\nsubroutines: %d, long functions: %d' % (subroutine_count, long_function_count))
        print('clang-check score: %d' % clang_check_score)

    clang_tidy_warnings, clang_tidy_warnings_count = clang.tidy.parse_warnings_new(format_dir, files, silent=silent)
    clang_tidy_score = 0

    if clang_tidy_warnings_count <= 10:
        clang_tidy_score += 2
    elif clang_tidy_warnings_count <= 25:
        clang_tidy_score += 1
    if len(clang_tidy_warnings) <= 3:
        clang_tidy_score += 2
    elif len(clang_tidy_warnings) <= 6:
        clang_tidy_score += 1
    if not silent:
        pprint(clang_tidy_warnings)
        print('\nclang-tidy score: %d' % clang_tidy_score)

    if silent:
        print('%d,%d' % (clang_check_score, clang_tidy_score))


parser = argparse.ArgumentParser(description='Project 3 Code Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)
