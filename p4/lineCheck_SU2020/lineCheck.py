#!/usr/bin/python3

import os
import argparse
from pprint import pprint

import clang.check
import clang.tidy
import clang.format


def main(project_dir, silent=False):
    # Formatting initialization
    files = ['binaryTree.cpp', 'binaryTree.h']
    format_dir = os.path.join(project_dir, 'formatted')

    # Clang checkings
    clang.format.generate_formatted_files(project_dir, format_dir, files, silent=silent)
    clang_check_score = 0
    long_function_count = 0

    functions = clang.check.parse_functions_new(format_dir, files, silent=silent)
    clang.check.parse_comments(functions, silent=silent)
    for func_prototype, func in functions.items():

        # Requirement: Non-main functions should be no longer than 10 physical lines.
        if func.name != 'main' and func.len >= 10:
            long_function_count += 1

    clang_check_score = 10-long_function_count*2
    if clang_check_score < 0:
        clang_check_score = 0


    if not silent:
        print('long functions: %d'% long_function_count)
        print('function length score: %d' % clang_check_score)

    if silent:
        print('function length score: %d' % clang_check_score)


parser = argparse.ArgumentParser(description='Project 2 Code Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)
