import subprocess
import re

from utilities import constants


def extract_dex_from_apks_in_path():
    print('find {} -type f -name "*.dex"'.format(constants.UNPACKED_FILES_PATH))
    cmd_out: bytes = subprocess.run(
        'find {} -type f -name "*.dex"'.format(constants.UNPACKED_FILES_PATH),
        shell=True,
        capture_output=True,
        text=True,
        check=True).stdout.split('\n')

    # APK name list to collect APK name alone and tag the dex file with the name
    apk_names_list = []
    for index, file_path in enumerate(cmd_out):
        if len(file_path) > 0:
            file_name = re.search(constants.REGEX_PATTERN_FOR_APK, file_path).group(0)
            print(file_name)
            apk_names_list.append(file_name)
        else:
            print("Probably the end of list!")
            print(len(apk_names_list))

    # Moves and tags the dex file with app name from all unpacked apks in temp folder.
    # Removes the APKs after retrieving dex files
    # print(len(apk_names_list))
    apk_names_list = set(apk_names_list)
    # print(len(apk_names_list))
    for apk in apk_names_list:
        name = re.search(constants.REGEX_PATTERN_FOR_APK_NAME, apk).group(0)
        # print(name)
        for file_path in cmd_out:
            # print(file_path)
            if name.split('/').pop() in file_path:
                # name = name.replace('$', '\$')
                print('cp {} {}'.format(file_path, constants.EXTRACTED_DEX_DIR + name.split('/').pop() + '.dex'))
                subprocess.run("cp '{}' {}".format(file_path, constants.EXTRACTED_DEX_DIR + name.split('/').pop() + ".dex"),
                               shell=True,
                               capture_output=True,
                               text=True,
                               check=True).stdout.split('\n')
                subprocess.run('rm -rf {}'.format(apk),
                               shell=True,
                               capture_output=True,
                               text=True,
                               check=True)
                break
