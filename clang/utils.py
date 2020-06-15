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
