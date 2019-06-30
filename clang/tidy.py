import re
import subprocess


def parse_warnings(main_cpp_path, silent=False):
    p = subprocess.Popen("clang-tidy %s -checks=-*,misc-*,performance-*,clang-analyzer-*,"
                         "readability-function-size,readability-identifier-naming,readability-named-parameter,"
                         "readability-redundant-*,readability-simplify-boolean-expr,readability-mis*,"
                         "--extra-arg='-fno-color-diagnostics' --"
                         % main_cpp_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    warnings = {}
    warnings_count = 0

    if not silent:
        print('\nparsing clang-tidy results:')
    while p.poll() is None:
        line = p.stdout.readline().decode('utf-8').strip()
        res = re.findall(r'warning:.*?\[(.*?)\]', line)
        if res:
            if res[0] in warnings:
                warnings[res[0]] += 1
            else:
                warnings[res[0]] = 1
            warnings_count += 1

    return warnings, warnings_count
