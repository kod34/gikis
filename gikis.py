#!/usr/bin/env python3

import argparse
import os
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urldefrag, urlparse
import validators
from tldextract import extract
import numpy as np
import platform

### ARGUMENTS (URL, OUTPUT DIR, LEVEL)

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-u", dest="url",help="Specify a url", required=True)
requiredNamed.add_argument("-o", dest="out",help="Specify an output directory", required=True)
requiredNamed.add_argument("-l", dest="lvl",help="Specify a level (basic, light, moderate, deep)", required=True)
requiredNamed.add_argument("-d", dest="delay",help="Specify a download delay")
args = parser.parse_args()

### FUNCTIONS

# split url into "https", "www.example.com", "/index.html"
class splitlink:
    def __init__(self, link):
        co = urlparse(link)
        self.scheme = co.scheme
        self.hostname = co.hostname
        self.path = co.path
        
class extr:
    def __init__(self, link):
        self.tsd, self.td, self.tsu = extract(str(link))

# checks url reachability
def checklink(link):
    print('[+] Checking availability of <'+str(link)+'>...', end='')
    sys.stdout.flush()
    try:
        reqs = requests.get(splitlink(link).scheme+'://'+splitlink(link).hostname)
        if reqs.status_code == 200:
            print('[OK]\n')
    except requests.exceptions.ConnectionError as E1:
        sys.exit('[X] Website unreachable')
    except requests.exceptions.MissingSchema as E2:
        sys.exit(E2)
    except KeyboardInterrupt:
        sys.exit('\n[!] User Interrupt')
    
# get hrefs found in source code of url web page
def looplinks(link, dalist):
    try:
        reqs = requests.get(link)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        for l in soup.find_all(['a', 'link', 'script', 'img']):
            if l.get('href'):
                x = l.get('href')
                if validators.url(str(x)) and extr(link).tsd+'.'+extr(link).td+'.'+extr(link).tsu == extr(x).tsd+'.'+extr(x).td+'.'+extr(x).tsu:
                    dalist.append(x)
                    print(x, end ='\n')
                else:
                    formatted_x = urljoin(splitlink(link).scheme+'://'+extr(link).tsd+'.'+extr(link).td+'.'+extr(link).tsu, str(x))
                    if formatted_x and validators.url(formatted_x) and extr(link).tsd+'.'+extr(link).td+'.'+extr(link).tsu == extr(formatted_x).tsd+'.'+extr(formatted_x).td+'.'+extr(formatted_x).tsu:
                        dalist.append(urldefrag(formatted_x)[0])
                        print(urldefrag(formatted_x)[0], end='\n')
            if l.get('src'):
                y = l.get('src')
                if validators.url(str(y)) and extr(link).tsd+'.'+extr(link).td+'.'+extr(link).tsu == extr(y).tsd+'.'+extr(y).td+'.'+extr(y).tsu:
                    dalist.append(y)
                    print(y, end ='\n')
                else:
                    formatted_y = urljoin(splitlink(link).scheme+'://'+extr(link).tsd+'.'+extr(link).td+'.'+extr(link).tsu, str(y))
                    if formatted_y and validators.url(formatted_y) and extr(link).tsd+'.'+extr(link).td+'.'+extr(link).tsu == extr(formatted_y).tsd+'.'+extr(formatted_y).td+'.'+extr(formatted_y).tsu:
                        dalist.append(urldefrag(formatted_y)[0])
                        print(urldefrag(formatted_y)[0], end='\n')
    except KeyboardInterrupt:
        sys.exit('\n[!] User Interrupt')

# levels
def getlink2():    
    for u in np.unique(href_list):
        looplinks(u, href_list2)
        
def getlink3():    
    for u in np.unique(href_list2):
        looplinks(u, href_list3)
        
def getlink4():    
    for u in np.unique(href_list3):
        looplinks(u, href_list4)
        
def getlink5():    
    for u in np.unique(href_list4):
        looplinks(u, href_list5)
        

# check passed argument
def check():
    global url, lvl, out, delay
    url = args.url
    lvl = args.lvl
    out = args.out
    try:
        delay = int(args.delay)
    except ValueError:
        parser.error("The delay argument must be an integer")
        
    if delay == None:
        delay = 0
    try:
        if not os.path.isdir(out):
            os.makedirs(out, exist_ok=True)
        else:
            while not validators.url(url):
                url = input('Invalid url, try again: ')
    except KeyboardInterrupt:
        sys.exit('\n[!] User Interrupt')
        
# make folders

def downfol():
    for f in href_full_list:
        fol = splitlink(f).path.strip('/')
        fol_list = fol.split('/')
        root, ext = os.path.splitext(f)
        if ext:
            if 'Linux' in platform.system():
                fol_final = '/'.join(fol_list[:-1])
            elif "Windows" in platform.system():
                fol_final = '\\'.join(fol_list[:-1])
            else:
                sys.exit("\n[-] Platform not supported.")
        else:
            fol_final = fol
        os.makedirs(os.path.join(out, fol_final), exist_ok=True)

        
                 
# download files

def downfile():
    for f in href_full_list:
        if 'Linux' in platform.system():
            fol = splitlink(f).path.strip('/')
        elif 'Windows' in platform.system():
            fol = splitlink(f).path.strip('/').replace('/', '\\')
        else:
            sys.exit("\n[-] Platform not supported.")
        root, ext = os.path.splitext(f)
        if ext:
            fold2do = os.path.join(out, fol)
            try:
                file2do = requests.get(f, stream=True)
            except requests.exceptions.ConnectionError:
                sys.exit('\n[-] Connection Error.')
            print('\nDownloading <'+f+'>...', end='')
            sys.stdout.flush()
            try:open(fold2do, "wb").write(file2do.content)
            except IsADirectoryError:pass
            try:
                print('\nFixing paths...', end='')
                abspath(fold2do)
            except IsADirectoryError:
                pass 
            print('\nWaiting '+str(delay)+' seconds...', end='')
            time.sleep(delay)
            
            
# fix paths

def abspath(file):
    with open(file, 'r', encoding="utf8", errors='ignore') as f:
        soupfile = BeautifulSoup(f, 'html.parser')
        for t in soupfile.find_all(['a', 'link', 'script', 'img']):
            if 'Linux' in platform.system():
                try:
                    if not validators.url(t['href']):
                        t['href'] = os.path.join(os.path.abspath(out), t['href'].strip('/'))
                    else:
                        t['href'] = os.path.join(os.path.abspath(out), splitlink(t['href']).path.strip('/'))
                except KeyError:
                    pass
                try:
                    if not validators.url(t['src']):
                        t['src'] = os.path.join(os.path.abspath(out), t['src'].strip('/'))
                    else:
                        t['src'] = os.path.join(os.path.abspath(out), splitlink(t['src']).path.strip('/'))
                except KeyError:
                    pass
            elif 'Windows' in platform.system():
                try:
                    if not validators.url(t['href']):
                        t['href'] = os.path.join(os.path.abspath(out), t['href'].strip('/').replace('/', '\\'))
                    else:
                        t['href'] = os.path.join(os.path.abspath(out), splitlink(t['href']).path.strip('/').replace('/', '\\'))
                except KeyError:
                    pass
                try:
                    if not validators.url(t['src']):
                        t['src'] = os.path.join(os.path.abspath(out), t['src'].strip('/').replace('/', '\\'))
                    else:
                        t['src'] = os.path.join(os.path.abspath(out), splitlink(t['src']).path.strip('/').replace('/', '\\'))
                except KeyError:
                    pass
            else:
                sys.exit("\n[-] Platform not supported.")
    with open(file, 'w') as f:
        f.write(str(soupfile))
    f.close()

### BANNER

banner = ''' 
       _ _    _     
  __ _(_) | _(_)___ 
 / _` | | |/ / / __|
| (_| | |   <| \__ \\
 \__, |_|_|\_\_|___/
 |___/              
    by kod34
'''

### MAIN

href_list = []
href_list2 = []
href_list3 = []
href_list4 = []
href_list5 = []
href_full_list = []

try:
    if __name__ == '__main__':
        check()
        if lvl != 'basic' and lvl != 'light' and lvl != 'moderate' and lvl != 'deep':
            parser.error("A required argument is missing")
        else:
            print(banner)
            checklink(url)
            t1 = datetime.now()
            t1_str = t1.strftime("%H:%M:%S")
            print('\n[+] Time of Start: '+t1_str, end='\n')
            print('\n[+] Collecting pages...', end='\n')
        if lvl == 'basic':
            looplinks(url, href_list)
            href_full_list = href_list
        elif lvl == 'light':
            looplinks(url, href_list)
            href_full_list = href_list
            getlink2()
            href_full_list = np.concatenate((np.array(href_full_list), np.array(href_list2)))
        elif lvl == 'moderate':
            looplinks(url, href_list)
            href_full_list = href_list
            getlink2()
            href_full_list = np.concatenate((np.array(href_full_list), np.array(href_list2)))
            getlink3()
            href_full_list = np.concatenate((np.array(href_full_list), np.array(href_list3)))
        elif lvl == 'deep' :
            looplinks(url, href_list)
            href_full_list = href_list
            getlink2()
            href_full_list = np.concatenate((np.array(href_full_list), np.array(href_list2)))
            getlink3()
            href_full_list = np.concatenate((np.array(href_full_list), np.array(href_list3)))
            getlink4()
            href_full_list = np.concatenate((np.array(href_full_list, np.array(href_list4))))
            getlink5()
            href_full_list = np.concatenate((np.array(href_full_list, np.array(href_list5)))) 
        
    href_full_list = np.unique(href_full_list)    
        
    print('\n[+] Making directories in <'+str(out)+'>...')
    time.sleep(1)
    sys.stdout.flush()
    downfol()

    print('\n[+] Downloading files...', end='')
    time.sleep(1)
    sys.stdout.flush()
    downfile()
    print('\n[+] Done', end='\n')
    t2 = datetime.now()
    t2_str = t2.strftime("%H:%M:%S")
    print('\n[+] Time of End: '+t2_str, end='\n')
    print('\n[*] Time taken: '+str(t2-t1), end='\n')

except KeyboardInterrupt:
    sys.exit('\n[!] User Interrupt')
