#!/usr/bin/env python3

import requests
from random import sample
import argparse
import re

#Setup Argparser

parser = argparse.ArgumentParser( description = "Returns a random link to an image from a given subreddit")
parser.add_argument("subreddit", help="Subreddit to grab image from")
parser.add_argument("--type", "-t", dest='filetype', help="Type of file to return" )
parser.add_argument("--count","-c", dest='count', default=1, help="Number of files to return (default 1)", type=int)
parser.add_argument("--limit", "-l", dest='limit', default=25, help="Number of links to request from reddit (must be >= count), default 25", type=int)
parser.add_argument("--sort", "-s", dest='sort', default="hot", help="How to sort subreddit when shuffling post")

VALID_SORTS = [ "hot", "top", "new" ]
VALID_FILETYPES = [None, "jpg", "jpeg", "gif", "webm", "png"]

#If you want, you can change your user agent
#This is useful if reddit bans you :)
#BTW: reddit blocks the default user agent, so this 
#must be set or reddit will return 
#Error 429 - Too Many Reqeusts
USER_AGENT = "Alienshuf 1.0"

ERROR_BAD_ARGUMENT = "Error - one or more arguments are inconsistent or invalid"

def validInput(args):
    # Checks if input is valid, and returns True if so
    # Returns false otherwise.
    validLimit = args.limit >= args.count
    validSort  = args.sort in VALID_SORTS
    validFiletype = args.filetype in VALID_FILETYPES
    return validLimit and validSort and validFiletype

def fixFiletype(filetype):
    i = 0
    while( i < len(filetype) and not filetype[i].isalnum() ):
        i+=1
    stringBegin = i
    while( i < len(filetype) and filetype[i].isalnum() ):
        i+=1
    stringEnd = i
    return filetype[stringBegin:stringEnd]

def getPostUrls(subreddit,limit,sort,filetype=None):
    # Returns count urls from subreddit as a list
    if( not subreddit.isalnum() ):
        return None
    
    raw_response = requests.get(
            "https://www.reddit.com/r/" + subreddit + "/hot/.json",
            params={"limit": str(limit)},
            headers={"User-agent": USER_AGENT}
    )
    
    json_response= raw_response.json()

    url_list = [post['data']['url'] for post in json_response['data']['children'] if not post['data']['is_self'] ]
    if filetype is not None:   
        regex = re.compile(r"\.%s$" % filetype)
        return list(filter(regex.search, url_list))
    else:
        return url_list

def printRandomUrls(subreddit, count, limit, sort, filetype):
    url_list = getPostUrls(subreddit, limit, sort, filetype)

    if len(url_list) > 0:
        for s in sample(url_list, count):
            print(s)
    else:
        print("")

ARGS = parser.parse_args()
ARGS.filetype = fixFiletype(ARGS.filetype) # fix the filetype

def main():
    if(validInput(ARGS)):
        printRandomUrls(ARGS.subreddit, ARGS.count, ARGS.limit, ARGS.sort, ARGS.filetype)
    else:
        print(ERROR_BAD_ARGUMENT)

main()
