#!/usr/bin/env python3

import requests
from random import sample
import argparse
import re
from copy import deepcopy

#Setup Argparser

parser = argparse.ArgumentParser( description = "Returns a random link to an image from a given subreddit")
parser.add_argument("subreddit", help="Subreddit to grab image from")
parser.add_argument("--type", "-t", dest='filetype', help="Type of file to return" )
parser.add_argument("--count","-c", dest='count', default=1, help="Number of files to return (default 1)", type=int)
parser.add_argument("--limit", "-l", dest='limit', default=25, help="Number of links to request from reddit (must be >= count), default 25", type=int)
parser.add_argument("--sort", "-s", dest='sort', default="hot", help="How to sort subreddit when shuffling post")
parser.add_argument("--debug", "-d", dest='debug', action='store_true', help="Enables debug mode and prints all debug messages")


VALID_SORTS = [ "hot", "top", "new" ]
DEFAULT_OPTIONS = { "top": { "t": "all" }, "hot": {}, "new": {} }
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
    if filetype is not None:
        i = 0
        while( i < len(filetype) and not filetype[i].isalnum() ):
            i+=1
        stringBegin = i
        while( i < len(filetype) and filetype[i].isalnum() ):
            i+=1
        stringEnd = i
        return filetype[stringBegin:stringEnd]
    else:
        return None

def getParamsForSort( sort, limit=None, options=None):   
    
    if limit:
        params = { "limit": str(limit) }
    else:
        params = {}

    if options:
        params.update(options)
    else:
        try:
            params.update(DEFAULT_OPTIONS[sort])
        except KeyError:
            raise ValueError("Bad sort '%s'  provided to getParamsForSort" % sort)

    return params
    
def getPostUrls(subreddit, limit, sort, filetype=None, options=None, debug=None):
    # Returns count urls from subreddit as a list
    if( not subreddit.isalnum() ):
        return None
    
    params = getParamsForSort(sort, limit, options)

    raw_response = requests.get(
            "https://www.reddit.com/r/" + subreddit + "/" + sort + "/.json",
            params=params,
            headers={"User-agent": USER_AGENT}
    )
    if debug:
        print(raw_response.url)
    json_response= raw_response.json()

    url_list = [post['data']['url'] for post in json_response['data']['children'] if not post['data']['is_self'] ]
    if debug:
        print("Got %d urls" % len(url_list))
    if filetype is not None:   
        regex = re.compile(r"\.%s$" % filetype)
        return list(filter(regex.search, url_list))
    else:
        return url_list

def printRandomUrls(subreddit, count, limit, sort, filetype=None, options=None, debug=False):
    url_list = getPostUrls(subreddit, limit, sort, filetype=filetype, options=options, debug=debug)

    if len(url_list) > 0:
        for s in sample(url_list, count):
            print(s)
    else:
        print("")

ARGS = parser.parse_args()
ARGS.filetype = fixFiletype(ARGS.filetype) # fix the filetype

def main():
    if(validInput(ARGS)):
        if ARGS.debug:
            print(ARGS)
        printRandomUrls(ARGS.subreddit, ARGS.count, ARGS.limit, ARGS.sort, filetype=ARGS.filetype, options=None, debug=ARGS.debug)
    else:
        print(ERROR_BAD_ARGUMENT)

main()
