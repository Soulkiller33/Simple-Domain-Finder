### Super Simple Subdomain Finder ###



import requests
import argparse
from colorama import Fore, Style, init
init(autoreset=True) ### Color codes output in terminal ###


### Example Usage ###
example_text = """
Example:
  python SubdomainFinder.py --domain example.com --timeout 2 --https --output found.txt --wordlist mysubdomains.txt
"""


### Used for --help ###
custom_usage = "SubdomainFinder.py --domain DOMAIN [--timeout TIMEOUT] [--https] [--output FILE] [--wordlist FILE]"



### Setting argparse ###
parser = argparse.ArgumentParser(
    description="Simple Domain Finder",
    usage=custom_usage,
    epilog=example_text,
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument("--domain", required=True, help="Base domain to scan (e.g. test.com)")
parser.add_argument("--timeout", type=float, default=1.0, help="Timeout for requests in seconds")
parser.add_argument("--https", action='store_true', help="Scan using HTTPS instead of HTTP")
parser.add_argument("--output", type=str, help="Save results to file")
parser.add_argument("--wordlist", type=str, help="Path to custom subdomain wordlist file (use full path)")

args = parser.parse_args()



### Set protocol ##
protocol = "https" if args.https else "http"



### Subdomains scans ###
subdomains = [
    'www',       # almost always exists
    'mail',      # email servers
    'ftp',       # file transfer servers
    'api',       # common attack surface
    'admin',     # admin panels
    'portal',    # login portals
    'webmail',   # email access
    'dev',       # development environments
    'test',      # test environments
    'staging',   # pre-production env
    'beta',      # beta versions
    'login',     # authentication
    'auth',      # alternative login/auth
    'dashboard', # admin/user dashboards
    'cpanel',    # common hosting panel
    'vpn',       # remote access
    'owa',       # Outlook Web Access (Microsoft)
    'secure',    # often tied to sensitive pages
    'support',   # helpdesk systems
    'blog'       # CMS (e.g., WordPress, Ghost)
]

### Wordlist input ###
if args.wordlist:
    try:
        with open(args.wordlist, 'r') as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{Fore.RED}Failed to load wordlist file: {e}")
        print("Using default subdomains list instead.")


### Stores found URL ###
found = []
print(f"\n [•] Scanning subdomains for: {args.domain} using {protocol.upper()}...\n")





### Scan loop ###


for sub in subdomains:
    url = f"{protocol}://{sub}.{args.domain}"
    try:
        response = requests.get(url, timeout=args.timeout)
        status = response.status_code
        if status < 400:
            print(f"{Fore.GREEN}[+] Found: {url} (Status: {status})")
            found.append(url)
        else:
            print(f"{Fore.YELLOW}[-] {url} responded with status code: {status}")
    except requests.ConnectionError:
        print(f"{Fore.RED}[!] Connection failed for URL {url}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error with {url}: {e}")




### Save to file ###
if args.output:
    try:
        with open(args.output, "w") as f:
            for url in found:
                f.write(url + "\n")
        print(f"\n{Fore.CYAN}Results saved to {args.output}")
    except Exception as e:
        print(f"{Fore.RED}Failed to save output: {e}")
