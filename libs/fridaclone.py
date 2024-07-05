import requests
from bs4 import BeautifulSoup
import re
from libs.banner import label

def fridaGET(slag):
    url = f"https://codeshare.frida.re/@"+slag
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', string=re.compile(r"projectSource"))
    if not script_tag:
        return "Project Data not found."
    script_text = script_tag.string
    if not script_text:
        return "Content not found."
    pattern = r"projectSource: \"(.*?)\""
    match = re.search(pattern, script_text, re.DOTALL)
    if match:
        plain_text = match.group(1)
    plain_text = (plain_text.encode('utf-8')
                  .decode('unicode_escape')
                  .replace(r'\u002D', '-')
                  .replace(r'\u0022', '"')
                  .replace(r'\u000A', '\n')
                  .replace(r'\u003B', ';'))

    return plain_text

def fridaClone(slag):
    try:
        slagn = slag.split("/")[1]
        print(f"{label.info} Cloning Frida Script: {slag}")
        script = fridaGET(slag)
        if script:
            with open(f"{slagn}.js", "w") as f:
                f.write(script)
            print(f"{label.done} Cloned Frida Script: {slagn}.js")
        else:
            print(f"{label.error} Error cloning Frida Script: {slag}")
    except Exception as e:
        print(f"{label.error} Error cloning Frida Script: {e}")
