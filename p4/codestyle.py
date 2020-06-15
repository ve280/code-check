#!/usr/bin/python3

import subprocess
import re
import shlex
import os
import argparse
from pprint import pprint
import chardet

from clang.utils import read_file

class FunctionDeclaration:
    function_declares = []

    def __init__(self, line):
        self.error = False

        # use regexp to parse the start and end line number
        function_range = re.findall(r":(\d+):", line)
        if len(function_range) < 1:
            self.error = True
            return
        self.start = int(function_range[0])

        # maybe a one-line function (declaration)
        if len(function_range) == 1:
            self.end = self.start
        else:
            self.end = int(function_range[1])

        # remove " static" at line end
        line = line.rstrip(' static')

        # use a trick to split the line
        splitter = shlex.shlex(line, posix=True)
        splitter.whitespace += ','
        splitter.whitespace_split = True
        args = list(splitter)
        if len(args) < 2:
            self.error = True
            return
        self.name = args[-2]

        # use another trick to split the args
        splitter = shlex.shlex(args[-1], posix=True)
        splitter.whitespace += ',()'
        splitter.whitespace_split = True
        args = list(splitter)
        if len(args) < 1:
            self.error = True
            return
        self.ret_type = args[0]
        self.args_type = args[1:]
        self.id = len(FunctionDeclaration.function_declares)
        self.body = []
        FunctionDeclaration.function_declares.append(self)

    def set_body(self, lines):
        self.body = lines

    def __str__(self):
        return '%s %s(%s)' % (self.ret_type, self.name, ', '.join(self.args_type))

    @staticmethod
    def get_by_id(_id):
        return FunctionDeclaration.function_declares[_id]


class Function:
    def __init__(self, func_decl):
        self.func_declarations = [func_decl]
        self.prototype_comments = 0
        self.body_comments = 0
        self.name = func_decl.name
        self.prototype = str(func_decl)

    def add_declaration(self, func_decl):
        self.func_declarations.append(func_decl)

    def count_lines(self):
        return sum([func_decl.end - func_decl.start + 1 for func_decl in self.func_declarations])

    def __str__(self):
        return self.prototype



def main(project_dir, silent=False):
    main_cpp_name = 'p2.cpp'
    main_cpp_path = os.path.join(project_dir, main_cpp_name)
    main_cpp_found = False
    functions = {}
    clang_check_score = 6

    p = subprocess.Popen("clang-check -ast-dump %s --" % main_cpp_path,
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not silent:
        print('parsing function declarations:')
    while p.poll() is None:
        line = p.stdout.readline().decode('utf-8')
        if main_cpp_name in line:
            main_cpp_found = True
        if main_cpp_found and 'FunctionDecl' in line and 'line' in line:
            line = re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', line).strip()
            func_decl = FunctionDeclaration(line)
            if not func_decl.error:
                func_prototype = str(func_decl)
                if not silent:
                    print('[line %d-%d] %s' % (func_decl.start, func_decl.end, func_decl))
                if func_prototype not in functions:
                    functions[func_prototype] = Function(func_decl)
                else:
                    functions[func_prototype].add_declaration(func_decl)
            elif not silent:
                print('error occurred in %s', line)

    if not silent:
        print('\nparsing cpp file:')
    main_cpp_contents = read_file(main_cpp_path, silent=silent)
    for i, func_decl in enumerate(FunctionDeclaration.function_declares):
        if func_decl.end <= len(main_cpp_contents):
            if i > 1:
                start = max(FunctionDeclaration.get_by_id(i - 1).end, func_decl.start - 5)
            else:
                start = max(0, func_decl.start - 5)
            end = func_decl.end
            func_decl.set_body([(x, main_cpp_contents[x]) for x in range(start, end)])

    if not silent:
        print('\ncounting function lines:')

    for func_prototype, func in functions.items():
        if not silent:
            print(func)
            line_count = func.count_lines()
            print('total lines: %d' % line_count)
            if line_count > 50 and clang_check_score > 0:
                clang_check_score -= 1

    if not silent:
        print('\nclang-check score: %d' % clang_check_score)

    clang_tidy_warnings = {}
    clang_tidy_warnings_count = 0
    clang_tidy_score = 0
    p = subprocess.Popen("clang-tidy %s -checks=-*,misc-*,performance-*,clang-analyzer-*,"
                         "readability-function-size,readability-identifier-naming,readability-named-parameter,"
                         "readability-redundant-*,readability-simplify-boolean-expr,readability-mis*,"
                         "--extra-arg='-fno-color-diagnostics' --"
                         % main_cpp_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not silent:
        print('\nparsing clang-tidy results:')
    while p.poll() is None:
        line = p.stdout.readline().decode('utf-8')
        line = re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', line).strip()
        res = re.findall(r'warning:.*?\[(.*?)\]', line)
        if res:
            if res[0] in clang_tidy_warnings:
                clang_tidy_warnings[res[0]] += 1
            else:
                clang_tidy_warnings[res[0]] = 1
            clang_tidy_warnings_count += 1
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


parser = argparse.ArgumentParser(description='Project 2 Code Style Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)
