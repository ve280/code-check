#!/usr/bin/python3

import tarfile
import zipfile
import os
import tempfile
import sys


def unzip(file, dest):
    print('unzip %s in %s' % (file, dest))
    if zipfile.is_zipfile(file):
        zf = zipfile.ZipFile(file, 'r')
        zf.extractall(dest)
        return 0
    else:
        print('failed', file=sys.stderr)
        return 1


def untar(file, dest):
    print('untar %s in %s' % (file, dest))
    if tarfile.is_tarfile(file):
        tf = tarfile.open(file, 'r')
        tf.extractall(dest)
        return 0
    else:
        print('failed', file=sys.stderr)
        return 1


def main(file):
    filename, _ = os.path.splitext(file)
    with tempfile.TemporaryDirectory() as tempdir:
        if unzip(file, tempdir) == 0:
            error = 0
            for file in os.listdir(tempdir):
                record_file = os.path.join(tempdir, file)
                record_filename, record_ext = os.path.splitext(file)
                record_dest = os.path.join(filename, record_filename)
                if record_ext == '.zip':
                    error += unzip(record_file, record_dest)
                elif record_ext == '.tar':
                    error += untar(record_file, record_dest)
            print('finished, with %d error(s)' % error)


if len(sys.argv) > 1:
    main(sys.argv[1])
else:
    print('usage: uncompress.py [filename]', file=sys.stderr)
