import subprocess
import os

from utilities import constants
"""
dexdump: [-a] [-c] [-d] [-e] [-f] [-h] [-i] [-l layout] [-o outfile] dexfile...

 -a : display annotations
 -c : verify checksum and exit
 -d : disassemble code sections
 -e : display exported items only
 -f : display summary information from file header
 -g : display CFG for dex
 -h : display file header details
 -i : ignore checksum failures
 -l : output layout, either 'plain' or 'xml'
 -o : output file name (defaults to stdout)
 
dexdump -a ab.huobaotv.cn.apk -o test2.txt
dexdump -c ab.huobaotv.cn.apk -o test2.txt
dexdump -d ab.huobaotv.cn.apk -o test2.txt
dexdump -e ab.huobaotv.cn.apk -o test2.txt
dexdump -f ab.huobaotv.cn.apk -o test2.txt
dexdump -g ab.huobaotv.cn.apk -o test2.txt
dexdump -h ab.huobaotv.cn.apk -o test2.txt
dexdump -i ab.huobaotv.cn.apk -o test2.txt

"""

def dexdump_plain(filename):
    try:
        subprocess.run('dexdump -l plain {} -o {}.txt'.format(constants.EXTRACTED_DEX_DIR + filename,
                                                              constants.DEXDUMP_PATH_PLAIN + filename),
                       shell=True,
                       capture_output=True,
                       text=True,
                       check=True).stdout.split('\n')
    except subprocess.CalledProcessError:
        print("An error occured while handling file: ", filename)


def dexdump_xml(filename):
    try:
        subprocess.run('dexdump -l xml {} -o {}.xml'.format(constants.EXTRACTED_DEX_DIR + filename,
                                                            constants.DEXDUMP_PATH_XML + filename),
                       shell=True,
                       capture_output=True,
                       text=True,
                       check=True).stdout.split('\n')
    except subprocess.CalledProcessError:
        print("An error occured while handling file: ", filename)


def dexdump_hex(filename):
    try:
        subprocess.run(
            'hexdump {} >> {}.txt'.format(constants.EXTRACTED_DEX_DIR + filename,
                                          constants.DEXDUMP_PATH_HEX + filename),
            shell=True,
            capture_output=True,
            text=True,
            check=True).stdout.split('\n')
    except subprocess.CalledProcessError:
        print("An error occured while handling file: ", filename)


def create_dex_dumps():
    print("[INFO] Creating dexdumps....")
    for _, _, files in os.walk(constants.EXTRACTED_DEX_DIR):
        print(files)
        for file in files:
            dexdump_plain(file)
            dexdump_xml(file)
            dexdump_hex(file)
    print("[INFO] Finished creating dexdumps....")
