import urllib.request, time, ctypes, os
from colorama import init, Fore, Style


init()

ctypes.windll.kernel32.SetConsoleTitleW(f"Scraping Proxies - Scraped: 0 | Failed: 0")

with open("raw.txt", "r") as f:
    urls = [line.strip() for line in f.readlines()]

unique_lines = set()

scraped = 0
failed = 0

for url in urls:
    print(f"{Fore.GREEN}[!] {Fore.RESET}SCRAPING{Fore.LIGHTCYAN_EX} {url}")
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
        lines = data.split("\n")
        total_lines = len(lines)
        if total_lines == 1:
            failed += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Scraping Proxies - Scraped: {scraped} | Failed: {failed}")
            print(f"{Fore.RED}[!] {Fore.RESET}NO PROXIES FOUND{Fore.LIGHTCYAN_EX}")
        else:
            for i, line in enumerate(lines):
                if line.strip() != "":
                    unique_lines.add(line.strip())
                scraped += 1
                ctypes.windll.kernel32.SetConsoleTitleW(f"Scraping Proxies - Scraped: {scraped} | Failed: {failed}")
                progress = int((i + 1) / total_lines * 20)
                loading_bar = f"{Fore.GREEN}[{'=' * progress}{' ' * (20 - progress)}]{Fore.RESET}"
                print(f"\r{loading_bar} {i+1}/{total_lines}", end="")
            print()
    except urllib.error.HTTPError:
        print(f"{Fore.RED}[!] {Fore.RESET}HTTP ERROR 403: FORBIDDEN{Fore.LIGHTCYAN_EX}")
        failed += 1
    except:
        print(f"{Fore.RED}[!] {Fore.RESET}FAILED TO SCRAPE{Fore.LIGHTCYAN_EX}")
        failed += 1

unique_lines = list(unique_lines)
unique_lines.sort()

with open("proxies.txt", "a+") as f:
    f.seek(0)
    existing_proxies = set(line.strip() for line in f.readlines())
    for line in unique_lines:
        if line.strip() not in existing_proxies:
            f.write(line.strip() + "\n")

with open("proxies.txt", "r") as f:
    proxies = [line.strip() for line in f.readlines()]

proxies = list(filter(lambda x: x != "", proxies))

with open("proxies.txt", "w") as f:
    for proxy in proxies:
        f.write(proxy + "\n")

print(f"{Fore.YELLOW}[!] FINISHED - {len(unique_lines)} new proxies scraped and saved to proxies.txt{Fore.RESET}")
ctypes.windll.kernel32.SetConsoleTitleW(f"Scraping Proxies - Scraped: {scraped} | Failed: {failed} | Completed")

unique_urls = list(set(urls))
num_duplicates = len(urls) - len(unique_urls)

if num_duplicates > 0:
    print(f"{Fore.GREEN}[!] {num_duplicates} DUPLICATE URL(S) REMOVED{Fore.RESET}")
else:
    print(f"{Fore.YELLOW}[!] NO DUPLICATE URLS FOUND{Fore.RESET}")

with open("proxies.txt", "r") as f:
    proxies = [line.strip() for line in f.readlines()]

proxies = list(filter(lambda x: x != "", proxies))

valid_proxies = []

for proxy in proxies:
    if proxy.count(".") == 3 and proxy.count(":") == 1:
        valid_proxies.append(proxy)

with open("proxies.txt", "w") as f:
    for proxy in valid_proxies:
        f.write(proxy + "\n")

with open("proxies.txt", "r") as f:
    lines = f.readlines()

# Remove lines that don't start with a number
lines = [line for line in lines if line.strip() and line.strip()[0].isdigit()]

with open("proxies.txt", "w") as f:
    f.write("".join(lines))


print(f"{Fore.GREEN}[!] FINISHED - {len(valid_proxies)} new proxies scraped and saved to proxies.txt{Fore.RESET}")

print("")
print(f"{Fore.LIGHTBLUE_EX}Press enter to continue...{Style.RESET_ALL}")
input("")
os.system('cls')