#!/usr/bin/env python3

import requests
from random import choice
import argparse
import re

#Setup Argparser

parser = argparse.ArgumentParser( description = "Returns a random link to an image from a given subreddit")
parser.add_argument("subreddit", help="Subreddit to grab image from")
parser.add_argument("--type", dest='filetype', help="Type of file to return" )

ARGS = parser.parse_args()
SUBREDDIT = ARGS.subreddit
FILETYPE  = ARGS.filetype

#If you want, you can change your user agent
#This is useful if reddit bans you :)
#BTW: reddit blocks the default user agent, so this 
#must be set or reddit will return 
#Error 429 - Too Many Reqeusts
USER_AGENT = "Alienshuf 1.0"

def getPostUrls(count, subreddit, filetype=None):
    # Returns count urls from subreddit as a list
    if( not subreddit.isalnum() ):
        return None
    
    raw_response = requests.get("https://www.reddit.com/r/" + subreddit + "/hot/.json",
            params={"limit": str(count)},
            headers={"User-agent": USER_AGENT}
    )
    
    json_response= raw_response.json()

    url_list = [post['data']['url'] for post in json_response['data']['children'] if not post['data']['is_self'] ]
    print("got %d urls" % len(url_list))
    if filetype is not None:
        regex = re.compile(r"%s$" % filetype)
        return list(filter(regex.search, url_list))
    else:
        return url_list


def printRandomUrl(count, subreddit, filetype=None):
    url_list = getPostUrls(count, subreddit, filetype)

    if len(url_list) > 0:
        print(choice(url_list))
    else:
        print("")

printRandomUrl(100, SUBREDDIT, FILETYPE)

