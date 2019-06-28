#!/usr/bin/python3

import tarfile
import zipfile
import rarfile
import os
import tempfile
import sys


def unzip(file, dest):
    print('unzip %s in %s' % (file, dest))
    if zipfile.is_zipfile(file):
        zf = zipfile.ZipFile(file, 'r')
        zf.extractall(dest)
        chmod(dest, 0o644)
        return 0
    else:
        print('failed', file=sys.stderr)
        return 1


def untar(file, dest):
    print('untar %s in %s' % (file, dest))
    if tarfile.is_tarfile(file):
        tf = tarfile.open(file, 'r')
        tf.extractall(dest)
        chmod(dest, 0o644)
        return 0
    else:
        print('failed', file=sys.stderr)
        return 1


def unrar(file, dest):
    print('unrar %s in %s' % (file, dest))
    if rarfile.is_rarfile(file):
        rf = rarfile.RarFile(file, 'r')
        rf.extractall(dest)
        chmod(dest, 0o644)
        return 0
    else:
        print('failed', file=sys.stderr)
        return 1


def chmod(directory, mode):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.chmod(os.path.join(root, name), mode=mode)
        for name in dirs:
            os.chmod(os.path.join(root, name), mode=mode)


def main(file):
    filename, _ = os.path.splitext(file)
    with tempfile.TemporaryDirectory() as tempdir:
        if unzip(file, tempdir) == 0:
            error = 0
            success = 0
            for file in os.listdir(tempdir):
                record_file = os.path.join(tempdir, file)
                record_filename, record_ext = os.path.splitext(file)
                record_dest = os.path.join(filename, record_filename)
                if record_ext == '.zip':
                    if unzip(record_file, record_dest):
                        error += 1
                    else:
                        success += 1
                elif record_ext == '.tar':
                    if untar(record_file, record_dest):
                        error += 1
                    else:
                        success += 1
                elif record_ext == '.rar':
                    if unrar(record_file, record_dest):
                        error += 1
                    else:
                        success += 1
                else:
                    print('extension not supported', file=sys.stderr)
            print('finished, with %d success(es) and %d error(s)' % (success, error))


if len(sys.argv) > 1:
    main(sys.argv[1])
else:
    print('usage: uncompress.py [filename]', file=sys.stderr)
