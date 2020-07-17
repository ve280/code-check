#!/usr/bin/python3

import os
import argparse
from pprint import pprint

import clang.check
import clang.tidy
import clang.format


def main(project_dir, silent=False):
    # Formatting initialization
    files = ['binaryTree.cpp', 'compress.cpp', 'decompress.cpp']
    format_dir = os.path.join(project_dir, 'formatted')
    main_cpp_files = ['compress.cpp', 'decompress.cpp']

    # Clang checkings
    clang.format.generate_formatted_files(project_dir, format_dir, files, silent=silent)

    driver_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'driver')
    clang.utils.inject_driver(project_dir, driver_dir)
    clang.utils.inject_driver(format_dir, driver_dir)

    clang_check_score = 0
    subroutine_count = 0
    long_function_count = 0
    uncomment_prototype_cnt = 0
    poorly_commented_cnt = 0

    functions = clang.check.parse_functions_new(format_dir, main_cpp_files, silent=silent)
    clang.check.parse_comments(functions, silent=silent)
    for func_prototype, func in functions.items():
        mainfunc = (func.name == 'main__compress.cpp' or func.name == 'main__decompress.cpp')
        # Checkpoint 1: Main function length
        # Requirement: Main function should be no longer than 50 physical lines.
        if mainfunc:
            if func.func_declarations[0].end - func.func_declarations[0].start >= 50:
                long_function_count += 1

        # Checkpoint 2: Non-main function amount
        # Requirement: Program should be split into at least 2 non-main functions.
        if not mainfunc and func.len >= 1:
            subroutine_count += 1

        # Checkpoint 3: Non-main function length and amount
        # Requirement: Non-main functions should be no longer than 150 physical lines.
        if not mainfunc and func.len >= 150:
            long_function_count += 1

        # Checkpoint 4: Function declaration comments (REQUIRES, MODIFIES, EFFECTS)
        # Requirement: All functions should have RME in their declaration.
        if not mainfunc and func.prototype_comments == 0:
            tolerance = ['Exception_t', 'bool', 'operator', 'static', 'inline']
            flag = len(func.func_declarations)>1
            for entity in tolerance:
                if func.name == entity:
                    flag = False
                    break
            if flag:
                print("{} is not commented under declaration.".format(func.name))
                uncomment_prototype_cnt += 1

        # Checkpoint 5: Function body comments
        # Requirement: the length of function // the number of comments < 50.
        if func.body_comments == 0:
            if func.len >= 50:
                poorly_commented_cnt += 1
        elif func.len // func.body_comments >= 50:
            poorly_commented_cnt += 1

    clang_check_score += min(2, subroutine_count // 1)
    clang_check_score += max(0, 2 - long_function_count)
    clang_check_score += max(0, 3 - uncomment_prototype_cnt)
    clang_check_score += max(0, 3 - poorly_commented_cnt)
    clang_check_score //= 2

    if not silent:
        print('\nsubroutines: %d, \nlong functions: %d, \nuncomment declarations: %d, \npoorly commented functions: %d'
              % (subroutine_count, long_function_count, uncomment_prototype_cnt, poorly_commented_cnt))
        print('clang-check score: %d' % clang_check_score)

    clang_tidy_warnings, clang_tidy_warnings_count = clang.tidy.parse_warnings_new(project_dir, files, silent=silent)
    clang_tidy_score = 0

    # Checkpoint 6: Clang tidies
    # Requirement: Your program should be free of clang tidies.
    if clang_tidy_warnings_count <= 5:
        clang_tidy_score += 3
    elif clang_tidy_warnings_count <= 10:
        clang_tidy_score += 2
    elif clang_tidy_warnings_count <= 25:
        clang_tidy_score += 1

    if len(clang_tidy_warnings) <= 2:
        clang_tidy_score += 2
    elif len(clang_tidy_warnings) <= 5:
        clang_tidy_score += 1
    if not silent:
        pprint(clang_tidy_warnings)
        print('\nclang-tidy score: %d' % clang_tidy_score)
        print('\nTotal style score: %d' % (clang_tidy_score + clang_check_score))

    if silent:
        print('%d,%d' % (clang_check_score, clang_tidy_score))


parser = argparse.ArgumentParser(description='Project 4 Code Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)
