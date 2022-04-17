import subprocess
import zipfile

import dexDumpUtility


def unpack_apk_files_and_run_dexdump(apk_input_path, decompiled_output_path):
    with zipfile.ZipFile(apk_input_path, 'r') as file:
        print('Extracting files from APK archive...')
        file.extractall(decompiled_output_path)

    print("Looking for classes.dex in ", decompiled_output_path)
    print("Executed Command: find {} -maxdepth 1 -type f -name \"classes.dex\"".format(decompiled_output_path))
    cmd_out: bytes = subprocess.run(
        'find {} -maxdepth 1 -type f -name "classes.dex"'.format(decompiled_output_path),
        shell=True,
        capture_output=True,
        text=True,
        check=True).stdout.split('\n')

    file_path = cmd_out[0]
    print("Found classes.dex at path:", file_path)
    print("APK File name:", file_path.split('/')[-2])
    file_name = file_path.split('/')[-2]
    # TODO: Write file_name variable (without benign/malicious tag) to a APKFilesList for reproducible experiments.
    print("Running dexdump on Dalvik executable file now... ")

    dexDumpUtility.dexdump_plain(file_path, file_name)
    dexDumpUtility.dexdump_xml(file_path, file_name)
    dexDumpUtility.dexdump_hex(file_path, file_name)

    print("Removing Decompiled files for APK :", file_name)
    subprocess.run('rm -rf {}'.format(decompiled_output_path),
                   shell=True,
                   capture_output=True,
                   text=True,
                   check=True).stdout.split('\n')
