#!/usr/bin/python3

import os
import argparse
from pprint import pprint

import clang.check
import clang.tidy
import clang.format


def main(project_dir, silent=False):
    # params
    clang_check_score = 0
    # mute clang-tidy check
    # clang_tidy_score = 0

    files_total = [['call.cpp'], ['cleaner.cpp']]
    main_function_name_total = ['main__call.cpp', 'main__cleaner.cpp']

    for i in range(len(files_total)):
        files = files_total[i]
        main_function_name = main_function_name_total[i]
        subroutine_count = 0
        long_function_count = 0
        poorly_commented_cnt = 0

        # --------------------------- clang-check ---------------------------
        # parse and record error
        functions = clang.check.parse_functions_new(project_dir, files, silent=silent)
        clang.check.parse_comments(functions, silent=silent)
        for func_prototype, func in functions.items():
            # check 1: update number of non-main functions
            if func.name != main_function_name:
                subroutine_count += 1
            # check 2: update number of long functions
            if (func.name == main_function_name and func.len >= 100) or (func.name != main_function_name and func.len >= 150):
                long_function_count += 1
                if not silent:
                    print("Long function:", func.name)
            # check 3: update number of poorly commented subroutine body
            if func.name == main_function_name:
                continue
            if func.len // (func.body_comments + 1) >= 50:
                poorly_commented_cnt += 1
                if not silent:
                    print("Poorly commented subroutine body:", func.name, func.len, func.body_comments)

        # clang-check score
        if subroutine_count >= 2:
            clang_check_score += 1
        if long_function_count == 0:
            clang_check_score += 2
        if poorly_commented_cnt == 0:
            clang_check_score += 2
        elif poorly_commented_cnt == 1: # one poorly commented function
            clang_check_score += 1
        
        if not silent:
            print("--------------------")
            print("clang-check summary:")
            print("Number of subroutines:", subroutine_count)
            print("Number of long functions:", long_function_count)
            print("Number of poorly commented body:", poorly_commented_cnt)
            print("accumulative clang-check score:", clang_check_score)
            print("--------------------")

        # mute clang-tidy check
        # # --------------------------- clang-tidy ---------------------------
        # # parse and record error
        # clang_tidy_warnings, clang_tidy_warnings_count = clang.tidy.parse_warnings_new(project_dir, files, silent=silent)

        # # clang-tidy score
        # if clang_tidy_warnings_count <= 5:
        #     clang_tidy_score += 1
        # elif clang_tidy_warnings_count <= 10:
        #     clang_tidy_score += 0.5
        # if len(clang_tidy_warnings) <= 2:
        #     clang_tidy_score += 1
        # elif len(clang_tidy_warnings) <= 5:
        #     clang_tidy_score += 0.5
        # if not silent:
        #     print("--------------------")
        #     print("clang-tidy summary:")
        #     print("Number of warning types:", clang_tidy_warnings_count)
        #     print("Number of warnings:", len(clang_tidy_warnings))
        #     print("accumulative clang-tidy score:", clang_tidy_score)
        #     print("--------------------")

    # print final result
    # print('%d,%d' % (clang_check_score, clang_tidy_score))
    print('%d' % (clang_check_score))
    


# driver
parser = argparse.ArgumentParser(description='Project 5 Code Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)

# # get main comment count
# main_cpp_path = os.path.join(project_dir, main_cpp_name)
# main_function = clang.check.parse_functions(main_cpp_name, main_cpp_path, silent=silent)
# clang.check.parse_comments(main_function, silent=silent)
# main_comment_count = 0
# for func_prototype, func in main_function.items():
#     if func.name != 'main__':
#         continue
#     main_comment_count = func.body_comments
