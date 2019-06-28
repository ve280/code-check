import chardet


def read_file(file_path, silent=False):
    with open(file_path, 'rb') as file:
        bytes_str = file.read()
        charset = chardet.detect(bytes_str)['encoding']
        if not silent:
            print('encoding: %s' % charset)
        return bytes_str.decode(charset).split('\n')
