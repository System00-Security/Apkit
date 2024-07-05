import subprocess
import os
from libs.banner import label

def jadaxDecompile(apkpath):
    print(f"{label.info} Decompiling APK file: {apkpath} Using Jadx")
    try:
        fullpath = os.path.abspath(apkpath)
        apkname = apkpath.split("/")[-1].replace(".apk", "")
        output = subprocess.check_output(f"./bin/jadx/bin/jadx -d {apkname}-jadx {fullpath} >nul 2>&1", shell=True)
        print(f"{label.info} APK decompiled successfully")
    except Exception as e:
        print(f"{label.info} Error decompiling APK: {e}")