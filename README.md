# APkit (BETA)

<p align="center">
  <img src="https://i.ibb.co/XxGH29G/apkit.png" width="200" alt="APkit Logo">
</p>

APkit is a powerful tool designed for analyzing security vulnerabilities and reversing Android APK files. Currently in Beta Phase, See [Screenshots](https://github.com/System00-Security/Apkit/tree/main/demoshots).
 <p align="center">
  <a href="https://github.com/System00-Security/Apkit/">
    <img src="https://img.shields.io/static/v1?label=Project&message=APKit&color=green">
  </a>
    <a href="https://github.com/System00-Security/Apkit/">
    <img src="https://img.shields.io/static/v1?label=Update&message=V1.0_beta&color=green">
  </a>
</p>

## Usage
```
$ git clone https://github.com/System00-Security/Apkit
$ cd Apkit
$ chmod +x dependency.sh
$ python3 apkit.py --help

```

## Requirements
#### Run dependency.sh to Fullfill all dependency
```
$ pip3 install colorama
$ sudo pip3 install frida
$ sudo pip3 install frida-tools
$ pip3 install androguard==3.4.0a1
$ sudo apt install openjdk8 # install jdk8
```

## Reporting Issues

If you encounter any bugs or issues while using APkit, please help us improve by reporting them. You can create a new issue on our [GitHub Issues page](https://github.com/System00-Security/Apkit/issues).

Your feedback is valuable to us as we work to enhance APkit and make it more effective for security analysis.

## Features
- **Frida CodeShare Cloner**
  - Clone frida script using `-fc pcipolloni/universal-android-ssl-pinning-bypass-with-frida/`

- **Dynamic Analysis Tools:**
  - **SSL Unpinning:** Bypass SSL Pinning mechanisms in APKs (`-sslp`, `-cert`, `-adb` options).
  - **Certificate Pinning:** Manage SSL certificates for testing (`-cert` option).
  - **Automated Actions:** Automate Frida SSL unpinning actions with ADB (`-adb` option).

- **Static Analysis Tools:**
  - **APK Decompilation:** Extract and decompile APKs for further analysis (`-an` option).
  - **Generic Analysis:** Perform generic analysis on decompiled APKs (`-an generic` option).
  - **OWASP Mobile Top 10:** Analyze APKs for OWASP Mobile Top 10 vulnerabilities (`-an owasp` option).

- **Security Checks:**
  - **Dangerous Permissions:** Check APKs for dangerous permissions (`-dp` option).

- **Data Extraction:**
  - **API Key Extraction:** Extract API keys embedded in APKs (`-ex api_key` option).
  - **URL Extraction:** Extract URLs from decompiled APKs (`-ex urls` option).

## Requirements
```
$ pip3 install colorama
$ sudo pip3 install frida
$ sudo pip3 install frida-tools
$ pip3 install androguard==3.4.0a1
$ sudo apt install openjdk8 # install jdk8
```

## Special Thanks

I extend my sincere gratitude to the following individuals and communities for their invaluable contributions, support, and inspiration:

- **[OWASP Mobile Security Testing Guide (MASTG)](https://mas.owasp.org/MASTG/techniques/#android-techniques)**: For their exceptional Android techniques cheatsheet.
- **[Frida](https://frida.re/)**: For creating this remarkable masterpiece.

And to all who have inspired this project.


## Contributors

We welcome contributions from anyone interested in improving this project. To contribute, simply create a pull request with your proposed changes.

Your contributions, whether they involve code improvements, bug fixes, documentation enhancements, or new features, are greatly appreciated and help make this project better for everyone.

Thank you for considering contributing to our project!





