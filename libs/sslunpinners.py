from libs.banner import label
from libs.apktoolWrapper import apktool
from libs.androgurdWrapper import appinfo
from libs.fridawrapper import Frida
import xml.etree.ElementTree as ET
from pathlib import Path

class sslUNpinners:
    def SslNet_Sec_Conf(apkpath):
        print(f"{label.info} Patching network_security_config.xml of APK: {apkpath}")
        try:
            apktool.decompile(apkpath)
            decompilepath = apkpath.split("/")[-1].replace(".apk", "")
            manifestpath = f"{decompilepath}/AndroidManifest.xml"
            tree = ET.parse(manifestpath)
            root = tree.getroot()
            application = root.find("application")
            networksecurityconfig = application.get(
            "{http://schemas.android.com/apk/res/android}networkSecurityConfig"
        )
            if networksecurityconfig is None:
                application.set(
                "{http://schemas.android.com/apk/res/android}networkSecurityConfig",
                "@xml/network_security_config",
            )
            with open(manifestpath, "w", encoding="utf-8") as f:
                f.write(ET.tostring(root, encoding="utf-8").decode())
            config_file = (
            Path(decompilepath) / "res" / "xml" / "network_security_config.xml"
            )
            print(f"{label.info} Patching network_security_config.xml")
            injection = """<?xml version="1.0" encoding="utf-8"?>
    <network-security-config>
        <debug-overrides>
            <trust-anchors>
                <certificates src="user" />
            </trust-anchors>
        </debug-overrides>
        <base-config cleartextTrafficPermitted="true">
            <trust-anchors>
                <certificates src="system" />
                <certificates src="user" />
            </trust-anchors>
        </base-config>
    </network-security-config>
    """
            with open(config_file, "w") as f:
                f.write(injection)
            print(f"{label.done} network_security_config.xml patched successfully")
            apktool.recompile(decompilepath)
            print(f"{label.info} Repackaging APK to {decompilepath}-recompiled.apk")
            apktool.apkresign(f"{decompilepath}-recompiled.apk")
            print(f"{label.info} Saved as {decompilepath}-recompiled-aligned-debugSigned.apk")
            apktool.AfterClean(decompilepath)
        except Exception as e:
            print(f"{label.error} Error removing SSL Pinning: {e}")
    def TrustManagerImpl(apkpath):
        print(f"{label.info} Patching TrustManagerImpl.java of APK: {apkpath}")
        try:
            apktool.decompile(apkpath)
            decompilepath = apkpath.split("/")[-1].replace(".apk", "")
            trustmanagerimpl = (
            Path(decompilepath) / "smali" / "okhttp3" / "internal" / "t"
            / "TrustManagerImpl.smali"
            )
            print(f"{label.info} Patching TrustManagerImpl.java")
            with open(trustmanagerimpl, "r") as f:
                data = f.read()
                data = data.replace(
                "checkServerTrusted",
                "checkServerTrusted1",
            )
            with open(trustmanagerimpl, "w") as f:
                f.write(data)
            print(f"{label.done} TrustManagerImpl.java patched successfully")
            apktool.recompile(decompilepath)
            print(f"{label.info} Repackaging APK to {decompilepath}-recompiled.apk")
            apktool.apkresign(f"{decompilepath}-recompiled.apk")
            print(f"{label.info} Saved as {decompilepath}-recompiled-aligned-debugSigned.apk")
            apktool.AfterClean(decompilepath)
        except Exception as e:
            print(f"{label.error} Error removing SSL Pinning: {e}")
    def FridaPinning(apk, adb, certpath):
        print(f"{label.info} Bypassing SSL Pinning using Frida")
        try:
            app = appinfo(apk)
            package = app['package']
            Frida.PinningBypassrunner(adb, package, certpath)
        except Exception as e:
            print(f"{label.error} Error bypassing SSL Pinning: {e}")
