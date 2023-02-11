import requests
import argparse
import os
from time import sleep
import threading

# Brute Force in web site for hidden/unknow directories 

parser = argparse.ArgumentParser(description='Brute Force in directories.')

parser.add_argument('-t', '--target', help='Target of brute force.')
parser.add_argument('-w', '--wordlist',  help='Wordlist for words to brute.' )
parser.add_argument('-ua', '--useragent',action='append', help='User agent for requests, personalize to maybe bypass defences.')
parser.add_argument('-x', '--extension', action='append', help='Set extensions for looking for, example: .php,.txt,.html. USE , TO SEP EACH EXTENSION.')

args = parser.parse_args()


target = args.target
user_agent = args.useragent
wordlists = args.wordlist
extensions = args.extension


extensionsss = []
stauts_code_meaning = {200: "OK", 301: "Moved", 403: "Forbidden"}
status_code_permited = [200,301,403]



def opening_wordlist():

    """Try to open the file, if the files opens continues, else, stop"""

    try:
        words = open(wordlists)
        return words

    except:
        print("\n >>> path incorrect or file doest exist. <<<")
        return 


def executing_brute_force_NOEXTENSIONs():

    """Function for call opening_wordlist function (get the words from file), first check if the host is on, if YES start testing the directories"""

    words = opening_wordlist()

    try:
            validating_host = requests.request('GET', target)
            if validating_host.status_code == 200:
                print("\nHosts seens online starting looking for directories....\n")
                print("Directories          STATUS CODE              STATUS MEANING")
                for X in words:
                    url_final = target + "/" + X.strip()
                    brute_force = requests.get(url=url_final)
                    status = brute_force.status_code
                    sleep(0.5)
                    if status in status_code_permited:
                        dic = X.replace("\n", "")
                        print(f"{dic}                    {status}                  {stauts_code_meaning[status]}")     
            else:
                print("Host seens offline or forbidden access")
    except:
            print("Invalid Host.")
    

def executing_brute_force_extensions(extension):
            words = opening_wordlist()
            validating_host = requests.request('GET', target)
            if validating_host.status_code == 200:
                for X in words:
                    cleaning = X.strip()
                    url_final = target + "/" + cleaning + extension
                    brute_force = requests.get(url=url_final)
                    status = brute_force.status_code
                    sleep(0.5)
                    if status in status_code_permited:
                        dic = X.replace("\n", "")
                        print(f"{dic}{extension}                    {status}                  {stauts_code_meaning[status]}")     
            else:
                print("Host seens offline or forbidden access")



print("-------- CONFIGURATION --------")

try:
    print(f"USER_AGENT: {user_agent[0]}")
    print(f"HOST >> {target}")
    print(f"WORDLIST >> {wordlists}")

except:

    print(f"HOST >> {target}")
    print(f"WORDLIST >> {wordlists}")
    print(f"USER_AGENT: Abyssarium 1.1")

print("-----------------------------")

threads = []


if args.extension != None:
    for extensions in args.extension:
        extensionsss.append(extensions)
        for X in extensionsss:
            for S in X.split(','):
                t = threading.Thread(target=executing_brute_force_extensions, args=(S,))
                threads.append(t)
                t.start()
    print("\nHosts seens online starting looking for directories....\n")
    print("Directories          STATUS CODE              STATUS MEANING")

    for t in threads:
        t.join()

else:
    executing_brute_force_NOEXTENSIONs()
