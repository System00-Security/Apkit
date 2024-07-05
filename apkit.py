from libs.banner import banner, label
from libs.keyleaks import *
from libs.analyzer import Generic_analyze_apk, Owasp_analyze_apk, dangrousPermission
from libs.apktoolWrapper import apktool
from libs.androgurdWrapper import appinfo
from libs.fridaclone import fridaClone
from libs.jadxWrapper import jadaxDecompile
from libs.sslunpinners import sslUNpinners
import os
import argparse


def appInformation(apk):
    appinfodict = appinfo(apk)
    print(f"""
- [PKG] {appinfodict['package']}
- [VER] {appinfodict['version']}
          """)

def main():
    banner()
    parser = argparse.ArgumentParser(description="APK Analysis Toolkit")
    parser.add_argument("-a", "--apk", help="APK file to analyze")
    parser.add_argument("-o", "--output", default="output.txt", help="Output directory")
    parser.add_argument("-fc", "--fridaclone" , help="Frida Clone 'ex: -fc example/example.js'")
    parser.add_argument("-sslp", "--sslunpin", help="Remove SSL Pinning from APK 'ex: -sslp netconf_patch'")
    parser.add_argument("-cert", "--certificates", help="SSL Certificate Pinning 'ex: -cert burp.der'")
    parser.add_argument("-adb", "--adb", help="For automating Frida SSL Unpinning actions 'ex: -adb 127.0.0.1:5555'")
    parser.add_argument("-lsmod", "--listmodules", help="List module for sslunpin 'ex: -lsmod'", action="store_true")
    parser.add_argument("-an", "--analyze", help="Analyze APK 'ex: -an owasp'")
    parser.add_argument("-la", "--listanalysis", help="List analysis modes 'ex: -la'", action="store_true")
    parser.add_argument("-dp", "--dangerouspermissions", help="Check Dangerous Permissions 'ex: -dp example.apk'")
    parser.add_argument("-ex", "--extract", help="Extract APK 'ex: -ex api_key'")
    parser.add_argument("-lex", "--listextract", help="List extractable data 'ex: -lex'", action="store_true")
    args = parser.parse_args()

    if args.fridaclone:
        fridaClone(args.fridaclone)
    elif args.sslunpin:
        if args.apk:
            appInformation(args.apk)
            apktool.decompile(args.apk)
            if args.sslunpin == "netconf_patch":
                sslUNpinners.SslNet_Sec_Conf(args.apk)
            elif args.sslunpin == "trustmanager_patch":
                sslUNpinners.TrustManagerImpl(args.apk)
            elif args.sslunpin == "auto_frida":
                if args.certificates:
                    if args.adb:
                        sslUNpinners.FridaPinning(args.apk, args.adb, args.certificates)
                    else:
                        print(f"{label.error} Please provide ADB IP")
                else:
                    print(f"{label.error} Please provide SSL Certificate")
            else:
                print(f"{label.error} Please provide a valid module")
        else:
            print(f"{label.error} Please provide an APK file")
    elif args.analyze:
        if args.apk:
            appInformation(args.apk)
            apkname = args.apk.split("/")[-1].replace(".apk", "")
            apkdepath = f"{apkname}-jadx"
            if args.analyze == "generic":
                if os.path.exists(apkdepath):
                    Generic_analyze_apk(apkdepath, args.output)
                else:
                    jadaxDecompile(args.apk)
                    Generic_analyze_apk(apkdepath, args.output)
            elif args.analyze == "owasp":
                if os.path.exists(apkdepath):
                    Owasp_analyze_apk(apkdepath, args.output)
                else:
                    jadaxDecompile(args.apk)
                    Owasp_analyze_apk(apkdepath, args.output)
            else:
                print(f"{label.error} Please provide a valid analysis mode")
        else:
            print(f"{label.error} Please provide an APK file")
    elif args.dangerouspermissions:
        appInformation(args.dangerouspermissions)
        dangrousPermission(args.dangerouspermissions, args.output)
    elif args.extract:
        if args.apk:
            appInformation(args.apk)
            if args.extract == "api_key":
                appDpath = args.apk.split("/")[-1].replace(".apk", "")
                if os.path.exists(appDpath):
                    findHardcodedCredentials(appDpath)
                else:
                    apktool.decompile(args.apk)
                    findHardcodedCredentials(appDpath)
            if args.extract == "urls":
                appDpath = args.apk.split("/")[-1].replace(".apk", "")
                if os.path.exists(appDpath):
                    links = linkExtractor(appDpath)
                    for link in links:
                        print(f"{label.info} Found URL: {link}")
                else:
                    apktool.decompile(args.apk)
                    links = linkExtractor(appDpath)
                    for link in links:
                        print(f"{label.info} Found URL: {link}")
        else:
            print(f"{label.error} Please provide an APK file")
    elif args.listanalysis:
        print(f"""
        analysis_mode                description
        -------------                -----------
        generic                      Generic Analysis
        owasp                        OWASP Mobile Top 10
              """)
    elif args.listextract:
        print(f"""
        extractable_data             description
        ----------------             -----------
        api_key                      Extract API Keys
        urls                         Extract URLs
              """)

    elif args.listmodules:
        print(f"""
        module                       description
        -------                      ------------
        netconf_patch                Patch network_security_config.xml
        trustmanager_patch           Patch TrustManagerImpl.java
        auto_frida                   Automatically Deployes Frida SSL Unpinning Method
              """)
        
    else:
        print(f"{label.error} Please provide a valid option, use -h for help")

if __name__ == "__main__":
    main()