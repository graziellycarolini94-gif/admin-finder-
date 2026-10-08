#!/usr/bin/env python3
import requests
import sys
from concurrent.futures import ThreadPoolExecutor

BLUE = "\033[94m"
RESET = "\033[0m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"

banner = rf"""
{BLUE}
  ___ ____ __ __ ___ _ _ _____ ___ _ _ ____ _____ ____
 / _ \ | _ \| \/ |_ _| \ | | | ___|_ _| \ | | _ \| ____| _ \
| |_| || | | | |\/| || || \| | | |_ | || \| | | | | _| | |_) |
| _ || |_| | | | || || |\ | | _| | || |\ | |_| | |___| _ <
|_| |_||____/|_| |_|___|_| \_| |_| |___|_| \_|____/|_____|_| \_\
{RESET}
{YELLOW} [ V3 - Threaded | Red Team | Blue Team ]{RESET}
"""

print(banner)

if len(sys.argv) < 2:
    print(f"{YELLOW}Uso: python admin_finder_v3.py http://demo.testfire.net{RESET}")
    sys.exit(1)

url = sys.argv[1].rstrip("/")
if not url.startswith("http"):
    url = "http://" + url

paths = [
"admin","admin/","administrator","admin/login","admin/login.php","admin.php",
"adminpanel","admin-panel","admin_area","admin-area","adminLogin","wp-admin",
"wp-login.php","cpanel","login","admin1","admin2","admin/account",
"admin/dashboard","admin_area/admin","admin_area/login","adminpanel.php","admin/index.php",
"admin/login.html","admin/index.html","admin_area/index.php","bb-admin","admin2.asp",
"admin2.php","admin/index2.php","admin/index.asp","admin.php","admin.asp"
]

print(f"{BLUE}[*] Alvo: {url}{RESET}")
print(f"{BLUE}[*] Threads: 10 | Salvando em resultados.txt{RESET}\n")

headers = {"User-Agent": "Mozilla/5.0"}
encontrados = []

def check(path):
    full_url = f"{url}/{path}"
    try:
        r = requests.get(full_url, headers=headers, timeout=10, allow_redirects=False, verify=False)
        if r.status_code == 200:
            print(f"{GREEN}[+] ENCONTRADO {r.status_code} -> {full_url}{RESET}")
            encontrados.append(full_url)
        elif r.status_code in [301,302,403,401]:
            print(f"{YELLOW}[!] POSSIVEL {r.status_code} -> {full_url}{RESET}")
            encontrados.append(f"{full_url} [{r.status_code}]")
        else:
            print(f"{RED}[-] {r.status_code} -> {full_url}{RESET}")
    except:
        print(f"{RED}[-] TIMEOUT -> {full_url}{RESET}")

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(check, paths)

with open("resultados.txt","w") as f:
    for item in encontrados:
        f.write(item+"\n")

print(f"\n{BLUE}[*] Finalizado. {len(encontrados)} possíveis encontrados.{RESET}")
print(f"{GREEN}[*] Salvo em resultados.txt{RESET}")
  
#!/usr/bin/env python3
import requests, sys, re
from concurrent.futures import ThreadPoolExecutor

C = {"g":"\033[92m","y":"\033[93m","r":"\033[91m","b":"\033[94m","e":"\033[0m"}

print(f"{C['b']} Scan threaded com titulo e WAF check {C['e']}")

if len(sys.argv) < 2:
    print("Uso: python scan.py http://demo.testfire.net")
    sys.exit(1)

url = sys.argv[1].rstrip("/")
headers = {"User-Agent":"Mozilla/5.0"}

paths = ["admin","admin/","administrator","admin/login","wp-admin","login","cpanel","admin/account","admin/dashboard"]

def get_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.I)
    return m.group(1)[:40] if m else ""

def check(p):
    full = f"{url}/{p}"
    try:
        r = requests.get(full, headers=headers, timeout=8, allow_redirects=False, verify=False)
        title = get_title(r.text) if r.status_code==200 else ""
        # WAF simples
        waf = "WAF?" if "cloudflare" in str(r.headers).lower() else ""
        if r.status_code==200:
            print(f"{C['g']}[200] {full} | {title} {waf}{C['e']}")
        elif r.status_code in [301,302,403,401]:
            print(f"{C['y']}[{r.status_code}] {full} {waf}{C['e']}")
        else:
            print(f"{C['r']}[-] {r.status_code} {full}{C['e']}")
    except Exception as e:
        print(f"[-] erro {full}")

with ThreadPoolExecutor(max_workers=10) as ex:
    ex.map(check, paths)

print("Fim - use apenas em alvos autorizados.")
