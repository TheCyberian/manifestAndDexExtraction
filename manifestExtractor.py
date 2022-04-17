import subprocess
import paths
import utilities


def extract_manifest_from_apk_in_path(decompiled_output_path):
    print("[INFO] Looking for AndroidManifest.xml in ", decompiled_output_path)
    print("[INFO] Executed Command: find {} -maxdepth 1 -type f -name \"AndroidManifest.xml\"".format(decompiled_output_path))
    cmd_out: bytes = subprocess.run(
        'find {} -maxdepth 1 -type f -name "AndroidManifest.xml"'.format(decompiled_output_path),
        shell=True,
        capture_output=True,
        text=True,
        check=True).stdout.split('\n')

    file_path = cmd_out[0]
    print("[INFO] Found AndroidManifest.xml at path:", file_path)
    print("[INFO] APK File name:", file_path.split('/')[-2])
    file_name = file_path.split('/')[-2]

    print("[INFO] Copying Manifest File now... ")
    subprocess.run('cp {} {}'.format(file_path, paths.MANIFEST_FILE_PATH + "/" + file_name + "_manifest.xml"),
                   shell=True,
                   capture_output=True,
                   text=True,
                   check=True).stdout.split('\n')

    print("[INFO] Removing Decompiled files for APK :", file_name)
    subprocess.run('rm -rf {}'.format(decompiled_output_path),
                   shell=True,
                   capture_output=True,
                   text=True,
                   check=True).stdout.split('\n')
    utilities.write_apkname_to_file(file_name)
