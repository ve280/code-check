import argparse
import csv
import os
import shutil
import subprocess
import multiprocessing


def check_one(project, checkers, uid, project_dir):
    result = [uid]
    for checker in checkers:
        checker_file = os.path.join(project, checker)
        p = subprocess.run("PYTHONPATH=. python3 %s %s --silent" % (checker_file, project_dir),
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result += p.stdout.decode().strip().split(',')
    print(result)
    return result


def inject_driver(project_dir, driver_dir):
    if os.path.isdir(project_dir) and os.path.isdir(driver_dir):
        for file in os.listdir(driver_dir):
            shutil.copy2(os.path.join(driver_dir, file), os.path.join(project_dir, file))


def main(project, jobs):
    records_dir = project + '_records'
    driver_dir = os.path.join(project, 'driver')
    # results_dir = project + '_results'
    result_file = project + '_code_check.csv'
    results = []
    pool = multiprocessing.Pool(processes=jobs)
    for uid in os.listdir(records_dir):
        project_dir = os.path.join(records_dir, uid)
        if os.path.isdir(project_dir):
            inject_driver(project_dir, driver_dir)
            results.append(pool.apply_async(check_one, (project, ['codestyle.py'], uid, project_dir,)))
    pool.close()
    pool.join()

    with open(result_file, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for result in results:
            writer.writerow(result.get())


parser = argparse.ArgumentParser(description='Code Check with Multiprocessing.')
parser.add_argument('-j', '--jobs', type=int, default=multiprocessing.cpu_count())
parser.add_argument('project', type=str, nargs=1)
args = parser.parse_args()
main(args.project[0], jobs=args.jobs)
