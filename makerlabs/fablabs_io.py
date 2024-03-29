# -*- encoding: utf-8 -*-
#
# Access data from fablabs.io
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
import pycountry
from time import sleep
import pandas as pd


# Endpoints
API_endpoint = "https://api.fablabs.io/0/labs.json"


class FabLab(Lab):
    """Represents a Fab Lab as it is described on fablabs.io."""

    def __init__(self):
        self.source = "fablabs.io"
        self.lab_type = "Fab Lab"


def data_from_fablabs_io(API_endpoint):
    """Gets data from fablabs.io."""

    data = requests.get(API_endpoint).json()

    return data


def get_labs(format, open_cage_api_key):
    """Gets Fab Lab data from fablabs.io."""

    fablabs_json = data_from_fablabs_io(API_endpoint)
    labs = {}

    # Load all the FabLabs
    for i in fablabs_json:
        current_lab = FabLab()
        current_lab.name = i["name"]
        current_lab.address_1 = i["address_1"]
        current_lab.address_2 = i["address_2"]
        current_lab.address_notes = i["address_notes"]
        current_lab.avatar = i["avatar_url"]
        current_lab.blurb = i["blurb"]
        current_lab.capabilities = i["capabilities"]
        if i["city"].isupper():
            i["city"] = i["city"].title()
        current_lab.city = i["city"]
        current_lab.country_code = i["country_code"]
        current_lab.county = i["county"]
        current_lab.description = i["description"]
        current_lab.email = i["email"]
        current_lab.id = i["id"]
        current_lab.phone = i["phone"]
        current_lab.postal_code = i["postal_code"]
        current_lab.slug = i["slug"]

        # Check coordinates
        if i["longitude"] is not None:
            current_lab.longitude = i["longitude"]
        else:
            current_lab.longitude = 0.0
        if i["latitude"] is not None:
            current_lab.latitude = i["latitude"]
        else:
            current_lab.latitude = 0.0

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
        except:
            pass

        # Find Facebook and Twitter links, add also the other ones
        current_lab.links = {"facebook": "", "twitter": ""}
        for link in i["links"]:
            if "facebook" in link["url"]:
                current_lab.links["facebook"] = link["url"]
            elif "twitter" in link["url"]:
                current_lab.links["twitter"] = link["url"]
            else:
                current_lab.links[link["id"]] = link["url"]
                current_lab.url = link["url"]

        # Add the lab to the list
        labs[i["slug"]] = current_lab

    # Return formatted data
    data = format_labs_data(format=format, labs=labs)

    return data


def labs_count():
    """Gets the number of current Fab Labs registered on fablabs.io."""

    fablabs = data_from_fablabs_io()

    return len(fablabs)


if __name__ == "__main__":
    pass
