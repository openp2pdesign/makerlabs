# -*- encoding: utf-8 -*-
#
# Access data from hackaday.io
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


import requests
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim


# Geocoding variable
geolocator = Nominatim()

# API key
# Register your app for the API key here:
# https://dev.hackaday.io/applications
API_key = "..."

# Endpoints
hackaday_io_labs_api_url = "https://api.hackaday.io/v1/pages/hackerspaces?api_key=" + API_key


class Hackerspace(object):
    """Represents a Hackerspace as it is described on hackaday.io."""

    def __init__(self):
        self.address_1 = ""
        self.address_2 = ""
        self.address_notes = ""
        self.avatar = ""
        self.blurb = ""
        self.capabilities = ""
        self.city = ""
        self.country_code = ""
        self.county = ""
        self.description = ""
        self.email = ""
        self.header_image_src = ""
        self.id = ""
        self.kind_name = ""
        self.latitude = ""
        self.longitude = ""
        self.links = ""
        self.name = ""
        self.parent_id = ""
        self.phone = ""
        self.postal_code = ""
        self.slug = ""
        self.url = ""
        self.lab_type = "Fab Lab"


def data_from_hackaday_io(endpoint):
    """Gets data from hackaday.io."""

    data = requests.get(endpoint).json()

    return data


def get_labs(format):
    """Gets Hackerspaces data from hackaday.io."""

    hackerspaces_json = data_from_hackaday_io(hackaday_io_labs_api_url)
    hackerspaces = {}

    # Load all the Hackerspaces
    for i in fablabs_json["labs"]:
        current_lab = FabLab()
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
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = fablabs
    # Default: return an oject
    else:
        output = fablabs

    return output


def labs_count():
    """Gets the number of current Hackerspaces listed on hackaday.io."""

    hackerspaces = data_from_hackaday_io(hackaday_io_labs_api_url)

    return len(hackerspaces["labs"])


if __name__ == "__main__":
    pass
