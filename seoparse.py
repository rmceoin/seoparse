#!/usr/bin/env python3

#
# seoparse.py
#
# Parse an HTML file from a SEO poisoned site
#

import re
import sys
import time
import urllib
from os import mkdir, path

import requests
import validators
from bs4 import BeautifulSoup

DEBUG = False
MAX_URLS = 90000

domains = {}
base_domains = {}
jobdir = ""
urls = []
depth = 0

requests.packages.urllib3.disable_warnings() 
sys.setrecursionlimit(3000)

IGNORE_FILENAME = "ignore.txt"
IGNORE_CUSTOM_FILENAME = "ignore-custom.txt"

ignore = []

def read_list(filename: str) -> list:
    data_list = []
    if path.exists(filename):
        file = open(filename, 'r')
        data = file.read()
        for line in data.split('\n'):
            if line:
                data_list.append(line)
    return data_list

ignore += read_list(IGNORE_FILENAME)
ignore += read_list(IGNORE_CUSTOM_FILENAME)

ignore_list="|".join(ignore)
re_ignore=r"("+ignore_list+")"

def print_domains():
    print(f'Base domains found: {len(base_domains)-1}\n')
    for base_domain in sorted(base_domains.keys()):
        print(f'{base_domain}')

def get_page(url: str) -> str:
    if validators.url(url):
        print(f'Getting {url}')
        try:
            response = requests.get(url, timeout=30, verify=False)
        except requests.exceptions.Timeout:
            print("Timeout")
            return None

        return response.text
    print(f"Not a valid URL: {url}")
    return None

def parse_page(url: str):
    global depth
    global urls

    print(f'PAGE:{depth} {url}')
    depth += 1

    html_text = get_page(url)

    if html_text:
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.replace("/","+")
        filename = f"{jobdir}/{parsed.netloc}{path}"
        if DEBUG:
            print(f"filename={filename}")
        output_file = open(filename, "w")
        output_file.write(html_text)
        output_file.close()

        soup = BeautifulSoup(html_text, 'html.parser')

        page_urls = []

        for link in soup.find_all('a'):
            href=link.get('href')
            if href:
                parsed = urllib.parse.urlparse(href)

                ig = re.search(re_ignore, parsed.netloc)
                if not ig:

                    base_domain = ".".join(parsed.netloc.split(".")[::-1][0:2][::-1])
                    # print(f"base_domain={base_domain}")

                    if base_domain in base_domains:
                        base_domains[base_domain] += 1
                    else:
                        base_domains[base_domain] = 1

                        if href not in page_urls:
                            page_urls.append(href)
                            if DEBUG:
                                print(f'PAGE_URL: {href}')

                    if parsed.netloc in domains:
                        domains[parsed.netloc] += 1
                    else:
                        domains[parsed.netloc] = 1

                else:
                    print(f'Ignore {href}')

        print(f"{len(page_urls)} page_urls found")
        for page_url in page_urls:
            if page_url not in urls:
                urls.append(page_url)
                if len(urls) < MAX_URLS:
                    if depth < (sys.getrecursionlimit() - 100):
                        parse_page(page_url)
                    else:
                        print('Max recursion')
                else:
                    print(f'Max urls {MAX_URLS}')
    depth -= 1

try:
    argument = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <url>")

if 'http' in argument:
    parsed = urllib.parse.urlparse(argument)
    domains[parsed.netloc] = 1

    jobdir = "job." + parsed.netloc + "." + str(int(time.time()))
    mkdir(jobdir)
    print(f"jobdir={jobdir}")

    parse_page(argument)
else:
    print(f'Error: must be url: {argument}')
    sys.exit(1)

if urls:
    print(f'URLs found: {len(urls)}')

if domains:
    print_domains()
