# -*- encoding: utf-8 -*-
#
# Access data from hackerspaces.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from . classes import Lab
from . utils import get_location
from . utils import format_labs_data

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


def get_labs(format, open_cage_api_key):
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
        current_lab.name = request_data['parse']['title']
        current_lab.links = {"facebook": "", "twitter": ""}
        content = BeautifulSoup(request_data['parse']['text'], 'html.parser')
        # Get coordinates from the embedded map
        # If the lab has no locations, we don't consider it
        map_div = content.find("div", {"class": "mapdata"})
        if map_div:
            # Get coordinates
            for map_div in content.find_all("div", {"class": "mapdata"}):
                map_javascript = json.loads(map_div.text)["locations"]
                if len(map_javascript) > 0:
                    map_content = BeautifulSoup(map_javascript[0]["text"], 'html.parser')
                    for p in map_content.find_all("p"):
                        if ", " in p.text.strip() or "," in p.text.strip():
                            if ", " in p.text.strip():
                                latitude = p.text.strip().split(', ')[0]
                                longitude = p.text.strip().split(', ')[1]
                            elif "," in p.text.strip():
                                latitude = p.text.strip().split(',')[0]
                                longitude = p.text.strip().split(',')[1]
                            latitude = latitude.replace("°","")
                            latitude = latitude.replace(" ","")
                            latitude = latitude.replace("N","")
                            latitude = latitude.replace("S","")
                            try:
                                latitude = float(latitude)
                            except:
                                pass
                            current_lab.latitude = latitude
                            longitude = longitude.replace("°","")
                            longitude = longitude.replace(" ","")
                            longitude = longitude.replace("E","")
                            longitude = longitude.replace("W","")
                            try:
                                longitude = float(longitude)
                            except:
                                pass
                            current_lab.longitude = longitude
                            # Get address from coordinates
                            # Try, in case there are issues with some coordinates formatting
                            try:
                                location = get_location(query=(
                                    current_lab.latitude,
                                    current_lab.longitude),
                                    format="reverse",
                                    api_key=open_cage_api_key)

                                current_lab.address_1 = location["address_1"]
                                current_lab.city = location["city"]
                                current_lab.country_code = location["country_code"]
                                current_lab.country = location["country"]
                                current_lab.county = location["county"]
                                current_lab.postal_code = location["postal_code"]
                                current_lab.continent = location["continent"]
                                current_lab.state = location["state"]

                                # Get the content
                                keywords = ["Status", "Date of founding", "Last Updated", "Website", "Phone", "EventBrite", "Facebook", "Snail mail", "Number of members", "Membership fee", "Size of rooms", "Members", "Location"]
                                results = {}
                                # th and td are mixed...
                                # so this should be run twice, for both
                                table_elements = ["th", "td"]
                                for table_element_tag in table_elements:
                                    for table in content.find_all('table'):
                                        # th
                                        for table_element in table.find_all(table_element_tag):
                                            if table_element.text.strip() in keywords:
                                              if table_element.text.strip() == "Status":
                                                  current_lab.status = table_element.find_next('td').text.strip()
                                              if table_element.text.strip() == "Date of founding":
                                                  current_lab.created_at = table_element.find_next('td').text.strip()
                                              if table_element.text.strip() == "Website":
                                                  current_lab.url = table_element.find_next('td').text.strip()
                                              if table_element.text.strip() == "Facebook":
                                                  current_lab.links["facebook"] = table_element.find_next('td').text.strip()
                                              if table_element.text.strip() == "Twitter":
                                                  current_lab.links["twitter"] = table_element.find_next('td').text.strip()
                                              if table_element.text.strip() == "Snail mail":
                                                  current_lab.email = table_element.find_next('td').text.strip()
                                              if table_element.text.strip() == "Number of members":
                                                  current_lab.membercount = table_element.find_next('td').text.strip()
                                              #if table_element.text.strip() == "Membership fee":
                                                  #results["Date of founding"] = table_element.find_next('td').text.strip()
                            except:
                                pass
                            # Add the lab to the list
                            labs[current_lab.name] = current_lab

    # Return formatted data
    data = format_labs_data(format=format, labs=labs)

    return data


def labs_count():
    """Gets the number of current Hackerspaces registered on hackerspaces.org."""

    labs = data_from_hackerspaces_org()

    return len(labs)


if __name__ == "__main__":
    pass
