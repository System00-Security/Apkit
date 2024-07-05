import os
from libs.banner import label
import json
import re
from libs.androgurdWrapper import appinfo
from colorama import Style, Fore



def search(directory, pattern):
    results = []
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_numbers = []
                    matched_lines = []
                    for line_number, line in enumerate(f, start=1):
                        if re.search(pattern, line):
                            line_numbers.append(line_number)
                            matched_lines.append(line)
                    if line_numbers:
                        results.append({
                            "path": file_path,
                            "line_numbers": line_numbers,
                            "matched_lines": matched_lines
                        })
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        line_numbers = []
                        matched_lines = []
                        for line_number, line in enumerate(f, start=1):
                            if re.search(pattern, line):
                                line_numbers.append(line_number)
                                matched_lines.append(line)
                        if line_numbers:
                            results.append({
                                "path": file_path,
                                "line_numbers": line_numbers,
                                "matched_lines": matched_lines
                            })
                except OSError as e:
                    print(f"Error opening file '{file_path}': {e}")
            except OSError as e:
                print(f"Error opening file '{file_path}': {e}")

    return results


def SeverityColor(severity):
    if severity == "info":
        return f"{Fore.BLUE}{severity}{Style.RESET_ALL}"
    elif severity == "low":
        return f"{Fore.GREEN}{severity}{Style.RESET_ALL}"
    elif severity == "medium":
        return f"{Fore.YELLOW}{severity}{Style.RESET_ALL}"
    elif severity == "high":
        return f"{Fore.RED}{severity}{Style.RESET_ALL}"

def Generic_analyze_apk(apkpath, output):
    print(f"{label.info} Analyzing Provided Decompiled APK: {Style.BRIGHT}{apkpath}.apk{Style.RESET_ALL}")
    vulntemplate_file = open("patterns/vuln-generic.json", "r")
    VulnTemplate = json.load(vulntemplate_file)
    print(f"{label.info} Loaded {Fore.BLUE}{len(VulnTemplate)}{Fore.RESET} vulnerabilities,info to check for in the APK")
    for vuln_name, vuln_data in VulnTemplate.items():
        severity = vuln_data["Severity"]
        for matcher in vuln_data["Matcher"]:
            try:    
                results = search(apkpath, matcher)
                if results:
                        print(f"{label.warn} Found an {SeverityColor(severity)} {Fore.RED}{vuln_name}{Fore.RESET} in file {Style.BRIGHT}{results[0]['path']}{Style.RESET_ALL} at line(s) {Fore.BLUE}{', '.join(map(str, results[0]['line_numbers']))}{Fore.RESET}")
                        save = open(output, "a")
                        save.write(f"Found an [{severity}]-> {vuln_name} in file {results[0]['path']} at line(s) {', '.join(map(str, results[0]['line_numbers']))}\n")
                        save.close()
            except Exception as e:
                pass
    print(f"{label.info} Analysis Completed Successfully")

def Owasp_analyze_apk(apkpath, output):
    print(f"{label.info} Analyzing Provided Decompiled APK: {Style.BRIGHT}{apkpath}.apk{Style.RESET_ALL}")
    vulntemplate_file = open("patterns/owasp10.json", "r")
    owaspdata = json.load(vulntemplate_file)
    print(f"{label.info} Loaded 10 Checks of {Fore.GREEN}OWASP-10{Fore.RESET} for analysis")
    for vuln_name, vuln_data in owaspdata.items():
        findings = []
        description = vuln_data["Description"]
        matcher = vuln_data["Matchers"]
        remediator = vuln_data["Remediation"]
        try:
            for match in matcher:
                results = search(apkpath, match)
                if results:
                    findings.append(results)
            if findings:
                print(f"---")
                print(f"{label.warn} Found {Fore.RED} {vuln_name} {Fore.RESET}")
                print(f"{label.info} Description: {Fore.BLUE}{description}{Fore.RESET}")
                for finding in findings:
                    print(f"{label.info} Found in file {Style.BRIGHT}{finding[0]['path']}{Style.RESET_ALL} at line(s) {Fore.BLUE}{', '.join(map(str, finding[0]['line_numbers']))}{Fore.RESET}")
                    save = open(output, "a")
                    save.write(f"Found {vuln_name} in file {finding[0]['path']} at line(s) {', '.join(map(str, finding[0]['line_numbers']))}\n")
                    save.close()
                print(f"{label.info} Remediations:")
                for remedy in remediator:
                    print(f"{Fore.YELLOW}> {remedy}{Fore.RESET}")
                print(f"---")
        except Exception as e:
            pass
    
def dangrousPermission(apkpath, output):
    print(f"{label.info} Analyzing Permissions of Provided APK: {Style.BRIGHT}{apkpath}.apk{Style.RESET_ALL}")
    DANGEROUS_TYPES = [
            "android.permission.READ_CALENDAR",
            "android.permission.WRITE_CALENDAR",
            "android.permission.CAMERA",
            "android.permission.READ_CONTACTS",
            "android.permission.WRITE_CONTACTS",
            "android.permission.GET_ACCOUNTS",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.RECORD_AUDIO",
            "android.permission.READ_PHONE_STATE",
            "android.permission.READ_PHONE_NUMBERS",
            "android.permission.CALL_PHONE",
            "android.permission.ANSWER_PHONE_CALLS",
            "android.permission.READ_CALL_LOG",
            "android.permission.WRITE_CALL_LOG",
            "android.permission.ADD_VOICEMAIL",
            "android.permission.USE_SIP",
            "android.permission.PROCESS_OUTGOING_CALLS",
            "android.permission.BODY_SENSORS",
            "android.permission.SEND_SMS",
            "android.permission.RECEIVE_SMS",
            "android.permission.READ_SMS",
            "android.permission.RECEIVE_WAP_PUSH",
            "android.permission.RECEIVE_MMS",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.MOUNT_UNMOUNT_FILESYSTEMS",
            "android.permission.READ_HISTORY_BOOKMARKS",
            "android.permission.WRITE_HISTORY_BOOKMARKS",
            "android.permission.INSTALL_PACKAGES",
            "android.permission.RECEIVE_BOOT_COMPLETED",
            "android.permission.READ_LOGS",
            "android.permission.CHANGE_WIFI_STATE",
            "android.permission.DISABLE_KEYGUARD",
            "android.permission.GET_TASKS",
            "android.permission.BLUETOOTH",
            "android.permission.CHANGE_NETWORK_STATE",
            "android.permission.ACCESS_WIFI_STATE",
        ]
    try:
        appInfo = appinfo(apkpath)
        permissions = appInfo['permissions']
        for permission in permissions:
            if permission in DANGEROUS_TYPES:
                print(f"{label.warn} Found a Possible {Fore.RED}DANGEROUS{Fore.RESET} permission: {Style.BRIGHT}{permission}{Style.RESET_ALL}")
                save = open(output, "a")
                save.write(f"Found a DANGEROUS permission: {permission}\n")
                save.close()
        print(f"{label.info} Analysis Completed Successfully")
    except Exception as e:
        print(f"{label.error} Error analyzing permissions: {e}")
        pass



