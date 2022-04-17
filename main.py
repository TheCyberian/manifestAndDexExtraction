import multiprocessing
import os
import subprocess
import timeit
import sys

import paths
from dexExtracter import unpack_apk_files_and_run_dexdump
from manifestExtractor import extract_manifest_from_apk_in_path


THREADS = multiprocessing.cpu_count()
GLOBAL_LOCK = multiprocessing.Lock()


def decompile_apk_and_extract_data(args):
    apk_input_path, decompiled_output_path = args
    GLOBAL_LOCK.acquire()
    try:
        subprocess.run('apktool d {} -o {}'.format(apk_input_path, decompiled_output_path),
                       shell=True,
                       capture_output=True,
                       text=True,
                       check=True).stdout.split('\n')
        extract_manifest_from_apk_in_path(decompiled_output_path)
        unpack_apk_files_and_run_dexdump(apk_input_path, decompiled_output_path)

    except Exception as e:
        print(e)
        print("Error Occurred! Could not find file " + apk_input_path)
    GLOBAL_LOCK.release()


def main():
    start_time = timeit.default_timer()
    tasks_args = []
    for root, directory, files in os.walk(paths.APK_FILE_PATH):
        for file in files:
            if 'benign' in root:
                tasks_args.append((root + '/' + file, paths.DECOMPILED_FILE_PATH + '/benign_' + file,))
            elif 'malicious' in root:
                tasks_args.append((root + '/' + file, paths.DECOMPILED_FILE_PATH + '/malicious_' + file,))
    print(tasks_args)

    pool = multiprocessing.Pool(THREADS)
    try:
        pool.map_async(decompile_apk_and_extract_data, tasks_args).get()
    except KeyboardInterrupt:
        sys.stdout.write('\033[0m')
        sys.stdout.write("User interupted...")
    pool.close()

    elapsed_time = timeit.default_timer()
    print("Time Taken: (in Secs)", elapsed_time - start_time)


if __name__ == '__main__':
    main()
