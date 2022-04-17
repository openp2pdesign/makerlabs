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

import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

hackerspaces_org_api_url = "https://wiki.hackerspaces.org/w/api.php"


class Hackerspace(Lab):

    """Represents a Hackerspace as it is described on hackerspaces.org."""

    def __init__(self):
        self.source = "hackerspaces.org"
        self.lab_type = "Hackerspace"


def get_single_lab(lab_slug):
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
    wiki_response = request_session.get(url=hackerspaces_org_api_url, params=params).json()
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

    wikicode = mwparserfromhell.parse(content)
    for k in wikicode.filter_templates():
        element_name = str(k.name)
        if "Hackerspace" in element_name:
            for j in k.params:
                # Remove new line in content
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
    wiki_response = request_session.get(url=hackerspaces_org_api_url, params=params).json()

    urls = []
    for i in wiki_response["query"]["categorymembers"]:
        urls.append(i["title"].replace(" ", "_"))

    # Load all the Labs in the first page
    for i in urls:
        current_lab = get_single_lab(i)
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
        wiki_response = request_session.get(url=hackerspaces_org_api_url, params=params).json()

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

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = labs_dict
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in labs_dict:
            single = labs_dict[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return a Pandas DataFrame
    elif format.lower() == "pandas" or format.lower() == "dataframe":
        output = labs_dict
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
        output = output.set_index(['name'])
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = labs
    # Default: return an object
    else:
        output = labs
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(labs_dict)
    return output


def labs_count():
    """Gets the number of current Hackerspaces registered on hackerspaces.org."""

    labs = get_labs()

    return len(labs)


if __name__ == "__main__":
    pass
