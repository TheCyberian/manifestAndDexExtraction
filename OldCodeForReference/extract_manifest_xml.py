import subprocess
import re

from utilities.constants import EXTRACTED_MANIFEST_DIR, DECOMPILED_FILES_PATH, REGEX_PATTERN_FOR_APK


def extract_manifest_from_apks_in_path():
    print("Starting execution")
    print('find {} -type f -name "AndroidManifest.xml"'.format(DECOMPILED_FILES_PATH))
    cmd_out: bytes = subprocess.run(
        'find {} -maxdepth 3 -type f -name "AndroidManifest.xml"'.format(DECOMPILED_FILES_PATH),
        shell=True,
        capture_output=True,
        text=True,
        check=True).stdout.split('\n')

    print(cmd_out)

    manifest_file_path = []
    for index, file_path in enumerate(cmd_out):
        if len(file_path) > 0:
            if 'apktool' in file_path and 'apktools/original' not in file_path:
                manifest_file_path.append(file_path)
        else:
            print("Probably the end of list!")

    print(len(manifest_file_path))

    for apk in manifest_file_path:
        file_name = re.search(REGEX_PATTERN_FOR_APK, apk).group(0)
        print(file_name)
        print(file_name.split('/')[-1])
        file_name = file_name.split('/')[-1]
        print("Copying ... ", file_name)
        subprocess.run('cp {} {}'.format(apk, EXTRACTED_MANIFEST_DIR + file_name + "_manifest.xml"),
                       shell=True,
                       capture_output=True,
                       text=True,
                       check=True).stdout.split('\n')
    # for apk in apk_names_list:
    #     name = re.search(constants.REGEX_PATTERN_FOR_APK, apk).group(0)
    #     for file_path in manifest_file_path:
    #         if name in file_path:
    #             subprocess.run('mv {} {}'.format(file_path, constants.EXTRACTED_DEX_DIR + name + ".dex"),
    #                            shell=True,
    #                            capture_output=True,
    #                            text=True,
    #                            check=True).stdout.split('\n')
    #             subprocess.run('rm -rf {}'.format(apk),
    #                            shell=True,
    #                            capture_output=True,
    #                            text=True,
    #                            check=True)
    #             break
