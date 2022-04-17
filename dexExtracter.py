import subprocess
import zipfile

import utilities


def unpack_apk_files_and_run_dexdump(apk_input_path, decompiled_output_path):
    with zipfile.ZipFile(apk_input_path, 'r') as file:
        print('[INFO] Extracting files from APK archive...')
        file.extractall(decompiled_output_path)

    print("[INFO] Looking for classes.dex in ", decompiled_output_path)
    print("[INFO] Executed Command: find {} -maxdepth 1 -type f -name \"classes.dex\"".format(decompiled_output_path))
    cmd_out: bytes = subprocess.run(
        'find {} -maxdepth 1 -type f -name "classes.dex"'.format(decompiled_output_path),
        shell=True,
        capture_output=True,
        text=True,
        check=True).stdout.split('\n')

    file_path = cmd_out[0]
    print("[INFO] Found classes.dex at path:", file_path)
    print("[INFO] APK File name:", file_path.split('/')[-2])
    file_name = file_path.split('/')[-2]

    print("[INFO] Running dexdump on Dalvik executable file now... ")

    utilities.dexdump_plain(file_path, file_name)
    utilities.dexdump_xml(file_path, file_name)
    utilities.dexdump_hex(file_path, file_name)

    print("[INFO] Removing Decompiled files for APK :", file_name)
    subprocess.run('rm -rf {}'.format(decompiled_output_path),
                   shell=True,
                   capture_output=True,
                   text=True,
                   check=True).stdout.split('\n')

    utilities.write_apkname_to_file(file_name, "dex")
