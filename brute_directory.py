import requests
import argparse
import os
from time import sleep

# Brute Force in web site for hidden/unknow directories 

parser = argparse.ArgumentParser(description='Brute Force in directories.')

parser.add_argument('-t', '--target', help='Target of brute force.')
parser.add_argument('-w', '--wordlist',  help='Wordlist for words to brute.' )
parser.add_argument('-ua', '--useragent',action='append', help='User agent for requests, personalize to maybe bypass defences.')

args = parser.parse_args()


target = args.target
user_agent = args.useragent
wordlists = args.wordlist

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

def executing_brute_force():

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

executing_brute_force()
