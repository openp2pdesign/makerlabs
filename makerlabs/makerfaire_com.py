# -*- encoding: utf-8 -*-
#
# Access data from makerfaire.com
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from . classes import Faire
from . utils import get_location
from . utils import format_labs_data

import json
from urllib.request import Request, urlopen
import pandas as pd


# Endpoints
API_endpoint = "https://makerfaire.com/query/?type=map"


class Makerfaire(Faire):
    """Represents a Maker Faire as it is described on makerfaire.com"""

    def __init__(self):
        self.source = "makerfaire.com"
        self.faire_type = "Maker Faire"


def data_from_makerfaire_com():
    """Gets data from makerfaire.com."""

    req = Request(API_endpoint, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = json.loads(webpage)
    data = data["Locations"]

    return data


def get_faires(format, open_cage_api_key):
    """Gets Maker Faire data from makerfaire.com."""

    makerfaires_json = data_from_makerfaire_com()
    makerfaires = {}

    # Load all the Makerspaces
    for i in makerfaires_json:
        current_lab = Makerfaire()
        current_lab.name = i["name"]
        current_lab.id = i["ID"]
        current_lab.url = i["faire_url"]
        current_lab.description = i["description"]
        current_lab.category = i["category"]
        current_lab.event_type = i["event_type"]
        current_lab.year = i["faire_year"]
        current_lab.dt = i["event_dt"]
        current_lab.event_start_dt = i["event_start_dt"]
        current_lab.event_end_dt = i["event_end_dt"]
        current_lab.cfm_start_dt = i["cfm_start_dt"]
        current_lab.cfm_end_dt = i["cfm_end_dt"]
        current_lab.free_event = i["free_event"]

        # Check coordinates
        if i["lng"] is not None:
            current_lab.longitude = i["lng"]
        else:
            current_lab.longitude = 0.0
        if i["lat"] is not None:
            current_lab.latitude = i["lat"]
        else:
            current_lab.latitude = 0.0

        # Get address from coordinates
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

        # Add the lab to the list
        makerfaires[i["name"]] = current_lab

    # Return formatted data
    data = format_labs_data(format=format, labs=makerfaires)

    return data


def faires_count():
    """Gets the number of current Maker Faires registered on makerfaire_com."""

    makerfaires = data_from_makerfaire_com()

    return len(makerfaires)


if __name__ == "__main__":
    pass
