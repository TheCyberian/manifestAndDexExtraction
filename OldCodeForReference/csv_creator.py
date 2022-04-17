import os
import pandas as pd
from utilities import constants


def generate_csv(path, tag):
    labels = []
    file_content = []
    for files in os.listdir(path):
        if "malicious_" in files:
            labels.append("1")
        else:
            labels.append("0")
        filename = os.path.join(path, files)
        print("[INFO] Reading file :  " + filename)
        with open(filename, encoding='ascii', errors='ignore') as f:
            content = f.read().splitlines()
            content = " ".join(content)
            file_content.append(content[50000:])
            print("[INFO] File text added to list...")
    print("[INFO] Saving the texts in dataframe...")
    df = pd.DataFrame(
        {
            'label': labels,
            'file_content': file_content
        }
    )
    print("[INFO] Writing Dataframe to CSV file...", df)
    df.to_csv(constants.CSV_PATH + tag + '.csv')
    print("[INFO] Writing Dataframe to CSV file Success...", df)


def transform_dex_files():
    generate_csv(constants.DEXDUMP_PATH_XML, "XML")
    generate_csv(constants.DEXDUMP_PATH_PLAIN, "Plain")
    generate_csv(constants.DEXDUMP_PATH_HEX, "Hex")