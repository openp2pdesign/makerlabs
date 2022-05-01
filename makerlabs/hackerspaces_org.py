# -*- encoding: utf-8 -*-
#
# Access data from hackerspaces.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab
from utils import get_location
from utils import format_labs_data

import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Endpoints
API_endpoint = "https://wiki.hackerspaces.org/w/api.php"


class Hackerspace(Lab):

    """Represents a Hackerspace as it is described on hackerspaces.org."""

    def __init__(self):
        self.source = "hackerspaces.org"
        self.lab_type = "Hackerspace"


def data_from_hackerspaces_org():
    """Gets data from hackerspaces.org."""

    hackerspaces = []
    req = requests.Session()
    # Get first 500 labs names / page titles
    params = {
        "action": "query",
        "cmtitle": "Category:Hackerspace",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json"
    }
    request_data = req.get(url=API_endpoint, params=params).json()
    for page in request_data['query']['categorymembers']:
        hackerspaces.append(page['title'])
    # Get all next labs names / page titles
    while "continue" in request_data:
        params = {
            "action": "query",
            "cmtitle": "Category:Hackerspace",
            "cmlimit": "500",
            "cmcontinue": request_data['continue']['cmcontinue'],
            "list": "categorymembers",
            "format": "json"
        }
        req = requests.Session()
        request_data = req.get(url=API_endpoint, params=params).json()
        for page in request_data['query']['categorymembers']:
            hackerspaces.append(page['title'])

    return hackerspaces


def get_labs(format):
    """Gets data from all hackerspaces from hackerspaces.org."""

    labs_titles = data_from_hackerspaces_org()
    labs = {}

    # Load all the Hackerspaces
    for i in labs_titles:
        current_lab = Hackerspace()
        req = requests.Session()
        params = {
            "action": "parse",
            "page": i,
            "prop": "text",
            "formatversion": "2",
            "format": "json"
        }
        request_data = req.get(url=API_endpoint, params=params).json()
        print(request_data)
        exit()
        for page in request_data['query']['categorymembers']:
            hackerspaces.append(page['title'])

    # Return formatted data
    data = format_labs_data(format=format, labs=labs)

    return data


def labs_count():
    """Gets the number of current Hackerspaces registered on hackerspaces.org."""

    labs = data_from_hackerspaces_org()

    return len(labs)


if __name__ == "__main__":
    #pass
    a = get_labs(format="dict")
    print(a)
