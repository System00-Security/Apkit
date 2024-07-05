import os
import re
from libs.banner import label
from colorama import Style, Fore

def linkExtractor(apkpath):
    link_pattern = r'\b((?:https?|ftp)://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))'
    extracted_path = apkpath.split("/")[-1].replace(".apk", "")
    links = []
    notAllowedLinks = ["google.com", "facebook.com", "instagram.com", "twitter.com", "youtube.com","android.com","w3.org","wikipedia.org","mozilla.org","github.com","apache.org","creativecommons.org","gnu.org","sourceforge.net","ietf.org","opengis.com"
    ,"googlesource.com","codebeautify",".png",".jpg",".gif","opengis.net","googleadservice","googlesyndication.com","crashlytics.com","adobe.com","publicsuffix.com","publicsuffix.org"]
    for root, dirs, files in os.walk(extracted_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding='latin-1') as f:
                    data = f.read()
                    for match in re.finditer(link_pattern, data):
                        link = match.group()
                        if not any(ban in link for ban in notAllowedLinks):
                            links.append(link)
    
            except Exception as e:
                return False
    return links

def findHardcodedCredentials(apkpath):
    credentials_patterns = {
        "API_Key": r"[aA][pP][iI]_?[kK][eE][yY].*['\"]([0-9a-zA-Z]{32,45})['\"]",
        "Bearer_Token": r"[bB][eE][aA][rR][eE][rR]\s([a-zA-Z0-9\-._~+/]+=*)",
        "Basic_Auth_Credentials": r"([a-zA-Z0-9_]+:[a-zA-Z0-9_]+)@[a-zA-Z0-9_.-]+\.[a-zA-Z]{2,}",
        "Google_API_Key": r"(AIza[0-9A-Za-z-_]{35})",
        "Google_OAuth_Token": r"(ya29\.[0-9A-Za-z-_]+)",
        "GitHub_Token": r"[gG][iI][tT][hH][uU][bB].*['\"]([0-9a-fA-F]{40})['\"]",
        "Slack_Token": r"(xox[baprs]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24,32})",
        "Twilio_API_Key": r"(SK[0-9a-fA-F]{32})",
        "Stripe_API_Key": r"(sk_live_[0-9a-zA-Z]{24})",
        "Mailgun_API_Key": r"(key-[0-9a-zA-Z]{32})",
        "Firebase_URL": r"(https:\/\/[a-zA-Z0-9-]+\.firebaseio\.com)",
        "MailChimp_API_Key": r"[0-9a-f]{32}-us[0-9]{1,2}",
	    "Mailgun_API_Key": r"key-[0-9a-zA-Z]{32}",
	    "Mailto": r"(?<=mailto:)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9.-]+",
	    "Password_in_URL": r"[a-zA-Z]{3,10}://[^/\\s:@]{3,20}:[^/\\s:@]{3,20}@.{1,100}[\"'\\s]",
        "PayPal_Braintree_Access_Token": r"access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}",
        "Google_Cloud_Platform_OAuth": r"[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
        "Google_Cloud_Platform_Service_Account": r"\"type\": \"service_account\"",
        "Google_OAuth_Access_Token": r"ya29\\.[0-9A-Za-z\\-_]+",
        "HackerOne_CTF_Flag": r"[h|H]1(?:[c|C][t|T][f|F])?\\{.*\\}",
        "HackTheBox_CTF_Flag": r"[h|H](?:[a|A][c|C][k|K][t|T][h|H][e|E][b|B][o|O][x|X]|[t|T][b|B])\\{.*\\}$"
    }
    print(f"{label.info} Searching for hardcoded credentials in APK: {apkpath}")
    extracted_path = apkpath.split("/")[-1].replace(".apk", "")
    for root, dirs, files in os.walk(extracted_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding='latin-1') as f:
                    data = f.read()
                    for key, pattern in credentials_patterns.items():
                        for match in re.finditer(pattern, data):
                            print(f"{label.warn} Found {Style.BRIGHT}{key}{Style.RESET_ALL} in file {Fore.BLUE}{file_path}{Fore.RESET}: {Fore.RED}{match.group(1)}{Fore.RESET}")
            except Exception as e:
                print(f"{label.error} Could not read file {file_path}: {e}")

