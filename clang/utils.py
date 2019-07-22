import chardet
import re
import os


def read_file(file_path, silent=False):
    with open(file_path, 'rb') as file:
        bytes_str = file.read()
        charset = chardet.detect(bytes_str)['encoding']
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
