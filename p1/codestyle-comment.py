#!/usr/bin/python3

import argparse
import os
import clang.check
import clang.tidy

def main(project_dir,silent=False):
    # get functions
    main_cpp_name="p1.cpp"
    main_cpp_path=os.path.join(project_dir,main_cpp_name)
    functions=clang.check.parse_functions(main_cpp_name,main_cpp_path,silent=silent)
    clang.check.parse_comments(functions,silent=silent)

    # initialize clang check
    clang_check_score=0
    subroutine_cnt=0
    light_commented_funtion_cnt=0
    heavy_commented_function_cnt=0

    for fn_prototype, fn in functions.items():
        # count subroutine
        if fn.name != 'main__':
            subroutine_cnt+=1
        # count comment
        comment_cnt=fn.prototype_comments+fn.body_comments
        if comment_cnt>=1:
            light_commented_funtion_cnt+=1
        if comment_cnt>=5:
            heavy_commented_function_cnt+=1
    
    # subroutine score
    if subroutine_cnt <=1:
        clang_check_score+=0
    elif subroutine_cnt<=3:
        clang_check_score+=1
    else:
        clang_check_score+=2

    # comment score
    if subroutine_cnt<=1:
        if heavy_commented_function_cnt>=1:
            clang_check_score+=2
    else:
        clang_check_score+=min(4,light_commented_funtion_cnt)

    # initialize clang tidy
    clang_tidy_score=0
    warning_types, warning_cnt = clang.tidy.parse_warnings(main_cpp_path,silent=silent)

    # warning type score
    if len(warning_types)<=2:
        clang_tidy_score+=2
    elif len(warning_cnt)<=5:
        clang_tidy_score+=1
    
    # warning cnt score
    if warning_cnt<=5:
        clang_tidy_score+=2
    elif warning_cnt<=11:
        clang_tidy_score+=1
    
    if not silent:
        print("\n")
        print("clang-check score: %d" %clang_check_score)
        print("clang-tidy score: %d" %clang_tidy_score)
    
# parse program args and call main
parser = argparse.ArgumentParser(description='Project 1 Code Checker.')
parser.add_argument('--silent', action='store_true')
parser.add_argument('project_dir', type=str, nargs=1)
args = parser.parse_args()
main(args.project_dir[0], silent=args.silent)