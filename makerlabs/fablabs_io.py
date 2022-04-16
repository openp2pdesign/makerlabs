# -*- encoding: utf-8 -*-
#
# Access data from fablabs.io
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from .classes import Lab

import json
import requests
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim
import pycountry
from time import sleep
import pandas as pd


# Geocoding variable
geolocator = Nominatim()

# Endpoints
fablabs_io_labs_api_url_v0 = "https://api.fablabs.io/0/labs.json"


class FabLab(Lab):
    """Represents a Fab Lab as it is described on fablabs.io."""

    def __init__(self):
        self.source = "fablabs.io"
        self.lab_type = "Fab Lab"


def data_from_fablabs_io(endpoint):
    """Gets data from fablabs.io."""

    data = requests.get(endpoint).json()

    return data


def get_labs(format):
    """Gets Fab Lab data from fablabs.io."""

    fablabs_json = data_from_fablabs_io(fablabs_io_labs_api_url_v0)
    fablabs = {}

    # Load all the FabLabs
    for i in fablabs_json["labs"]:
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
        current_lab.url = i["url"]

        continent_code = pycountry.country_alpha2_to_continent_code(i["country_code"])
        current_lab.continent = pycountry.convert_continent_code_to_continent_name(continent_code)

        current_country = pycountry.countries.get(alpha_2=i["country_code"].upper())
        current_lab.country_code = current_country.alpha_3
        current_lab.country = current_country.name

        # Check coordinates
        if i["longitude"] is not None:
            current_lab.longitude = i["longitude"]
        else:
            current_lab.longitude = 0.0
        if i["latitude"] is not None:
            current_lab.latitude = i["latitude"]
        else:
            current_lab.latitude = 0.0

        # Find Facebook and Twitter links, add also the other ones
        current_lab.links = {"facebook": "", "twitter": ""}
        for link in i["links"]:
            if "facebook" in link["url"]:
                current_lab.links["facebook"] = link["url"]
            elif "twitter" in link["url"]:
                current_lab.links["twitter"] = link["url"]
            else:
                current_lab.links[link["id"]] = link["url"]

        # Add the lab to the list
        fablabs[i["slug"]] = current_lab

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in fablabs:
            output[j] = fablabs[j].__dict__
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in fablabs:
            single = fablabs[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return a Pandas DataFrame
    elif format.lower() == "pandas" or format.lower() == "dataframe":
        output = {}
        for j in fablabs:
            output[j] = fablabs[j].__dict__
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = fablabs
    # Default: return an oject
    else:
        output = fablabs
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)
    return output


def labs_count():
    """Gets the number of current Fab Labs registered on fablabs.io."""

    fablabs = data_from_fablabs_io(fablabs_io_labs_api_url_v0)

    return len(fablabs["labs"])


if __name__ == "__main__":
    print(get_labs(format="json"))
