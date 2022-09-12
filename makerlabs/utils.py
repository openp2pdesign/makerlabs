# -*- encoding: utf-8 -*-
#
# Shared fuctions
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#

# Import necessary modules

from geopy.geocoders import OpenCage
from time import sleep
import pycountry
import json
import pandas as pd


def format_labs_data(format, labs):
    # Return a dictionary / json
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
        for j in labs:
            output[j] = labs[j].__dict__
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = labs
    # Default: return an object
    else:
        output = labs
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)

    return output


def get_location(query, format, api_key):
    """Get geographic data of a lab in a coherent way for all labs."""

    # Play nice with the API...
    sleep(1)
    geolocator = OpenCage(api_key=api_key, timeout=10)

    # Variables for storing the data
    data = {"city": None,
            "address_1": None,
            "postal_code": None,
            "country": None,
            "county": None,
            "state": None,
            "country_code": None,
            "latitude": None,
            "longitude": None,
            "continent": None}
    road = ""
    number = ""
    # Default None values
    location_data = {"city": None,
                     "road": None,
                     "house_number": None,
                     "postcode": None,
                     "country": None,
                     "county": None,
                     "state": None,
                     "ISO_3166-1_alpha-2": None,
                     "country_code": None,
                     "lat": None,
                     "lng": None}

    # Reverse geocoding ... from coordinates to address
    if format == "reverse":
        # If the query (coordinates) is not empty
        if query is None or len(query) < 2:
            pass
        else:
            location = geolocator.reverse(query)
            if location is not None:
                location_data = location.raw['components']
    # Direct geocoding ... from address to coordinates and full address
    if format == "direct":
        # If the query (address) is not empty
        if query is None or len(query) < 3:
            pass
        else:
            location = geolocator.geocode(query)
            if location is not None:
                location_data = location.raw['components']

    # Extract the meaningful data
    for component in location_data:
        if component == "town" or component == "city":
            data["city"] = location_data[component]
        if component == "road":
            road = location_data[component]
        if component == "house_number":
            number = location_data[component]
        if component == "postcode":
            data["postal_code"] = location_data[component]
        if component == "country":
            data["country"] = location_data[component]
        if component == "county":
            data["county"] = location_data[component]
        if component == "state":
            data["state"] = location_data[component]
        if component == "ISO_3166-1_alpha-3":
            data["country_code"] = location_data[component]
        if component == "continent":
            data["continent"] = location_data[component]
    data["address_1"] = location.raw['formatted']
    data["latitude"] = location.raw['geometry']["lat"]
    data["longitude"] = location.raw['geometry']["lng"]

    # Return the final data
    return data


if __name__ == "__main__":
    pass
