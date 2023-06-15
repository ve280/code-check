import os
import subprocess
import time


def generate_formatted_files(project_dir, target_dir, files, silent=False):
    if not silent:
        print('reformatting files:')

    os.makedirs(target_dir, exist_ok=True)
    for file in files:
        input_file = os.path.join(project_dir, file)
        output_file = os.path.join(target_dir, file)
        if not silent:
            print('%s => %s' % (input_file, output_file))
        with open(output_file, 'wb') as f:
            p = subprocess.run("clang-format -style=WebKit %s"
                               % input_file, shell=True, stdout=f,
                               stderr=silent and subprocess.PIPE or None)
            # while p.poll() is None:
            #     time.sleep(0.001)

    if not silent:
        print('')

# generate_formatted_files('/home/liu/SJTU/code-check/solution', '/home/liu/SJTU/code-check/solution/formatted',
#                          ['world_type.h', 'simulation.cpp', 'p3.cpp', 'simulation.h'])
