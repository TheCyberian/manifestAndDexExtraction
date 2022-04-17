import multiprocessing
import os
import timeit
from multiprocessing import Process
import sys

import apk2java

from utilities import constants


THREADS = multiprocessing.cpu_count()
GLOBAL_LOCK = multiprocessing.Lock()


# noinspection PyBroadException
def benign_decompile(args):
    unpacked_apk_input_path, decompiled_output_path = args
    GLOBAL_LOCK.acquire()
    try:
        apk2java.decompile(unpacked_apk_input_path, decompiled_output_path)
    except Exception:
        print("Error Occurred! Could not find file " + unpacked_apk_input_path)
    GLOBAL_LOCK.release()


def main(args=None):
    start_time = timeit.default_timer()
    tasks_args = []
    for root, directory, files in os.walk(constants.RAW_FILES_PATH):
        for file in files:
            if 'benign' in root:
                tasks_args.append((root + '/' + file, constants.DECOMPILED_FILES_PATH + 'benign_' + file,))
            elif 'malicious' in root:
                tasks_args.append((root + '/' + file, constants.DECOMPILED_FILES_PATH + 'malicious_' + file,))
    print(tasks_args)
    #         if 'benign' in root:
    #             print("Decompiling...")
    #             print(root + '/' + file)
    #             # benign_decompile(root + '/' + file, constants.DECOMPILED_FILES_PATH + 'benign_' + file)
    #             p1 = Process(target=benign_decompile, args=(root + '/' + file, constants.DECOMPILED_FILES_PATH + 'benign_' + file))
    #             tasks.append(p1)
    #             p1.start()
    #         elif 'malicious' in root:
    #             print("Decompiling...")
    #             print(root + '/' + file)
    #             # malicious_decompile(root + '/' + file, constants.DECOMPILED_FILES_PATH + 'malicious_' + file)
    #             p2 = Process(target=malicious_decompile, args=(root + '/' + file, constants.DECOMPILED_FILES_PATH + 'malicious_' + file))
    #             tasks.append(p2)
    #             p2.start()
    #
    #     for task in tasks:
    #         task.join()
    pool = multiprocessing.Pool(THREADS)
    try:
        pool.map_async(benign_decompile, tasks_args).get()
    except KeyboardInterrupt:
        sys.stdout.write('\033[0m')
        sys.stdout.write("User interupted...")
    pool.close()

    elapsed_time = timeit.default_timer()
    print("Time Taken: (in Secs)", elapsed_time - start_time)


if __name__ == '__main__':
    main()
