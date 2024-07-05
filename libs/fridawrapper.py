import subprocess
import os
import requests
from libs.banner import label
from libs.fridaclone import fridaClone


class Frida:
    def ServerDownloader(arch):
        print(f"{label.info} Downloading Frida Server for {arch}")
        try:
            githubrelase = requests.get("https://api.github.com/repos/frida/frida/releases/latest", headers={'User-Agent': 'Mozilla/5.0'}).json()
            assets = githubrelase['assets']
            for asset in assets:
                if "server" in asset['name'] and "android" in asset['name'] and arch in asset['name']:
                    serverurl = asset['browser_download_url']
                    servername = asset['name']
                    break
            if not serverurl:
                print(f"{label.error} Frida Server not found for {arch}")
                return
            if os.path.exists(servername):
                print(f"{label.warn} Removing old Frida Server")
                os.remove(servername)
            print(f"{label.info} Downloading Frida Server: {servername}")
            response = requests.get(serverurl, headers={'User-Agent': 'Mozilla/5.0'})
            with open(servername, "wb") as f:
                f.write(response.content)
            print(f"{label.done} Downloaded Frida Server: {servername}")
        except Exception as e:
            print(f"{label.error} Error downloading Frida Server: {e}")

    def PinningBypassrunner(adb, package,certpath):
        print(f"{label.info} Started Frida Runner")
        try:
            print(f"{label.info} Connecting to ADB")
            output = subprocess.check_output(f"adb connect {adb} >/dev/null", shell=True)
            print(f"{label.done} Connected to ADB")
            arc = subprocess.check_output(f"adb -s {adb} shell getprop ro.product.cpu.abi", shell=True).decode().strip()
            print(f"{label.info} Downloading Frida Server for Android: {arc}")
            Frida.ServerDownloader(arc)
            unzip = subprocess.check_output(f"unxz *.xz", shell=True)
            rename = subprocess.check_output(f"mv frida-server-* frida-server", shell=True)
            print(f"{label.info} Pushing Frida Server to Android")
            push = subprocess.check_output(f"adb -s {adb} push frida-server /data/local/tmp", shell=True)
            permission = subprocess.check_output(f"adb -s {adb} shell chmod 777 /data/local/tmp/frida-server", shell=True)
            print(f"{label.info} Pushing SSL Certificate to Android")
            rename = subprocess.check_output(f"mv {certpath} cert-der.crt", shell=True)
            pushcert = subprocess.check_output(f"adb -s {adb} push cert-der.crt /data/local/tmp", shell=True)
            print(f"{label.info} Cloning Frida Script pcipolloni/universal-android-ssl-pinning-bypass-with-frida")
            fridaClone("pcipolloni/universal-android-ssl-pinning-bypass-with-frida")
            rname = subprocess.check_output(f"mv universal-android-ssl-pinning-bypass-with-frida.js fridascript.js", shell=True)
            pushscript = subprocess.check_output(f"adb -s {adb} push fridascript.js /data/local/tmp", shell=True)
            print(f"{label.info} Starting Frida Server")
            server = subprocess.Popen(f"adb -s {adb} shell /data/local/tmp/frida-server &", shell=True)
            print(f"{label.info} Running Frida Script")
            subprocess.Popen(f"frida -U -f {package} -l fridascript.js", shell=True)
        except Exception as e:
            print(f"{label.error} Error running Frida: {e}")





        
            