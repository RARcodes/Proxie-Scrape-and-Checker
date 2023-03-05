import urllib.request
import threading
import time
import os
import colorama
from colorama import Fore, Back, Style
import ctypes

colorama.init(autoreset=True)

checked = 0
working = 0
dead = 0

# function to check if proxy is bad
def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('http://www.google.com')
        sock=urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        # print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        # print("ERROR:", detail)
        return True
    return False

def read_proxies():
    with open('proxies.txt', 'r') as f:
        proxies = f.readlines()
    return [p.strip() for p in proxies]

def check_proxies(proxies):
    global checked, working, dead
    for item in proxies:
        checked += 1
        if is_bad_proxy(item):
            print(Fore.RED + "[-] Bad Proxy: " + item)
            ctypes.windll.kernel32.SetConsoleTitleW(f"Checking proxies - Working: {working} | Dead: {dead}")
            dead += 1
        else:
            print(Fore.GREEN + "[+] Working Proxy: " + item)
            working += 1
            with open('alive.txt', 'a') as f:
                f.write(item + '\n')
            ctypes.windll.kernel32.SetConsoleTitleW(f"Checking proxies - Working: {working} | Dead: {dead}")

def main():
    proxies = read_proxies()
    num_threads = int(input("Enter the number of threads to use (recommended: 50): "))
    chunk_size = len(proxies) // num_threads
    threads = []

    for i in range(num_threads):
        chunk_start = i * chunk_size
        if i == num_threads - 1:
            chunk_end = len(proxies)
        else:
            chunk_end = (i + 1) * chunk_size
        chunk = proxies[chunk_start:chunk_end]
        t = threading.Thread(target=check_proxies, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(Fore.GREEN + "\n[+] Done! Checked {checked} proxies, {working} working, {dead} dead.")
    print(Fore.GREEN + "Working proxies saved in 'alive.txt'")
    ctypes.windll.kernel32.SetConsoleTitleW(f"Checked proxies - Working: {working} | Dead: {dead} | Completed")

if __name__ == '__main__':
    main()
