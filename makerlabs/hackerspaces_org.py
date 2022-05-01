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
    # Get first 500 labs
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
    # Get next labs
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


def get_single_lab(lab_slug, open_cage_api_key):
    """Gets data from a single lab from hackerspaces.org."""

    # API connection setup
    request_session = requests.Session()

    # Get the first page of data
    params = {
        "action": "parse",
        "page": lab_slug,
        "prop": "text",
        "formatversion": "2",
        "format": "json"
    }
    wiki_response = request_session.get(url=API_endpoint, params=params).json()
    content = BeautifulSoup(wiki_response['parse']['text'], 'html.parser')

    # Transform the data into a Lab object
    current_lab = Hackerspace()

    # Parse the Mediawiki code
    current_lab.name = wiki_response["parse"]["title"]
    current_lab.id = wiki_response["parse"]["pageid"]
    current_lab.slug = lab_slug
    # Coordinates from the map marker
    for div in content.find_all("div", {"class": "mapdata"}):
        mapjavascript = json.loads(div.text)["locations"]
        current_lab.latitude = mapjavascript[0]['lat']
        current_lab.longitude = mapjavascript[0]['lon']

    # Parse the side table
    # th and td<b> are mixed...
    for table in content.find_all('table'):
        # th
        for th in table.find_all('th'):
            #if th.text.strip() == "Status":
            #    current_lab.membercount = th.find_next('td').text.strip()
            if th.text.strip() == "Country":
                current_lab.country = th.find_next('td').text.strip()
            if th.text.strip() == "State or District":
                current_lab.state = th.find_next('td').text.strip()
            if th.text.strip() == "City":
                current_lab.city = th.find_next('td').text.strip()
            if th.text.strip() == "Date of founding":
                current_lab.created_at = th.find_next('td').text.strip()
            if th.text.strip() == "Website":
                current_lab.url = th.find_next('td').text.strip()
            if th.text.strip() == "Facebook":
                current_lab.membercount = th.find_next('td').text.strip()
            if th.text.strip() == "Snail mail":
                current_lab.membercount = th.find_next('td').text.strip()
            if th.text.strip() == "Number of members":
                current_lab.membercount = th.find_next('td').text.strip()
            if th.text.strip() == "Membership fee":
                current_lab.membercount = th.find_next('td').text.strip()
        # td
        for td in table.find_all('td'):
            if td.text.strip() in keywords:
                print("B",td,'---', td.find_next('td').text.strip())
            if td.text.strip() == "Status":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "Country":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "State or District":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "City":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "Date of founding":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "Website":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "Facebook":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "Snail mail":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "Number of members":
                current_lab.membercount = td.find_next('td').text.strip()
            if td.text.strip() == "Membership fee":
                current_lab.membercount = td.find_next('td').text.strip()

    # TODO
    # Find Facebook and Twitter links, add also the other ones
    current_lab.links = {"facebook": "", "twitter": ""}
    for link in i["links"]:
        if "facebook" in link["url"]:
            current_lab.links["facebook"] = link["url"]
        elif "twitter" in link["url"]:
            current_lab.links["twitter"] = link["url"]
        else:
            current_lab.links[link["id"]] = link["url"]

    # TODO
        if j_name == "coordinate":
            # Get the full address with the coordinates
            address = get_location(query=j_value, format="reverse", api_key=open_cage_api_key)
            current_lab.city = address["city"]
            current_lab.county = address["county"]
            current_lab.state = address["state"]
            current_lab.postal_code = address["postal_code"]
            current_lab.address_1 = address["address_1"]
            current_lab.country = address["country"]
            current_lab.country_code = address["country_code"]
            current_lab.continent = address["continent"]
            current_lab.latitude = address["latitude"]
            current_lab.longitude = address["longitude"]


    return current_lab


def get_labs(format):
    """Gets data from all labs from hackerspaces.org."""

    labs = []

    # API connection setup
    request_session = requests.Session()

    # Get the first page of data
    params = {
        "action": "query",
        "cmtitle": "Category:Hackerspace",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json"
    }
    wiki_response = request_session.get(url=API_endpoint, params=params).json()

    urls = []
    for i in wiki_response["query"]["categorymembers"]:
        urls.append(i["title"].replace(" ", "_"))

    # Load all the Labs in the first page
    for i in urls:
        current_lab = get_single_lab(i, open_cage_api_key)
        labs.append(current_lab)

    # Load all the Labs from the other pages
    while "continue" in wiki_response:
        params = {
            "action": "query",
            "cmtitle": "Category:Hackerspace",
            "cmlimit": "500",
            "cmcontinue": wiki_response['continue']['cmcontinue'],
            "list": "categorymembers",
            "format": "json"
        }
        wiki_response = request_session.get(url=API_endpoint, params=params).json()

        urls = []
        for i in wiki_response["query"]["categorymembers"]:
            urls.append(i["title"].replace(" ", "_"))

        # Load all the Labs
        for i in urls:
            current_lab = get_single_lab(i)
            labs.append(current_lab)

    # Transform the list into a dictionary
    labs_dict = {}
    for j, k in enumerate(labs):
        labs_dict[j] = k.__dict__

    # Return formatted data
    data = format_labs_data(format=format, labs=labs)

    return data


def labs_count():
    """Gets the number of current Hackerspaces registered on hackerspaces.org."""

    labs = get_labs()

    return len(labs)


if __name__ == "__main__":
    #pass
    a = data_from_hackerspaces_org()
    print(a)
