import os
import re
import shlex
import subprocess

from clang.utils import read_file, split_sources_headers, build_full_paths


class FunctionDeclaration:
    function_declares = []

    def __init__(self, line, file=''):
        self.file = file
        self.error = False

        # use regexp to parse the start and end line number
        function_range = re.findall(r"<(.*?)>", line)
        if not function_range:
            self.error = True
            return

        function_range = re.findall(r"[^l0-9]:(\d+)", function_range[0])
        if len(function_range) < 1:
            self.error = True
            return
        self.start = int(function_range[0])

        # maybe a one-line function (declaration)
        if len(function_range) == 1:
            self.end = self.start
        else:
            self.end = int(function_range[1])

        # simply assume one line definition / declaration
        self.len = self.end - self.start

        # use a trick to split the line
        splitter = shlex.shlex(line, posix=True)
        splitter.whitespace += ','
        splitter.whitespace_split = True
        args = list(splitter)
        if len(args) < 2:
            self.error = True
            return
        if args[-1] == 'static':
            self.static = True
            if len(args) < 3:
                self.error = True
                return
            self.name = args[-3]
            splitter = shlex.shlex(args[-2], posix=True)
        else:
            self.static = False
            self.name = args[-2]
            splitter = shlex.shlex(args[-1], posix=True)

        if self.name == 'main':
            self.name += '__' + file

        # use another trick to split the args
        splitter.whitespace = ',()'
        splitter.whitespace_split = True
        args = list(splitter)
        if len(args) < 1:
            self.error = True
            return
        self.ret_type = args[0].strip()
        self.args_type = list(map(lambda x: x.strip(), args[1:]))
        self.id = len(FunctionDeclaration.function_declares)
        self.body = []
        FunctionDeclaration.function_declares.append(self)

    def calculate_length(self, lines):
        self.len = 0
        block_comment = False
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            left_block = len(re.findall(r'/\*', line))
            right_block = len(re.findall(r'\*/', line))
            if left_block > right_block:
                if not line.startswith('/*'):
                    self.len += 1
                block_comment = True
            elif left_block < right_block:
                if not line.endswith('*/'):
                    self.len += 1
                block_comment = False
            elif block_comment or line.startswith('//'):
                continue
            else:
                self.len += 1
        self.len = max(0, self.len - 1)

    def set_body(self, lines):
        self.body = lines

    def __str__(self):
        prefix = self.static and 'static ' or ''
        return '%s%s %s(%s)' % (prefix, self.ret_type, self.name, ', '.join(self.args_type))

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
        self.len = 0

    def add_declaration(self, func_decl):
        self.func_declarations.append(func_decl)

    def calculate_length(self):
        self.len = 0
        for func_decl in self.func_declarations:
            self.len += func_decl.len

    def analyze_comments(self):
        self.prototype_comments = 0
        self.body_comments = 0

        def add_comment(line, is_prototype):
            if not block_comment:
                line = ''.join(re.findall(r'//(.+)', line, re.DOTALL))
            line = re.sub(r'[/*\s]', '', line)
            if len(line) > 5:
                if is_prototype:
                    self.prototype_comments += 1
                else:
                    self.body_comments += 1

        for func_decl in self.func_declarations:
            is_prototype = func_decl.start == func_decl.end
            block_comment = False
            for i, line in func_decl.body:
                line = line.strip()
                if len(line) == 0:
                    continue
                left_block = len(re.findall(r'/\*', line))
                right_block = len(re.findall(r'\*/', line))
                if left_block > right_block:
                    block_comment = True
                    add_comment(line, is_prototype)
                elif left_block < right_block:
                    add_comment(line, is_prototype)
                    block_comment = False
                elif block_comment:
                    add_comment(line, is_prototype)
                elif left_block == right_block and left_block > 0:
                    block_comment = True
                    add_comment(line, is_prototype)
                    block_comment = False
                elif '//' in line:
                    line = line[line.find('//'):]
                    add_comment(line, is_prototype)

    def __str__(self):
        return self.prototype


def parse_functions_new(project_dir, files, silent=False, functions=None):
    if not functions:
        functions = dict()

    split_sources_headers(files)
    sources, headers, _ = split_sources_headers(files)
    files = sources + headers
    sources_path = build_full_paths(project_dir, sources)
    files_path = build_full_paths(project_dir, files)
    p = subprocess.Popen("clang-check -ast-dump %s --extra-arg='-fno-color-diagnostics' --"
                         % ' '.join(sources_path), shell=True, stdout=subprocess.PIPE,
                         stderr=silent and subprocess.PIPE or None)

    current_file = None

    if not silent:
        print('\nparsing function declarations:')

    func_decl_lines = []

    while p.poll() is None:
        line = p.stdout.readline().decode('utf-8').strip()
        result = re.findall(r'<(?!(line|col))(.*?), (line|col):.*?>', line)
        if result:
            file_name = result[0][1]
            flag = False
            for i, file_path in enumerate(files_path):
                if file_path in file_name:
                    current_file = files[i]
                    flag = True
                    break
            if not flag:
                current_file = None

        decl = 'FunctionDecl' in line \
               or 'CXXConstructorDecl' in line \
               or 'CXXDestructorDecl' in line \
               or 'CXXMethodDecl' in line
        if current_file and ' default ' not in line and decl:
            line = line.strip()
            func_decl_lines.append((line, current_file))

    file_func_decls = {x: [] for x in files}

    for line, file in func_decl_lines:
        func_decl = FunctionDeclaration(line, file)
        if not func_decl.error:
            func_prototype = str(func_decl)
            if not silent:
                print('[%s:%d-%d] %s' % (func_decl.file, func_decl.start, func_decl.end, func_decl))
            if func_prototype not in functions:
                functions[func_prototype] = Function(func_decl)
            else:
                functions[func_prototype].add_declaration(func_decl)
            file_func_decls[file].append(func_decl)
        elif not silent:
            print('error occurred in %s' % line)

    if not silent:
        print('\nparsing cpp files:')

    for i, file in enumerate(files):
        try:
            file_contents = read_file(files_path[i], silent=silent)
            func_decls = sorted(file_func_decls[file], key=lambda x: x.start)
            for j, func_decl in enumerate(func_decls):
                if func_decl.end <= len(file_contents):
                    """
                    if j > 0:
                        start = max(func_decls[j - 1].end, func_decl.start - 20)
                    else:
                        start = max(0, func_decl.start - 20)
                    end = min(func_decl.end, len(file_contents) - 1)
                    """
                    start = func_decl.start - 2
                    end = func_decl.end
                    while file_contents[start].startswith('/') or "*" in file_contents[start]:
                        if start == 0:
                            break
                        start -= 1
                    while file_contents[end].startswith('/') or "*" in file_contents[start]:
                        if end == len(file_contents) - 1:
                            break
                        end += 1
                    func_decl.calculate_length(file_contents[func_decl.start:end + 1])
                    func_decl.set_body([(x, file_contents[x]) for x in range(start, end + 1)])
        except Exception as e:
            if not silent:
                print(e.args)

    for function in functions.values():
        function.calculate_length()

    return functions


def parse_functions(main_cpp_name, main_cpp_path, silent=False):
    p = subprocess.Popen("clang-check -ast-dump %s --extra-arg='-fno-color-diagnostics' --"
                         % main_cpp_path, shell=True, stdout=subprocess.PIPE)
    main_cpp_found = False
    functions = {}

    if not silent:
        print('\nparsing function declarations:')
    while p.poll() is None:
        line = p.stdout.readline().decode('utf-8')
        if main_cpp_name in line:
            main_cpp_found = True
        if main_cpp_found and 'FunctionDecl' in line and 'line' in line:
            line = line.strip()
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
                start = max(FunctionDeclaration.get_by_id(i - 1).end, func_decl.start - 20)
            else:
                start = max(0, func_decl.start - 20)
            end = func_decl.end
            func_decl.set_body([(x, main_cpp_contents[x]) for x in range(start, end)])

    return functions


def parse_comments(functions, silent=False):
    if not silent:
        print('\nparsing function comments:')
    for func_prototype, func in functions.items():
        if func.name == "inline":
            continue
        func.analyze_comments()
        if not silent:
            print(func)
            print('declarations: %d, body length: %d, prototype comments: %d, body comments: %d'
                  % (len(func.func_declarations), func.len, func.prototype_comments, func.body_comments))
