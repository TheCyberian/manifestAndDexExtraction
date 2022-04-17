import os
import subprocess

import paths


def dexdump_plain(input_filename, output_filename):
    plain_dex_path = paths.DEX_FILE_PATH + "/plain/"
    os.makedirs(os.path.dirname(plain_dex_path), exist_ok=True)
    try:
        subprocess.run('dexdump -l plain {} -o {}.txt'.format(input_filename, plain_dex_path + output_filename),
                       shell=True,
                       capture_output=True,
                       text=True,
                       check=True).stdout.split('\n')
    except subprocess.CalledProcessError:
        print("[ERROR] An error occured while handling file: ", input_filename)


def dexdump_xml(input_filename, output_filename):
    xml_dex_path = paths.DEX_FILE_PATH + "/xml/"
    os.makedirs(os.path.dirname(xml_dex_path), exist_ok=True)
    try:
        subprocess.run('dexdump -l xml {} -o {}.xml'.format(input_filename, xml_dex_path + output_filename),
                       shell=True,
                       capture_output=True,
                       text=True,
                       check=True).stdout.split('\n')
    except subprocess.CalledProcessError:
        print("[ERROR] An error occured while handling file: ", input_filename)


def dexdump_hex(input_filename, output_filename):
    hex_dex_path = paths.DEX_FILE_PATH + "/hex/"
    os.makedirs(os.path.dirname(hex_dex_path), exist_ok=True)
    try:
        subprocess.run(
            'hexdump {} >> {}.txt'.format(input_filename, hex_dex_path + output_filename),
            shell=True,
            capture_output=True,
            text=True,
            check=True).stdout.split('\n')
    except subprocess.CalledProcessError:
        print("[ERROR] An error occured while handling file: ", input_filename)


def write_apkname_to_file(filename, file_tag="man"):
    if "dex" in file_tag:
        output_filepath = paths.CLASSES_DEX_FILES_LIST
    else: output_filepath = paths.MANIFEST_FILES_LIST

    with open(output_filepath, "a") as file:
        if "benign_" in filename:
            tag = "0"
        else:
            tag = "1"
        apk_name = filename.split("_")[-1]
        file.write(tag + ", " + apk_name + "\n")
