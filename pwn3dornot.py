#!/usr/bin/env python3
#import modules
import logging
import os
import sys
from time import sleep, time
from typing import List
from urllib.parse import quote
import re
import requests
from dotenv import load_dotenv
import operator



logging.basicConfig(format='%(message)s')


# load secrets
load_dotenv()
#Api key from HIBP
apikey=os.getenv("apikey")
#variable for valid email regex
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#logging 
log = logging.getLogger()


def get_filename(args: str) -> str:
    """Function to check the given file in command line.
       Checking if the given file is not empty and if it
       exists. exit script when condition not met."""
    if len(args) < 2:
        raise ValueError("input missing ")

    file = args[1]

    if not os.path.isfile(file):
        raise FileNotFoundError("No such file in directory")
   

    if os.path.getsize(file) == 0:
        raise ValueError("File is empty")

    return file




def read_emails(filepath: str) -> List[str]:
    """extract valid regex emails from a file"""
    try:
        inputfile = open(filepath, "r")

        emails=[]

        for line in inputfile:
            email = line.lower().strip()
            
            if not email:
                continue
            if re.fullmatch(regex, email):
                emails.append(email)
            else:
                logging.warning("Invald email: %s", email)
                continue

        return emails
   
    finally:
        if inputfile is not None:
            inputfile.close()



def build_url(emails: str)-> str:
    """Build basic URL for each extracted email from a file ."""
    return "https://haveibeenpwned.com/api/v3/breachedaccount/"+ quote(emails) + "?truncateResponse=false"



def hibp_response(url: str) -> str:
    """Handle http GET response "HIBP"."""
    headers = {"hibp-api-key": apikey}
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return ''    
    
    if response.status_code != 200:
        raise ValueError("status code = " + str(response.status_code) + " --> " + str(response.content))

    if len(response.content) == 0:
        raise ValueError("response empty")
    
    sleep(5)
    jsondata = response.json()
    return jsondata


if __name__ == '__main__':
# MAIN
    try:
    #Get emails from file
        emaillist = get_filename(sys.argv)
        emails = read_emails(emaillist)


        #check emails and preform get response
        for email in emails:
            url = build_url(email)
            data = hibp_response(url)
            
            print()
            print('-->', email)
            
            #Print out Pwned data
            for breach in ( sorted(data, key=operator.itemgetter("BreachDate"))):
                Title = breach["Title"]
                Domain = breach["Domain"]
                Time = breach["BreachDate"]
                print(Time,Title,Domain)
                

    except KeyboardInterrupt:
        pass
    except ValueError as e:
        logging.critical(e)