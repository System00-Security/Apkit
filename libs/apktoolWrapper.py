import subprocess
import os
from libs.banner import label
import shutil

class apktool:
    def decompile(apkpath):
        print(f"{label.info} Decompiling APK file: {apkpath}")
        apkname = apkpath.split("/")[-1].replace(".apk", "")
        try:
            if os.path.exists(apkname):
                output = subprocess.check_output(f"rm -rf {apkname}", shell=True)
            output = subprocess.check_output(f"java -jar bin/apktool.jar d {apkpath} -o {apkname} > /dev/null 2>&1", shell=True)
            if os.path.exists(apkname):
                print(f"{label.done} APK decompiled successfully")
        except Exception as e:
            print(f"{label.error} Error decompiling APK: {e}")

    def recompile(apkpath):
        print(f"{label.info} Recompiling APK file: {apkpath}")
        try:
            output = subprocess.check_output(f"java -jar bin/apktool.jar b {apkpath} -o {apkpath}-recompiled.apk", shell=True)
            if os.path.exists(f"{apkpath}-recompiled.apk"):
                print(f"{label.done} APK recompiled successfully")
        except Exception as e:
            if os.path.exists(f"{apkpath}-recompiled.apk"):
                output = subprocess.check_output(f"java -jar bin/apktool.jar b {apkpath} -o {apkpath}-recompiled.apk --use-aapt2", shell=True)
                print(f"{label.done} APK recompiled successfully")
            else:
                print(f"{label.error} Error recompiling APK: {e}")
    def apkresign(apkpath):
        print(f"{label.info} Resigning APK file: {apkpath}")
        try:
            apkname = apkpath.split("/")[-1].replace(".apk", "")
            output = subprocess.check_output(f"java -jar bin/signer.jar --apks {apkpath}", shell=True)
            if os.path.exists(f"{apkname}-recompiled-aligned-debugSigned.apk"):
                print(f"{label.done} APK resigned successfully")
        except Exception as e:
            print(f"{label.error} Error resigning APK: {e}")
    def AfterClean(apkname):
        print(f"{label.info} Cleaning Up Post-Processing Files")
        try:
            shutil.rmtree(apkname)
            os.remove(f"{apkname}-recompiled.apk")
            idsgifile = f"{apkname}-recompiled-aligned-debugSigned.apk.idsig"
            if os.path.exists(idsgifile):
                os.remove(idsgifile)
            print(f"{label.done} Cleaned Up Post-Processing Files")
        except Exception as e:
            print(f"{label.error} Error Cleaning Up Post-Processing Files: {e}")
            