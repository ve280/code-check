import re
import subprocess
import json

from clang.utils import split_sources_headers, build_full_paths

# ported from CLion, remove modernize-*, cert-*, hicpp-*, cppcoreguidelines-*
clang_tidy_checks = {'Checks': ','.join([
    "*",
    "-android-*",
    "-bugprone-bool-pointer-implicit-conversion",
    "-bugprone-exception-escape",
    "-cert-*",
    "-cppcoreguidelines-*",
    "-fuchsia-*",
    "-google-*",
    "google-default-arguments",
    "google-explicit-constructor",
    "google-runtime-operator",
    "-hicpp-*",
    "-llvm-*",
    "-objc-*",
    "-readability-else-after-return",
    "-readability-implicit-bool-conversion",
    "-readability-magic-numbers",
    "-readability-named-parameter",
    "-readability-simplify-boolean-expr",
    "-readability-braces-around-statements",
    "-readability-identifier-naming",
    "-readability-function-size",
    "-readability-redundant-member-init",
    "-readability-isolate-declaration",
    "-readability-redundant-control-flow,"
    "-misc-bool-pointer-implicit-conversion",
    "-misc-definitions-in-headers",
    "-misc-unused-alias-decls",
    "-misc-unused-parameters",
    "-misc-unused-using-decls",
    "-modernize-*",
    "-clang-diagnostic-*",
    "-clang-analyzer-*",
    "-zircon-*",
]), 'CheckOptions': [{
    'key': 'misc-throw-by-value-catch-by-reference.CheckThrowTemporaries',
    'value': '0'
}]}

# print(json.dumps(clang_tidy_checks))


def parse_warnings_new(project_dir, files, silent=False):
    split_sources_headers(files)
    sources, headers, _ = split_sources_headers(files)
    sources_path = build_full_paths(project_dir, sources)
    p = subprocess.Popen("clang-tidy %s -config='%s' --extra-arg='-fno-color-diagnostics' --"
                         % (' '.join(sources_path), json.dumps(clang_tidy_checks)),
                         shell=True, stdout=subprocess.PIPE, stderr=silent and subprocess.PIPE or None)

    warnings = {}
    warnings_count = 0

    if not silent:
        print('\nparsing clang-tidy results:')
        print('Ignore the following warnings, if they are suspended.')
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


def parse_warnings(main_cpp_path, silent=False):
    p = subprocess.Popen("clang-tidy %s -checks=%s --extra-arg='-fno-color-diagnostics' --"
                         % (main_cpp_path, clang_tidy_checks),
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
