# -*- encoding: utf-8 -*-
#
# Access data from makery.info
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab

import json
import requests
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim
import pandas as pd


# Geocoding variable
geolocator = Nominatim()

# Endpoints
makery_info_labs_api_url = "http://www.makery.info/api/labs/"


class MakeryLab(Lab):
    """Represents a Lab as it is described on makery.info."""

    def __init__(self):
        self.source = "makery.info"
        self.lab_type = "Lab on makery.info"


def data_from_makery_info(endpoint):
    """Gets data from makery.info."""

    data = requests.get(endpoint).json()

    return data


def get_labs(format):
    """Gets Lab data from makery.info."""

    labs_json = data_from_makery_info(makery_info_labs_api_url)
    labs = {}

    # Load all the FabLabs
    for i in labs_json["labs"]:
        current_lab = MakeryLab()
        current_lab.address_1 = i["address_1"]
        current_lab.address_2 = i["address_2"]
        current_lab.address_notes = i["address_notes"]
        current_lab.avatar = i["avatar"]
        current_lab.blurb = i["blurb"]
        current_lab.capabilities = i["capabilities"]
        current_lab.city = i["city"]
        current_lab.country_code = i["country_code"]
        current_lab.county = i["county"]
        current_lab.description = i["description"]
        current_lab.email = i["email"]
        current_lab.header_image_src = i["header_image_src"]
        current_lab.id = i["id"]
        current_lab.kind_name = i["kind_name"]
        # Some labs do not have coordinates
        if i["latitude"] is None or i["longitude"] is None:
            address = i["address_1"] + i["city"] + i["country_code"]
            try:
                location = geolocator.geocode(address)
                current_lab.latitude = location.latitude
                current_lab.longitude = location.longitude
            except:
                try:
                    location = geolocator.geocode(i["city"])
                    current_lab.latitude = location.latitude
                    current_lab.longitude = location.longitude
                except:
                    # For labs without a city, add 0,0 as coordinates
                    current_lab.latitude = 0.0
                    current_lab.longitude = 0.0
        else:
            current_lab.latitude = i["latitude"]
            current_lab.longitude = i["longitude"]
        current_lab.links = i["links"]
        current_lab.name = i["name"]
        current_lab.parent_id = i["parent_id"]
        current_lab.phone = i["phone"]
        current_lab.postal_code = i["postal_code"]
        current_lab.slug = i["slug"]
        current_lab.url = i["url"]
        # Add the lab
        labs[i["slug"]] = current_lab

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in labs:
            output[j] = labs[j].__dict__
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in labs:
            single = labs[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return a Pandas DataFrame
    elif format.lower() == "pandas" or format.lower() == "dataframe":
        output = {}
        for j in labs_list:
            output[j] = labs_list[j].__dict__
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = labs
    # Default: return an oject
    else:
        output = labs
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)
    return output


def labs_count():
    """Gets the number of current Labs listed on makery.info."""

    labs = data_from_makery_info(makery_info_labs_api_url)

    return len(labs["labs"])


if __name__ == "__main__":
    pass
