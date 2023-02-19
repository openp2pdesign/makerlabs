# -*- encoding: utf-8 -*-
#
# Access data from makery.info
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


# Endpoints
# INFO: https://www.makery.info/api/
API_endpoint = "https://www.makery.info/api/labs/"


class MakeryLab(Lab):
    """Represents a Lab as it is described on makery.info."""

    def __init__(self):
        self.source = "makery.info"
        self.lab_type = "Lab on makery.info"


def data_from_makery_info():
    """Gets data from makery.info."""

    data = requests.get(API_endpoint).json()

    return data


def get_labs(format, open_cage_api_key):
    """Gets Lab data from makery.info."""

    labs_json = data_from_makery_info()
    labs = {}

    # Load all the FabLabs
    for i in labs_json["features"]:
        ip = i["properties"]
        current_lab = MakeryLab()
        current_lab.name = ip["name"]
        current_lab.slug = ip["url_makery"]
        current_lab.url = ip["url_makery"]
        current_lab.capabilities = ip["equipments"]
        current_lab.description = ip["activities"]
        current_lab.blurb = ip["type_lab"]
        current_lab.lab_type = "Lab on makery.info - " + ip["type_lab"]
        current_lab.links = {"facebook": "", "twitter": "", "website": ""}
        current_lab.links["facebook"] = ip["facebook"]
        current_lab.links["twitter"] = ip["twitter"]
        current_lab.links["website"] = ip["website"]
        current_lab.latitude = i["geometry"]["coordinates"][1]
        current_lab.longitude = i["geometry"]["coordinates"][0]

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

        # Add the lab
        labs[ip["name"]] = current_lab

    # Return formatted data
    output = format_labs_data(format=format, labs=labs)

    return output


def labs_count():
    """Gets the number of current Labs listed on makery.info."""

    labs = data_from_makery_info(API_endpoint)

    return len(labs["labs"])


if __name__ == "__main__":
    pass
