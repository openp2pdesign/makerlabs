# -*- encoding: utf-8 -*-
#
# Access data from makerspaces.make.co
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
from urllib.request import Request, urlopen
import pandas as pd


# Endpoints
API_endpoint = "https://makerspaces.make.co/wp-json/makemap/v1/mapdata/5"


class Makerspace(Lab):
    """Represents a Makerspace as it is described on makerspaces.make.co."""

    def __init__(self):
        self.source = "makerspaces.make.co"
        self.lab_type = "Makerspace"


def data_from_makerspaces_make_co():
    """Gets data from makerspaces.make.co."""

    req = Request(API_endpoint, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = json.loads(webpage)
    data = data["Locations"]

    return data


def get_labs(format, open_cage_api_key):
    """Gets Makerspace data from makerspaces.make.co."""

    makerspaces_json = data_from_makerspaces_make_co()
    makerspaces = {}

    # Load all the Makerspaces
    for i in makerspaces_json:
        current_lab = Makerspace()
        current_lab.name = i["mmap_eventname"]
        current_lab.url = i["mmap_url"]

        # Check coordinates
        if i["mmap_lng"] is not None:
            current_lab.longitude = i["mmap_lng"]
        else:
            current_lab.longitude = 0.0
        if i["mmap_lat"] is not None:
            current_lab.latitude = i["mmap_lat"]
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
        makerspaces[i["mmap_eventname"]] = current_lab

    # Return formatted data
    data = format_labs_data(format=format, labs=makerspaces)

    return data


def labs_count():
    """Gets the number of current Makerspaces registered on makerspaces.make.co."""

    makerspaces = data_from_makerspaces_make_co()

    return len(makerspaces)


if __name__ == "__main__":
    pass
