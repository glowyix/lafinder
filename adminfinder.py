#!/usr/bin/env python3

import requests
import sys
from urllib.parse import urljoin
from colorama import Fore, Style, init
from alive_progress import alive_bar
from bs4 import BeautifulSoup
import pyfiglet

# Initialize colorama
init(autoreset=True)

def print_title():
    """Programın başlığını ASCII sanatıyla yazdırır."""
    title = "Admin Finder"
    try:
        # Orta boyutlu bir yazı tipi kullanarak başlığı yazdırır
        ascii_art = pyfiglet.figlet_format(title, font="standard")
        print(Fore.WHITE + ascii_art)
    except pyfiglet.FontNotFound:
        print(Fore.RED + "Belirtilen yazı tipi bulunamadı.")

def is_admin_page(html_content):
    """HTML içeriğinde admin paneli olup olmadığını kontrol eder."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Basit bir kontrol, daha detaylı kontrol yapılabilir
    admin_keywords = ["admin", "admincp", "adminpanel", "administrator", "cp", "controlpanel", "webadmin"]
    if any(keyword in soup.get_text().lower() for keyword in admin_keywords):
        return True
    
    return False

def find_admin_pages(base_url, paths_file):
    """Verilen base_url ve paths_file içindeki yolları kullanarak admin sayfalarını bulur."""
    with open(paths_file, 'r') as file:
        paths = file.read().splitlines()

    admin_pages = []
    
    with alive_bar(len(paths), title='Tarama devam ediyor') as bar:
        for path in paths:
            url = urljoin(base_url, path)
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    if is_admin_page(content):
                        if url not in admin_pages:
                            admin_pages.append(url)
                    
            except requests.RequestException as e:
                print(Fore.RED + f"Error accessing {url}: {e}")
            bar()
    
    return admin_pages

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(Fore.RED + f"Kullanım: {sys.argv[0]} -u <base_url> -p <paths_file>")
        sys.exit(1)

    base_url = None
    paths_file = None

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "-u":
            base_url = sys.argv[i+1]
        elif sys.argv[i] == "-p":
            paths_file = sys.argv[i+1]

    if not base_url or not paths_file:
        print(Fore.YELLOW + "Base URL ve paths file belirtilmelidir.")
        sys.exit(1)

    print_title()  # Başlığı yazdır

    print(Fore.CYAN + "Tarama başlatılıyor...")
    admin_pages = find_admin_pages(base_url, paths_file)
    
    # Tarama sonuçlarını yazdır
    if admin_pages:
        print(Fore.CYAN + "\nAdmin sayfaları:")
        for page in admin_pages:
            print(Fore.YELLOW + page)
    else:
        print(Fore.RED + "Admin sayfaları bulunamadı.")

















































#CODEBYGLOWYIX
