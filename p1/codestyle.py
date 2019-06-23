#!/usr/bin/python3

import subprocess
import re
import shlex
import os
import argparse

import chardet


class FunctionDeclaration:
    function_declares = []

    def __init__(self, line):
        self.error = False

        # use regexp to parse the start and end line number
        function_range = re.findall(r"line:(\d+)", line)
        if len(function_range) < 1:
            self.error = True
            return
        self.start = int(function_range[0])

        # maybe a one-line function (declaration)
        if len(function_range) == 1:
            self.end = self.start
        else:
            self.end = int(function_range[1])

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

    def analyze_comments(self):
        self.prototype_comments = 0
        self.body_comments = 0

        def add_comment(line):
            if not block_comment:
                line = ''.join(re.findall(r'//(.+)', line, re.DOTALL))
            line = re.sub(r'[/*\s]', '', line)
            if len(line) > 5:
                if state < 2:
                    self.prototype_comments += 1
                else:
                    self.body_comments += 1

        for func_decl in self.func_declarations:
            state = 0
            block_comment = False
            for i, line in func_decl.body:
                line = line.strip()
                if len(line) == 0:
                    if i > func_decl.start:
                        state += 1
                    continue
                left_block = len(re.findall(r'/\*', line))
                right_block = len(re.findall(r'\*/', line))
                if left_block > right_block:
                    block_comment = True
                    add_comment(line)
                elif left_block < right_block:
                    add_comment(line)
                    block_comment = False
                elif block_comment:
                    add_comment(line)
                elif line.startswith('//'):
                    add_comment(line)
                elif i > func_decl.start:
                    state += 1

    def __str__(self):
        return self.prototype


def read_file(file_path, silent=False):
    with open(file_path, 'rb') as file:
        bytes_str = file.read()
        charset = chardet.detect(bytes_str)['encoding']
        if not silent:
            print('encoding: %s' % charset)
        return bytes_str.decode(charset).split('\n')


def main(project_dir, silent=False):
    main_cpp_name = 'p1.cpp'
    main_cpp_path = os.path.join(project_dir, main_cpp_name)
    main_cpp_found = False
    functions = {}
    clang_check_score = 0
    clang_tidy_score = 0

    p = subprocess.Popen("clang-check-8 -ast-dump %s --" % main_cpp_path, shell=True, stdout=subprocess.PIPE)

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
    subroutine_count = 0
    one_line_comment_count = 0
    five_line_comment_count = 0
    for i, func_decl in enumerate(FunctionDeclaration.function_declares):
        if func_decl.end <= len(main_cpp_contents):
            if i > 1:
                start = max(FunctionDeclaration.get_by_id(i - 1).end, func_decl.start - 5)
            else:
                start = max(0, func_decl.start - 5)
            end = func_decl.end
            func_decl.set_body([(x, main_cpp_contents[x]) for x in range(start, end)])

    if not silent:
        print('\nparsing function comments:')

    for func_prototype, func in functions.items():
        func.analyze_comments()
        if not silent:
            print(func)
            print('declarations: %d, prototype comments: %d, body comments: %d'
                  % (len(func.func_declarations), func.prototype_comments, func.body_comments))

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
        print('\nclang_check_score: %d' % clang_check_score)


parser = argparse.ArgumentParser(description='Project 1 Code Checker.')
parser.add_argument('--silent', default=False, type=bool)
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)
