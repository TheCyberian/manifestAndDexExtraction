# Extract Manifest and Dex from APK

This is the pre-processing part of the research work done on using document embeddings approach for Android malware detection. This piece of code helps automate extraction of the *files of interest* that will be used for generating artefacts for our experiments. It utilises multithreading which allows decompilation and file extraction to run on multiple Android APKs at once.

The program looks for files in `paths.APK_FILE_PATH`. The files should be segregated into `benign` and `malicious` folders.

It decompiles the APK using `apktool` and extracts decompiled `AndroidManifest.xml` into `paths.MANIFEST_FILE_PATH`.
After which it unzips the APK and runs `dexdump` on the `classes.dex` file and extracts three types of dexdumps into `paths.DEX_FILE_PATH`.

It also stores the APK filenames from which the above files were extracted into a `.csv` file. This file contains APK names and a tag (0 for benign and 1 for malicious).

The decompiled and extracted files are also cleaned up after the necessary files are extracted.

