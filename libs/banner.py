from colorama import Fore, Style, Back
def banner():
    print(f"""
╔═╗╔═╗╦╔═  {Style.BRIGHT}A P K i t {Style.RESET_ALL}  
╠═╣╠═╝╠╩╗  {Fore.RED}{Style.BRIGHT}D3V~>{Style.RESET_ALL} ARMx64
╩ ╩╩  ╩ ╩  {Fore.BLACK}{Style.BRIGHT}ⓒ System00 Security{Style.RESET_ALL}
.   .    . 
Combined Utility for Android Application {Fore.RED}Reversing{Fore.RESET} and {Fore.GREEN}Analysis{Fore.RESET}
.   .    . 
""")
    
class label:
    info = f"{Fore.BLUE}[INFO]{Fore.RESET}"
    warn = f"{Fore.YELLOW}[WARN]{Fore.RESET}"
    error = f"{Fore.RED}[ERRR]{Fore.RESET}"
    code = f"{Fore.CYAN}[CODE]{Fore.RESET}"
    done = f" > {Back.GREEN}{Fore.WHITE} DONE {Fore.RESET}{Back.RESET}"
