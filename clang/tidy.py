import re
import subprocess
import json

from clang.utils import split_sources_headers, build_full_paths

# ported from CLion, remove modernize-*, cert-*, hicpp-*
clang_tidy_checks = {'Checks': ','.join([
    "*",
    "-android-*",
    "-bugprone-bool-pointer-implicit-conversion",
    "-bugprone-exception-escape",
    "-cert-*",
    "-cppcoreguidelines-avoid-goto",
    "-cppcoreguidelines-avoid-magic-numbers",
    "-cppcoreguidelines-no-malloc",
    "-cppcoreguidelines-owning-memory",
    "-cppcoreguidelines-pro-bounds-array-to-pointer-decay",
    "-cppcoreguidelines-pro-bounds-constant-array-index",
    "-cppcoreguidelines-pro-bounds-pointer-arithmetic",
    "-cppcoreguidelines-pro-type-const-cast",
    "-cppcoreguidelines-pro-type-cstyle-cast",
    "-cppcoreguidelines-pro-type-reinterpret-cast",
    "-cppcoreguidelines-pro-type-union-access",
    "-cppcoreguidelines-pro-type-vararg",
    "-cppcoreguidelines-pro-type-member-init",
    "-cppcoreguidelines-special-member-functions",
    "-cppcoreguidelines-avoid-c-arrays",
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
    "-misc-bool-pointer-implicit-conversion",
    "-misc-definitions-in-headers",
    "-misc-unused-alias-decls",
    "-misc-unused-parameters",
    "-misc-unused-using-decls",
    "-modernize-*",
    "-clang-diagnostic-*",
    "-clang-analyzer-*",
    "-zircon-*",
]), 'CheckOptions': []}

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
