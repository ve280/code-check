import chardet
import re
import os
import shutil


def read_file(file_path, silent=False):
    with open(file_path, 'rb') as file:
        bytes_str = file.read()
        charset = chardet.detect(bytes_str)['encoding'] or 'utf-8'
        if not silent:
            print('%s: encoding: %s' % (file_path, charset))
        return bytes_str.decode(charset).split('\n')


def split_sources_headers(files):
    headers = []
    sources = []
    other = []
    for file in files:
        if re.findall(r'\.(h|hpp|hh|H|hxx|h\+\+)$', file):
            headers.append(file)
        elif re.findall(r'\.(c|cpp|cc|C|cxx|c\+\+)$', file):
            sources.append(file)
        else:
            other.append(file)
    return sources, headers, other


def build_full_paths(project_dir, files):
    return list(map(lambda x: os.path.join(project_dir, x), files))


def inject_driver(project_dir, driver_dir):
    if os.path.isdir(project_dir) and os.path.isdir(driver_dir):
        for file in os.listdir(driver_dir):
            shutil.copy2(os.path.join(driver_dir, file), os.path.join(project_dir, file))


def count_not_allowed_headers(project_dir, files, allowed_headers, silent=False):
    not_allowed_usage_count = 0
    for file in files:
        absolute_path = os.path.join(project_dir, file)
        with open(absolute_path, 'r', encoding='unicode_escape') as source_file:
            lines = source_file.readlines()
            for line in lines:
                for usage in re.findall(r'\s*#\s*include\s+<\s*[a-z]+\s*>\s*', line):
                    remove_right = re.split(r'\s*>\s*', usage)[0]
                    header_name = re.sub(r'\s*#\s*include\s+<\s*', '', remove_right)
                    if header_name not in allowed_headers:
                        not_allowed_usage_count += 1
                        if not silent:
                            print('Found not allowed header file at:\n\n{}\nin {}'.format(usage, file))
    return not_allowed_usage_count
