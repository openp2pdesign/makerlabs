# -*- encoding: utf-8 -*-
#
# Access data from hackaday.io
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab
from utils import format_labs_data

import json
import requests
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim
import pandas as pd

# Geocoding variable
geolocator = Nominatim()


# Endpoints
# The documented endpoint does not have coordinates,
# the undocumented one has them, so for the moment we use the latter.
# The undocumented endpoint does not need API keys or OAuth.
# hackaday.io API documentation:
# https://dev.hackaday.io/doc/api/get-pages
# Register your app for the API key here:
# https://dev.hackaday.io/applications
client_id = "..."
client_secret = "..."
API_key = "..."
# Documented endpoint for the list of hackerspaces
hackaday_io_labs_api_url = "https://api.hackaday.io/v1/pages/hackerspaces?api_key=" + API_key
# Undocumented endpoint for the map of hackerspaces
hackaday_io_labs_map_url = "http://hackaday.io/api/location/hackerspaces"


class Hackerspace(Lab):
    """Represents a Hackerspace as it is described on hackaday.io."""

    def __init__(self):
        self.source = "hackaday.io"
        self.lab_type = "Hackerspace"


def data_from_hackaday_io(endpoint):
    """Gets data from hackaday.io."""

    data = requests.get(endpoint).json()

    return data


def get_labs(format):
    """Gets Hackerspaces data from hackaday.io."""

    hackerspaces_json = data_from_hackaday_io(hackaday_io_labs_map_url)
    hackerspaces = {}

    # Load all the Hackerspaces
    for i in hackerspaces_json:
        current_lab = Hackerspace()
        current_lab.id = i["id"]
        current_lab.url = "https://hackaday.io/hackerspace/" + current_lab.id
        current_lab.name = i["name"]
        if len(i["description"]) != 0:
            current_lab.description = i["description"]
        elif len(i["summary"]) != 0:
            current_lab.description = i["summary"]
        current_lab.created_at = i["moments"]["exact"]

        # Check if there are coordinates
        if i["latlon"] is not None:
            latlon = json.loads(i["latlon"])
            current_lab.latitude = latlon["lat"]
            current_lab.longitude = latlon["lng"]
            # Get country, county and city from them
            country = geolocator.reverse(
                [latlon["lat"], latlon["lng"]])
            current_lab.country = country.raw[
                "address"]["country"]
            current_lab.address = country.raw["display_name"]
            current_lab.address_1 = country.raw["display_name"]
            current_lab.country_code = country.raw[
                "address"]["country_code"]
            current_lab.county = country.raw[
                "address"]["state_district"]
            current_lab.city = country.raw[
                "address"]["city"]
            current_lab.postal_code = country.raw[
                "address"]["postcode"]
        else:
            # For labs without a location or coordinates
            # add 0,0 as coordinates
            current_lab.latitude = 0.0
            current_lab.longitude = 0.0

        # Add the lab
        hackerspaces[i["name"]] = current_lab

    # Return formatted data
    data = format_labs_data(format=format, labs=hackerspaces)

    return data


def labs_count():
    """Gets the number of current Hackerspaces listed on hackaday.io."""

    hackerspaces = data_from_hackaday_io(hackaday_io_labs_api_url)

    return len(hackerspaces["labs"])


if __name__ == "__main__":
    pass
