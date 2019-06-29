#!/usr/bin/python3

import subprocess
import re
import os
import argparse
from collections import defaultdict
import networkx as nx
import itertools


def main(project_dir, silent=False):
    funcs_to_test = ['size', 'memberOf', 'dot', 'isIncreasing', 'reverse', 'append', 'isArithmeticSequence',
                     'filter_odd', 'filter', 'unique', 'insert_list', 'chop', 'tree_sum', 'tree_search', 'depth',
                     'tree_max', 'traversal', 'tree_hasMonotonicPath', 'tree_allPathSumGreater', 'covered_by',
                     'contained_by', 'insert_tree']
    main_cpp_name = 'p2.cpp'
    main_cpp_path = os.path.join(project_dir, main_cpp_name)

    p = subprocess.Popen("clang-check -ast-dump %s --extra-arg='-fno-color-diagnostics' --" % main_cpp_path, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not silent:
        print('parsing function declarations and function calls:')

    ast = p.stdout.read().decode('utf-8')
    blocks = ast.split('FunctionDecl')[1:]
    func_calls_dict = defaultdict(set)
    edges = []
    for block in blocks:
        lines = block.split('\n')
        func_decl = re.findall(r"(\w+) '(?:.+?)'", lines[0])
        if not func_decl:
            continue
        func_decl = func_decl[0]

        for line in lines[1:]:
            func_call = re.findall(r"DeclRefExpr(?:.+?)Function 0x\w+ '(\w+)' '(?:.+?)'", line)
            if func_call:
                func_calls_dict[func_decl].add(func_call[0])

    for func_decl, func_calls in func_calls_dict.items():
        edges.extend([(func_decl, func_call) for func_call in func_calls])

    G = nx.DiGraph(edges)
    rec_funcs = set(itertools.chain.from_iterable((nx.simple_cycles(G))))

    non_rec_funcs = []
    for func in funcs_to_test:
        if func not in func_calls_dict:
            non_rec_funcs.append(func)
        else:
            is_rec = False
            for rec_func in rec_funcs:
                if func == rec_func or list(nx.all_simple_paths(G, source=func, target=rec_func)):
                    is_rec = True
                    break
            if not is_rec:
                non_rec_funcs.append(func)

    if silent:
        print(';'.join(non_rec_funcs))
    else:
        print('Non-recursive functions: %s' % non_rec_funcs)


parser = argparse.ArgumentParser(description='Project 2 Recursion Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)
