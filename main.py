"""
Extracts Dex and Manifest from the APK by first decompiling it using APKTool.
For all the files in APK_FILE_PATH:
    Decompile into a temp folder
    Extract Dex files to DEX_FILE_PATH
    Extract Manifest files to MANIFEST_FILE_PATH
    Delete the remaining files
"""

